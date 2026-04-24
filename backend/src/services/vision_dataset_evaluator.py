from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Callable

from src.services.image_analysis import DetectedOutfitItem, analyze_outfit_items


@dataclass(frozen=True)
class DatasetLabelItem:
    category: str
    color: str
    item_label: str
    notes: str = ""

    @property
    def key(self) -> tuple[str, str, str]:
        return (self.category, self.color, self.item_label)


@dataclass(frozen=True)
class DatasetSample:
    sample_id: str
    image_path: Path
    label_path: Path
    expected_items: tuple[DatasetLabelItem, ...]


@dataclass(frozen=True)
class SampleEvaluation:
    sample_id: str
    expected_count: int
    predicted_count: int
    matched_count: int
    exact_match: bool
    missing_items: tuple[str, ...]
    unexpected_items: tuple[str, ...]
    matched_items: tuple[str, ...]


@dataclass(frozen=True)
class DatasetEvaluationSummary:
    sample_count: int
    expected_item_count: int
    predicted_item_count: int
    matched_item_count: int
    exact_match_sample_count: int
    item_precision: float
    item_recall: float
    exact_match_accuracy: float
    category_recall: dict[str, float]
    samples: tuple[SampleEvaluation, ...]


def load_dataset_samples(dataset_root: Path) -> list[DatasetSample]:
    labels_dir = dataset_root / "labels"
    images_dir = dataset_root / "images"
    samples: list[DatasetSample] = []

    for label_path in sorted(labels_dir.glob("*.json")):
        payload = json.loads(label_path.read_text(encoding="utf-8"))
        sample_id = payload["sample_id"]
        image_candidates = sorted(images_dir.glob(f"{sample_id}.*"))
        if not image_candidates:
            raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {sample_id}")

        expected_items = tuple(
            DatasetLabelItem(
                category=item["category"],
                color=item["color"],
                item_label=item["item_label"],
                notes=item.get("notes", ""),
            )
            for item in payload.get("items", [])
        )
        samples.append(
            DatasetSample(
                sample_id=sample_id,
                image_path=image_candidates[0],
                label_path=label_path,
                expected_items=expected_items,
            )
        )
    return samples


def evaluate_dataset(
    dataset_root: Path,
    predictor: Callable[[bytes], list[DetectedOutfitItem]] | None = None,
) -> DatasetEvaluationSummary:
    predictor = predictor or analyze_outfit_items
    samples = load_dataset_samples(dataset_root)
    evaluated_samples: list[SampleEvaluation] = []
    expected_total = 0
    predicted_total = 0
    matched_total = 0
    exact_sample_total = 0
    category_expected = Counter()
    category_matched = Counter()

    for sample in samples:
        content = sample.image_path.read_bytes()
        predicted_items = predictor(content)

        expected_counter = Counter(item.key for item in sample.expected_items)
        predicted_counter = Counter((item.category, item.color, item.item_label) for item in predicted_items)
        matched_counter = expected_counter & predicted_counter
        missing_counter = expected_counter - predicted_counter
        unexpected_counter = predicted_counter - expected_counter

        matched_items = _expand_counter_strings(matched_counter)
        missing_items = _expand_counter_strings(missing_counter)
        unexpected_items = _expand_counter_strings(unexpected_counter)
        matched_count = sum(matched_counter.values())

        expected_total += sum(expected_counter.values())
        predicted_total += sum(predicted_counter.values())
        matched_total += matched_count
        exact_match = not missing_items and not unexpected_items
        if exact_match:
            exact_sample_total += 1

        sample_expected_categories = Counter(item.category for item in sample.expected_items)
        sample_matched_categories = Counter(key[0] for key, count in matched_counter.items() for _ in range(count))
        category_expected.update(sample_expected_categories)
        category_matched.update(sample_matched_categories)

        evaluated_samples.append(
            SampleEvaluation(
                sample_id=sample.sample_id,
                expected_count=sum(expected_counter.values()),
                predicted_count=sum(predicted_counter.values()),
                matched_count=matched_count,
                exact_match=exact_match,
                missing_items=tuple(missing_items),
                unexpected_items=tuple(unexpected_items),
                matched_items=tuple(matched_items),
            )
        )

    category_recall = {
        category: round(category_matched[category] / category_expected[category], 4)
        for category in sorted(category_expected)
        if category_expected[category] > 0
    }

    return DatasetEvaluationSummary(
        sample_count=len(evaluated_samples),
        expected_item_count=expected_total,
        predicted_item_count=predicted_total,
        matched_item_count=matched_total,
        exact_match_sample_count=exact_sample_total,
        item_precision=round(matched_total / predicted_total, 4) if predicted_total else 0.0,
        item_recall=round(matched_total / expected_total, 4) if expected_total else 0.0,
        exact_match_accuracy=round(exact_sample_total / len(evaluated_samples), 4) if evaluated_samples else 0.0,
        category_recall=category_recall,
        samples=tuple(evaluated_samples),
    )


def format_evaluation_text(summary: DatasetEvaluationSummary) -> str:
    lines = [
        "비전 데이터셋 평가 결과",
        f"- 샘플 수: {summary.sample_count}",
        f"- 정답 아이템 수: {summary.expected_item_count}",
        f"- 예측 아이템 수: {summary.predicted_item_count}",
        f"- 일치 아이템 수: {summary.matched_item_count}",
        f"- 아이템 정밀도: {summary.item_precision:.4f}",
        f"- 아이템 재현율: {summary.item_recall:.4f}",
        f"- 샘플 완전일치율: {summary.exact_match_accuracy:.4f} ({summary.exact_match_sample_count}/{summary.sample_count})",
        "- 카테고리별 재현율:",
    ]
    for category, recall in summary.category_recall.items():
        lines.append(f"  - {category}: {recall:.4f}")

    lines.append("- 샘플별 상세:")
    for sample in summary.samples:
        lines.append(
            f"  - {sample.sample_id}: matched={sample.matched_count}/{sample.expected_count}, "
            f"predicted={sample.predicted_count}, exact={sample.exact_match}"
        )
        if sample.missing_items:
            lines.append(f"    missing: {', '.join(sample.missing_items)}")
        if sample.unexpected_items:
            lines.append(f"    unexpected: {', '.join(sample.unexpected_items)}")
    return "\n".join(lines)


def _expand_counter_strings(counter: Counter[tuple[str, str, str]]) -> list[str]:
    values: list[str] = []
    for (category, color, item_label), count in sorted(counter.items()):
        values.extend([f"{category}:{color}:{item_label}"] * count)
    return values
