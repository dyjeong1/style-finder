from __future__ import annotations

from io import BytesIO

from PIL import Image, ImageDraw

from src.services.image_analysis import DetectedOutfitItem
from src.services.store import InMemoryStore
from src.services.vision_outfit_analyzer import (
    VisionOutfitAnalyzer,
    VisionOutfitAnalyzerConfig,
    merge_detected_items,
)


def build_flatlay_fixture() -> bytes:
    image = Image.new("RGB", (512, 768), (176, 142, 112))
    draw = ImageDraw.Draw(image)
    draw.rectangle((94, 90, 420, 196), fill=(18, 18, 22))
    draw.rectangle((118, 196, 394, 332), fill=(246, 246, 242))
    draw.rectangle((124, 334, 392, 706), fill=(243, 240, 232))
    draw.ellipse((44, 566, 126, 716), fill=(46, 28, 22))
    draw.ellipse((388, 548, 490, 712), fill=(242, 238, 228))

    output = BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()


def test_merge_detected_items_prefers_vision_category_and_keeps_fallback_rest() -> None:
    vision_items = [
        DetectedOutfitItem(category="top", color="blue", item_label="가디건", query="블루 가디건"),
        DetectedOutfitItem(category="accessory", color="black", item_label="안경", query="블랙 안경"),
    ]
    fallback_items = [
        DetectedOutfitItem(category="top", color="white", item_label="셔츠", query="화이트 셔츠"),
        DetectedOutfitItem(category="bottom", color="white", item_label="팬츠", query="화이트 팬츠"),
        DetectedOutfitItem(category="bag", color="white", item_label="숄더백", query="아이보리 숄더백"),
    ]

    merged = merge_detected_items(vision_items, fallback_items)

    assert [item.category for item in merged] == ["top", "bottom", "bag", "accessory"]
    assert merged[0].query == "블루 가디건"
    assert merged[1].query == "화이트 팬츠"
    assert merged[2].query == "아이보리 숄더백"
    assert merged[3].query == "블랙 안경"


def test_store_keeps_rule_based_analysis_when_vision_analyzer_disabled(tmp_path) -> None:
    store = InMemoryStore(
        wishlist_store_path=tmp_path / "wishlist.json",
        vision_outfit_analyzer=VisionOutfitAnalyzer(VisionOutfitAnalyzerConfig(enabled=False)),
    )

    record = store.create_upload(
        user_id="local-user",
        filename="flatlay.png",
        content_type="image/png",
        size_bytes=0,
        content=build_flatlay_fixture(),
    )

    assert record.analysis.category_query_hints["top"] == "화이트 셔츠"
    assert record.analysis.category_query_hints["outer"] == "블랙 니트 베스트"


def test_store_merges_mock_vision_items_with_rule_based_analysis(tmp_path) -> None:
    mock_items = (
        DetectedOutfitItem(category="top", color="blue", item_label="가디건", query="블루 가디건"),
        DetectedOutfitItem(category="accessory", color="black", item_label="안경", query="블랙 안경"),
    )
    store = InMemoryStore(
        wishlist_store_path=tmp_path / "wishlist.json",
        vision_outfit_analyzer=VisionOutfitAnalyzer(
            VisionOutfitAnalyzerConfig(enabled=True, provider="mock"),
            mock_items=mock_items,
        ),
    )

    record = store.create_upload(
        user_id="local-user",
        filename="flatlay.png",
        content_type="image/png",
        size_bytes=0,
        content=build_flatlay_fixture(),
    )

    assert record.analysis.category_query_hints["top"] == "블루 가디건"
    assert record.analysis.category_query_hints["accessory"] == "블랙 안경"
    assert record.analysis.category_query_hints["bottom"] == "화이트 팬츠"
