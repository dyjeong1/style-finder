from __future__ import annotations

from src.services.image_analysis import DetectedOutfitItem
from src.services.store import resolve_detected_items


def test_resolve_detected_items_keeps_ai_categories_without_rule_bag_supplement() -> None:
    detected_items, analysis_source, fallback_reason = resolve_detected_items(
        b"fixture",
        vision_predictor=lambda _content: [
            DetectedOutfitItem(category="top", color="white", item_label="셔츠", query="화이트 셔츠"),
            DetectedOutfitItem(category="bottom", color="black", item_label="슬랙스", query="블랙 슬랙스"),
        ],
        rule_predictor=lambda _content: [
            DetectedOutfitItem(category="bag", color="brown", item_label="숄더백", query="브라운 숄더백"),
        ],
    )

    assert [(item.category, item.query) for item in detected_items] == [
        ("top", "화이트 셔츠"),
        ("bottom", "블랙 슬랙스"),
    ]
    assert analysis_source == "vision"
    assert fallback_reason is None


def test_resolve_detected_items_uses_rule_fallback_only_when_vision_raises() -> None:
    def broken_predictor(_content: bytes) -> list[DetectedOutfitItem]:
        raise RuntimeError("provider crashed")

    detected_items, analysis_source, fallback_reason = resolve_detected_items(
        b"fixture",
        vision_predictor=broken_predictor,
        rule_predictor=lambda _content: [
            DetectedOutfitItem(category="outer", color="black", item_label="자켓", query="블랙 자켓"),
        ],
    )

    assert [(item.category, item.query) for item in detected_items] == [("outer", "블랙 자켓")]
    assert analysis_source == "rule_fallback"
    assert fallback_reason == "vision_error"


def test_resolve_detected_items_refines_generic_labels_with_same_category_rule_items_only() -> None:
    detected_items, analysis_source, fallback_reason = resolve_detected_items(
        b"fixture",
        vision_predictor=lambda _content: [
            DetectedOutfitItem(category="shoes", color="black", item_label="슈즈", query="블랙 슈즈"),
            DetectedOutfitItem(category="bag", color="brown", item_label="가방", query="브라운 가방"),
        ],
        rule_predictor=lambda _content: [
            DetectedOutfitItem(category="shoes", color="black", item_label="메리제인 슈즈", query="블랙 메리제인 슈즈"),
            DetectedOutfitItem(category="bag", color="brown", item_label="숄더백", query="브라운 숄더백"),
            DetectedOutfitItem(category="accessory", color="gray", item_label="목걸이", query="실버 목걸이"),
        ],
    )

    assert [(item.category, item.query) for item in detected_items] == [
        ("shoes", "블랙 메리제인 슈즈"),
        ("bag", "브라운 숄더백"),
    ]
    assert analysis_source == "vision"
    assert fallback_reason is None
