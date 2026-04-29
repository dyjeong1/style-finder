from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

from src.services.image_analysis import DetectedOutfitItem
from src.services.vision_dataset_evaluator import (
    compare_summaries,
    evaluate_dataset,
    format_comparison_text,
    format_evaluation_text,
    load_dataset_samples,
)


def _make_dataset(root: Path) -> Path:
    dataset_root = root / "vision_dataset"
    images_dir = dataset_root / "images"
    labels_dir = dataset_root / "labels"
    images_dir.mkdir(parents=True)
    labels_dir.mkdir(parents=True)

    image = Image.new("RGB", (32, 32), (255, 255, 255))
    image.save(images_dir / "sample-001.png")

    (labels_dir / "sample-001.json").write_text(
        json.dumps(
            {
                "sample_id": "sample-001",
                "source": "test",
                "items": [
                    {"category": "top", "color": "white", "item_label": "셔츠"},
                    {"category": "bottom", "color": "blue", "item_label": "데님 팬츠"},
                ],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    return dataset_root


def test_evaluate_dataset_calculates_summary(tmp_path: Path) -> None:
    dataset_root = _make_dataset(tmp_path)

    def predictor(_content: bytes) -> list[DetectedOutfitItem]:
        return [
            DetectedOutfitItem(category="top", color="white", item_label="셔츠", query="화이트 셔츠"),
            DetectedOutfitItem(category="bag", color="black", item_label="숄더백", query="블랙 숄더백"),
        ]

    summary = evaluate_dataset(dataset_root, predictor=predictor)

    assert summary.sample_count == 1
    assert summary.expected_item_count == 2
    assert summary.predicted_item_count == 2
    assert summary.matched_item_count == 1
    assert summary.item_precision == 0.5
    assert summary.item_recall == 0.5
    assert summary.exact_match_accuracy == 0.0
    assert summary.category_recall["top"] == 1.0
    assert summary.category_recall["bottom"] == 0.0
    assert summary.samples[0].missing_items == ("bottom:blue:데님 팬츠",)
    assert summary.samples[0].unexpected_items == ("bag:black:숄더백",)


def test_format_evaluation_text_contains_summary_and_sample_lines(tmp_path: Path) -> None:
    dataset_root = _make_dataset(tmp_path)

    def predictor(_content: bytes) -> list[DetectedOutfitItem]:
        return [DetectedOutfitItem(category="top", color="white", item_label="셔츠", query="화이트 셔츠")]

    summary = evaluate_dataset(dataset_root, predictor=predictor)
    text = format_evaluation_text(summary)

    assert "비전 데이터셋 평가 결과" in text
    assert "- 샘플 수: 1" in text
    assert "sample-001" in text
    assert "missing: bottom:blue:데님 팬츠" in text


def test_compare_summaries_reports_improvement(tmp_path: Path) -> None:
    dataset_root = _make_dataset(tmp_path)

    def baseline_predictor(_content: bytes) -> list[DetectedOutfitItem]:
        return [DetectedOutfitItem(category="top", color="white", item_label="셔츠", query="화이트 셔츠")]

    def candidate_predictor(_content: bytes) -> list[DetectedOutfitItem]:
        return [
            DetectedOutfitItem(category="top", color="white", item_label="셔츠", query="화이트 셔츠"),
            DetectedOutfitItem(category="bottom", color="blue", item_label="데님 팬츠", query="블루 데님 팬츠"),
        ]

    baseline = evaluate_dataset(dataset_root, predictor=baseline_predictor)
    candidate = evaluate_dataset(dataset_root, predictor=candidate_predictor)
    comparison = compare_summaries("rule", baseline, "gemini", candidate)
    text = format_comparison_text(comparison)

    assert comparison.precision_delta == 0.0
    assert comparison.recall_delta == 0.5
    assert comparison.improved_samples == ("sample-001",)
    assert "비전 분석기 비교 결과" in text
    assert "기준 분석기: rule" in text
    assert "비교 분석기: gemini" in text


def test_load_dataset_samples_supports_sample_ids_offset_and_limit(tmp_path: Path) -> None:
    dataset_root = _make_dataset(tmp_path)
    labels_dir = dataset_root / "labels"
    images_dir = dataset_root / "images"

    image = Image.new("RGB", (32, 32), (0, 0, 0))
    image.save(images_dir / "sample-002.png")
    (labels_dir / "sample-002.json").write_text(
        json.dumps(
            {
                "sample_id": "sample-002",
                "source": "test",
                "items": [{"category": "bag", "color": "black", "item_label": "숄더백"}],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    filtered = load_dataset_samples(dataset_root, sample_ids=("sample-002",))
    assert [sample.sample_id for sample in filtered] == ["sample-002"]

    windowed = load_dataset_samples(dataset_root, offset=1, limit=1)
    assert [sample.sample_id for sample in windowed] == ["sample-002"]
