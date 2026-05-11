from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.compare_vision_predictors import build_comparison_report_payload, _resolve_predictor
from src.services.vision_dataset_evaluator import compare_summaries, evaluate_dataset, format_comparison_text


def validate_dataset_root(dataset_root: Path) -> None:
    labels_dir = dataset_root / "labels"
    images_dir = dataset_root / "images"
    if not dataset_root.exists():
        raise FileNotFoundError(f"데이터셋 루트가 없습니다: {dataset_root}")
    if not labels_dir.exists() or not any(labels_dir.glob("*.json")):
        raise FileNotFoundError(f"정답 라벨 파일이 없습니다: {labels_dir}")
    if not images_dir.exists() or not any(images_dir.iterdir()):
        raise FileNotFoundError(f"이미지 파일이 없습니다: {images_dir}")


def build_report_stem(
    *,
    baseline_name: str,
    candidate_name: str,
    sample_ids: tuple[str, ...] = (),
    offset: int = 0,
    limit: int | None = None,
    generated_at: datetime | None = None,
) -> str:
    generated_at = generated_at or datetime.now(timezone.utc)
    timestamp = generated_at.strftime("%Y%m%d-%H%M%S")
    scope_parts: list[str] = []
    if sample_ids:
        scope_parts.append(f"samples-{'-'.join(sample_ids)}")
    if offset:
        scope_parts.append(f"offset-{offset}")
    if limit is not None:
        scope_parts.append(f"limit-{limit}")
    scope_suffix = f"-{'-'.join(scope_parts)}" if scope_parts else ""
    return f"{candidate_name}-vs-{baseline_name}-{timestamp}{scope_suffix}"


def generate_openai_comparison_artifacts(
    *,
    dataset_root: Path,
    baseline_name: str = "rule",
    candidate_name: str = "openai",
    sample_ids: tuple[str, ...] = (),
    offset: int = 0,
    limit: int | None = None,
    timeout_seconds: float | None = None,
    max_retries: int = 2,
    use_cache: bool = True,
    generated_at: datetime | None = None,
) -> dict[str, object]:
    validate_dataset_root(dataset_root)
    baseline_cache = dataset_root / "cache" / f"{baseline_name}.json"
    candidate_cache = dataset_root / "cache" / f"{candidate_name}.json"
    report_root = dataset_root / "reports" / "openai"
    report_root.mkdir(parents=True, exist_ok=True)
    report_stem = build_report_stem(
        baseline_name=baseline_name,
        candidate_name=candidate_name,
        sample_ids=sample_ids,
        offset=offset,
        limit=limit,
        generated_at=generated_at,
    )
    json_path = report_root / f"{report_stem}.json"
    text_path = report_root / f"{report_stem}.txt"

    baseline_predictor = _resolve_predictor(
        baseline_name,
        dataset_root=dataset_root,
        cache_path=baseline_cache if baseline_name != "rule" else None,
        min_interval_seconds=12.5 if baseline_name == "gemini" else 0.0,
        max_retries=max_retries,
        timeout_seconds=timeout_seconds if baseline_name != "rule" else None,
        use_cache=use_cache,
    )
    candidate_predictor = _resolve_predictor(
        candidate_name,
        dataset_root=dataset_root,
        cache_path=candidate_cache if candidate_name != "rule" else None,
        min_interval_seconds=0.0,
        max_retries=max_retries,
        timeout_seconds=timeout_seconds if candidate_name != "rule" else None,
        use_cache=use_cache,
    )

    selected_sample_ids = sample_ids or None
    baseline_summary = evaluate_dataset(
        dataset_root,
        predictor=baseline_predictor,
        sample_ids=selected_sample_ids,
        offset=offset,
        limit=limit,
    )
    candidate_summary = evaluate_dataset(
        dataset_root,
        predictor=candidate_predictor,
        sample_ids=selected_sample_ids,
        offset=offset,
        limit=limit,
    )
    comparison = compare_summaries(
        baseline_name=baseline_name,
        baseline=baseline_summary,
        candidate_name=candidate_name,
        candidate=candidate_summary,
    )
    report_payload = build_comparison_report_payload(dataset_root, comparison)
    text_summary = format_comparison_text(comparison)
    json_path.write_text(json.dumps(report_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    text_path.write_text(text_summary + "\n", encoding="utf-8")

    return {
        "baseline_name": baseline_name,
        "candidate_name": candidate_name,
        "json_report_path": str(json_path),
        "text_report_path": str(text_path),
        "precision_delta": comparison.precision_delta,
        "recall_delta": comparison.recall_delta,
        "exact_match_delta": comparison.exact_match_delta,
        "candidate_summary": {
            "item_precision": comparison.candidate.item_precision,
            "item_recall": comparison.candidate.item_recall,
            "exact_match_accuracy": comparison.candidate.exact_match_accuracy,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="OpenAI Vision 정답 비교 리포트 자동 생성")
    parser.add_argument(
        "--dataset-root",
        default=str(ROOT / "data" / "vision_dataset"),
        help="데이터셋 루트 경로",
    )
    parser.add_argument(
        "--baseline",
        default="rule",
        help="기준 분석기 이름 (기본값: rule)",
    )
    parser.add_argument(
        "--candidate",
        default="openai",
        help="비교 분석기 이름 (기본값: openai)",
    )
    parser.add_argument(
        "--sample-ids",
        default="",
        help="쉼표로 구분한 샘플 ID 목록만 실행",
    )
    parser.add_argument(
        "--offset",
        type=int,
        default=0,
        help="앞에서 건너뛸 샘플 수",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="실행할 최대 샘플 수",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=None,
        help="이번 실행에만 적용할 provider 타임아웃(초)",
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=2,
        help="OpenAI 호출 실패 시 샘플별 최대 재시도 횟수",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="OpenAI 캐시를 읽거나 저장하지 않고 새 결과로 실행",
    )
    args = parser.parse_args()

    payload = generate_openai_comparison_artifacts(
        dataset_root=Path(args.dataset_root),
        baseline_name=args.baseline,
        candidate_name=args.candidate,
        sample_ids=tuple(sample_id.strip() for sample_id in args.sample_ids.split(",") if sample_id.strip()),
        offset=args.offset,
        limit=args.limit,
        timeout_seconds=args.timeout_seconds,
        max_retries=args.max_retries,
        use_cache=not args.no_cache,
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
