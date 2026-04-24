from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

from src.services.image_analysis import DetectedOutfitItem
from src.services.vision_dataset_evaluator import evaluate_dataset, format_evaluation_text


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
