from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
import time
from urllib.error import HTTPError, URLError


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.core.config import Settings
from src.services.image_analysis import DetectedOutfitItem, analyze_outfit_items
from src.services.vision_dataset_evaluator import (
    compare_summaries,
    evaluate_dataset,
    format_comparison_text,
)
from src.services.vision_outfit_analyzer import (
    VisionOutfitAnalyzer,
    VisionOutfitAnalyzerConfig,
    summarize_provider_error,
)


def build_predictor(
    name: str,
    cache_path: Path | None = None,
    min_interval_seconds: float = 0.0,
    max_retries: int = 2,
):
    normalized = name.lower()
    if normalized == "rule":
        return analyze_outfit_items

    settings = Settings()
    provider = normalized
    model_name = settings.vision_outfit_analyzer_model_name
    api_key = settings.openai_api_key
    api_base_url = settings.vision_outfit_analyzer_api_base_url

    if provider == "gemini":
        model_name = settings.vision_outfit_analyzer_model_name or "gemini-2.5-flash"
        api_key = settings.gemini_api_key
    elif provider == "openai":
        model_name = settings.vision_outfit_analyzer_model_name or "gpt-4o"

    analyzer = VisionOutfitAnalyzer(
        VisionOutfitAnalyzerConfig(
            enabled=True,
            provider=provider,
            model_name=model_name,
            max_image_bytes=settings.vision_outfit_analyzer_max_image_bytes,
            timeout_seconds=settings.vision_outfit_analyzer_timeout_seconds,
            api_base_url=api_base_url,
            api_key=api_key,
        )
    )
    cache = load_cache(cache_path) if cache_path else {}
    last_called_at = {"value": 0.0}

    def predictor(content: bytes):
        cache_key = hashlib.sha256(content).hexdigest()
        if cache_key in cache:
            return deserialize_items(cache[cache_key])

        for attempt in range(max_retries + 1):
            wait_seconds = min_interval_seconds - (time.monotonic() - last_called_at["value"])
            if wait_seconds > 0:
                time.sleep(wait_seconds)

            try:
                items = analyzer.analyze_or_raise(content)
                last_called_at["value"] = time.monotonic()
                cache[cache_key] = serialize_items(items)
                if cache_path:
                    save_cache(cache_path, cache)
                return items
            except (HTTPError, URLError, ValueError) as exc:
                last_called_at["value"] = time.monotonic()
                if attempt >= max_retries:
                    print(f"{normalized} predictor fallback: {summarize_provider_error(exc)}", file=sys.stderr)
                    return []

                retry_delay = parse_retry_delay_seconds(exc)
                time.sleep(retry_delay)

        return []

    return predictor


def main() -> int:
    parser = argparse.ArgumentParser(description="규칙 기반 분석기와 AI 비전 분석기 비교")
    parser.add_argument(
        "--dataset-root",
        default=str(ROOT / "data" / "vision_dataset"),
        help="데이터셋 루트 경로",
    )
    parser.add_argument(
        "--baseline",
        default="rule",
        choices=("rule", "openai", "gemini"),
        help="기준 분석기",
    )
    parser.add_argument(
        "--candidate",
        default="gemini",
        choices=("rule", "openai", "gemini"),
        help="비교 분석기",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="출력 형식",
    )
    parser.add_argument(
        "--min-interval-seconds",
        type=float,
        default=None,
        help="AI provider 호출 간 최소 대기 시간(초)",
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=2,
        help="AI provider 실패 시 샘플별 최대 재시도 횟수",
    )
    args = parser.parse_args()

    dataset_root = Path(args.dataset_root)
    baseline_cache = dataset_root / "cache" / f"{args.baseline}.json"
    candidate_cache = dataset_root / "cache" / f"{args.candidate}.json"
    interval_seconds = args.min_interval_seconds
    if interval_seconds is None:
        interval_seconds = 12.5 if args.candidate == "gemini" else 0.0

    baseline_summary = evaluate_dataset(
        dataset_root,
        predictor=build_predictor(
            args.baseline,
            cache_path=baseline_cache if args.baseline != "rule" else None,
            min_interval_seconds=12.5 if args.baseline == "gemini" else 0.0,
            max_retries=args.max_retries,
        ),
    )
    candidate_summary = evaluate_dataset(
        dataset_root,
        predictor=build_predictor(
            args.candidate,
            cache_path=candidate_cache if args.candidate != "rule" else None,
            min_interval_seconds=interval_seconds,
            max_retries=args.max_retries,
        ),
    )
    comparison = compare_summaries(
        baseline_name=args.baseline,
        baseline=baseline_summary,
        candidate_name=args.candidate,
        candidate=candidate_summary,
    )

    if args.format == "json":
        payload = {
            "baseline_name": comparison.baseline_name,
            "candidate_name": comparison.candidate_name,
            "precision_delta": comparison.precision_delta,
            "recall_delta": comparison.recall_delta,
            "exact_match_delta": comparison.exact_match_delta,
            "improved_samples": list(comparison.improved_samples),
            "worsened_samples": list(comparison.worsened_samples),
            "unchanged_samples": list(comparison.unchanged_samples),
            "baseline": {
                "item_precision": comparison.baseline.item_precision,
                "item_recall": comparison.baseline.item_recall,
                "exact_match_accuracy": comparison.baseline.exact_match_accuracy,
            },
            "candidate": {
                "item_precision": comparison.candidate.item_precision,
                "item_recall": comparison.candidate.item_recall,
                "exact_match_accuracy": comparison.candidate.exact_match_accuracy,
            },
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(format_comparison_text(comparison))
    return 0


def load_cache(path: Path) -> dict[str, list[dict[str, str]]]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def save_cache(path: Path, payload: dict[str, list[dict[str, str]]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def serialize_items(items):
    return [
        {
            "category": item.category,
            "color": item.color,
            "item_label": item.item_label,
            "query": item.query,
        }
        for item in items
    ]


def deserialize_items(raw_items):
    return [DetectedOutfitItem(**raw_item) for raw_item in raw_items]


def parse_retry_delay_seconds(exc: Exception) -> float:
    if isinstance(exc, HTTPError):
        try:
            body = exc.read().decode("utf-8")
            payload = json.loads(body)
        except Exception:
            return 12.5

        for detail in payload.get("error", {}).get("details", []):
            retry_delay = detail.get("retryDelay")
            if isinstance(retry_delay, str) and retry_delay.endswith("s"):
                try:
                    return max(float(retry_delay[:-1]), 1.0)
                except ValueError:
                    return 12.5
    return 12.5


if __name__ == "__main__":
    raise SystemExit(main())
