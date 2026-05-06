from __future__ import annotations

from io import BytesIO
import json

from PIL import Image, ImageDraw

from src.core.config import Settings, resolve_vision_outfit_analyzer_runtime_config
from src.services.image_analysis import DetectedOutfitItem
from src.services.store import (
    InMemoryStore,
    apply_selective_category_corrections,
    resolve_detected_items,
    _sort_detected_items_for_display,
    select_gemini_correction_categories,
)
from src.services.vision_outfit_analyzer import (
    VisionOutfitAnalyzer,
    VisionOutfitAnalyzerConfig,
    build_item_query,
    ensure_local_provider_reachable,
    guess_mime_type,
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
        DetectedOutfitItem(category="accessory", color="gray", item_label="목걸이", query="그레이 목걸이"),
    ]
    fallback_items = [
        DetectedOutfitItem(category="top", color="white", item_label="셔츠", query="화이트 셔츠"),
        DetectedOutfitItem(category="bottom", color="white", item_label="팬츠", query="화이트 팬츠"),
        DetectedOutfitItem(category="bag", color="white", item_label="숄더백", query="아이보리 숄더백"),
    ]

    merged = merge_detected_items(vision_items, fallback_items)

    assert [item.category for item in merged] == ["top", "bottom", "bag", "accessory", "accessory"]
    assert merged[0].query == "블루 가디건"
    assert merged[1].query == "화이트 팬츠"
    assert merged[2].query == "아이보리 숄더백"
    assert merged[3].query == "블랙 안경"
    assert merged[4].query == "그레이 목걸이"


def test_merge_detected_items_reconciles_outer_color_and_bottom_specificity() -> None:
    vision_items = [
        DetectedOutfitItem(category="outer", color="gray", item_label="가디건", query="그레이 가디건"),
        DetectedOutfitItem(category="bottom", color="blue", item_label="데님 팬츠", query="블루 데님 팬츠"),
    ]
    fallback_items = [
        DetectedOutfitItem(category="outer", color="blue", item_label="가디건", query="블루 가디건"),
        DetectedOutfitItem(category="bottom", color="navy", item_label="와이드 데님 팬츠", query="네이비 와이드 데님 팬츠"),
    ]

    merged = merge_detected_items(vision_items, fallback_items)

    assert [(item.category, item.query) for item in merged] == [
        ("outer", "블루 가디건"),
        ("bottom", "네이비 와이드 데님 팬츠"),
    ]


def test_merge_detected_items_reassigns_cardigan_from_top_to_outer_and_keeps_fallback_top() -> None:
    vision_items = [
        DetectedOutfitItem(category="top", color="blue", item_label="가디건", query="블루 가디건"),
    ]
    fallback_items = [
        DetectedOutfitItem(category="top", color="white", item_label="셔츠", query="화이트 셔츠"),
        DetectedOutfitItem(category="outer", color="blue", item_label="가디건", query="블루 가디건"),
    ]

    merged = merge_detected_items(vision_items, fallback_items)

    assert [(item.category, item.query) for item in merged] == [
        ("top", "화이트 셔츠"),
        ("outer", "블루 가디건"),
    ]


def test_merge_detected_items_refines_generic_bag_with_more_specific_fallback() -> None:
    vision_items = [
        DetectedOutfitItem(category="bag", color="brown", item_label="가방", query="브라운 가방"),
    ]
    fallback_items = [
        DetectedOutfitItem(category="bag", color="brown", item_label="숄더백", query="브라운 숄더백"),
    ]

    merged = merge_detected_items(vision_items, fallback_items)

    assert [(item.category, item.query) for item in merged] == [
        ("bag", "브라운 숄더백"),
    ]


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
    assert record.analysis.analysis_source == "rule_fallback"
    assert record.analysis.query_source == "rule_fallback"
    assert record.analysis.fallback_reason == "vision_disabled"


def test_store_keeps_mock_vision_items_and_only_supplements_missing_bag(tmp_path) -> None:
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
    assert record.analysis.category_query_hints["bag"] == "아이보리 숄더백"
    assert record.analysis.category_query_hints["accessory"] == "블랙 안경"
    assert "bottom" not in record.analysis.category_query_hints
    assert [item.query for item in record.analysis.detected_items] == ["블루 가디건", "아이보리 숄더백", "블랙 안경"]


def test_store_keeps_all_detected_items_but_uses_first_query_hint_per_category(tmp_path) -> None:
    mock_items = (
        DetectedOutfitItem(category="accessory", color="black", item_label="안경", query="블랙 안경"),
        DetectedOutfitItem(category="accessory", color="gray", item_label="목걸이", query="그레이 목걸이"),
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

    assert [item.query for item in record.analysis.detected_items if item.category == "accessory"] == [
        "블랙 안경",
        "그레이 목걸이",
    ]
    assert record.analysis.category_query_hints["accessory"] == "블랙 안경"


def test_select_gemini_correction_categories_targets_layered_and_conflicting_categories() -> None:
    vision_items = [
        DetectedOutfitItem(category="top", color="white", item_label="셔츠", query="화이트 셔츠"),
        DetectedOutfitItem(category="outer", color="gray", item_label="가디건", query="그레이 가디건"),
        DetectedOutfitItem(category="bottom", color="blue", item_label="데님 팬츠", query="블루 데님 팬츠"),
    ]
    merged_items = tuple(vision_items)

    categories = select_gemini_correction_categories(vision_items, merged_items)

    assert categories == ("top", "outer", "bottom")


def test_select_gemini_correction_categories_does_not_add_missing_category_from_rule_signal() -> None:
    vision_items = [
        DetectedOutfitItem(category="top", color="white", item_label="탑", query="화이트 탑"),
    ]
    categories = select_gemini_correction_categories(vision_items, tuple(vision_items))

    assert categories == ("top",)


def test_apply_selective_category_corrections_replaces_only_targeted_categories() -> None:
    base_items = (
        DetectedOutfitItem(category="top", color="white", item_label="셔츠", query="화이트 셔츠"),
        DetectedOutfitItem(category="outer", color="blue", item_label="가디건", query="블루 가디건"),
        DetectedOutfitItem(category="bottom", color="black", item_label="데님 팬츠", query="블랙 데님 팬츠"),
        DetectedOutfitItem(category="bag", color="brown", item_label="숄더백", query="브라운 숄더백"),
        DetectedOutfitItem(category="accessory", color="black", item_label="안경", query="블랙 안경"),
    )
    correction_items = [
        DetectedOutfitItem(category="top", color="white", item_label="슬리브리스 탑", query="화이트 슬리브리스 탑"),
        DetectedOutfitItem(category="accessory", color="black", item_label="안경", query="블랙 안경"),
        DetectedOutfitItem(category="accessory", color="gray", item_label="귀걸이", query="그레이 귀걸이"),
    ]

    corrected = apply_selective_category_corrections(base_items, correction_items, ("top", "accessory"))

    assert [(item.category, item.query) for item in corrected] == [
        ("top", "화이트 슬리브리스 탑"),
        ("outer", "블루 가디건"),
        ("bottom", "블랙 데님 팬츠"),
        ("bag", "브라운 숄더백"),
        ("accessory", "블랙 안경"),
    ]


def test_sort_detected_items_for_display_prioritizes_jewelry_over_ring_and_socks() -> None:
    items = [
        DetectedOutfitItem(category="accessory", color="white", item_label="양말", query="화이트 양말"),
        DetectedOutfitItem(category="accessory", color="gray", item_label="반지", query="실버 반지"),
        DetectedOutfitItem(category="accessory", color="gray", item_label="목걸이", query="실버 목걸이"),
        DetectedOutfitItem(category="accessory", color="gray", item_label="팔찌", query="실버 팔찌"),
    ]

    sorted_items = _sort_detected_items_for_display(items)

    assert [item.query for item in sorted_items] == [
        "실버 목걸이",
        "실버 팔찌",
        "실버 반지",
        "화이트 양말",
    ]


def test_store_applies_optional_gemini_correction_to_generic_bag_label(tmp_path) -> None:
    primary_items = (
        DetectedOutfitItem(category="top", color="white", item_label="티셔츠", query="화이트 티셔츠"),
        DetectedOutfitItem(category="bag", color="brown", item_label="가방", query="브라운 가방"),
    )
    correction_items = (
        DetectedOutfitItem(category="bag", color="brown", item_label="숄더백", query="브라운 숄더백"),
    )
    store = InMemoryStore(
        wishlist_store_path=tmp_path / "wishlist.json",
        vision_outfit_analyzer=VisionOutfitAnalyzer(
            VisionOutfitAnalyzerConfig(enabled=True, provider="mock"),
            mock_items=primary_items,
        ),
        gemini_correction_analyzer=VisionOutfitAnalyzer(
            VisionOutfitAnalyzerConfig(enabled=True, provider="mock"),
            mock_items=correction_items,
        ),
        enable_gemini_correction=True,
    )

    record = store.create_upload(
        user_id="local-user",
        filename="flatlay.png",
        content_type="image/png",
        size_bytes=0,
        content=build_flatlay_fixture(),
    )

    assert record.analysis.category_query_hints["bag"] == "브라운 숄더백"


def test_store_applies_optional_gemini_correction_for_ambiguous_ollama_output(tmp_path) -> None:
    primary_items = (
        DetectedOutfitItem(category="top", color="white", item_label="셔츠", query="화이트 셔츠"),
        DetectedOutfitItem(category="outer", color="gray", item_label="가디건", query="그레이 가디건"),
        DetectedOutfitItem(category="bottom", color="blue", item_label="데님 팬츠", query="블루 데님 팬츠"),
        DetectedOutfitItem(category="accessory", color="black", item_label="안경", query="블랙 안경"),
    )
    correction_items = (
        DetectedOutfitItem(category="top", color="white", item_label="슬리브리스 탑", query="화이트 슬리브리스 탑"),
        DetectedOutfitItem(category="outer", color="blue", item_label="가디건", query="블루 가디건"),
        DetectedOutfitItem(category="bottom", color="black", item_label="와이드 데님 팬츠", query="블랙 와이드 데님 팬츠"),
        DetectedOutfitItem(category="accessory", color="black", item_label="안경", query="블랙 안경"),
        DetectedOutfitItem(category="accessory", color="black", item_label="귀걸이", query="블랙 귀걸이"),
    )
    store = InMemoryStore(
        wishlist_store_path=tmp_path / "wishlist.json",
        vision_outfit_analyzer=VisionOutfitAnalyzer(
            VisionOutfitAnalyzerConfig(enabled=True, provider="mock"),
            mock_items=primary_items,
        ),
        gemini_correction_analyzer=VisionOutfitAnalyzer(
            VisionOutfitAnalyzerConfig(enabled=True, provider="mock"),
            mock_items=correction_items,
        ),
        enable_gemini_correction=True,
    )

    record = store.create_upload(
        user_id="local-user",
        filename="flatlay.png",
        content_type="image/png",
        size_bytes=0,
        content=build_flatlay_fixture(),
    )

    assert record.analysis.category_query_hints["top"] == "화이트 슬리브리스 탑"
    assert record.analysis.category_query_hints["outer"] == "블루 가디건"
    assert record.analysis.category_query_hints["bottom"] == "블랙 와이드 데님 팬츠"
    assert [item.query for item in record.analysis.detected_items if item.category == "accessory"] == [
        "블랙 안경",
    ]


def test_store_keeps_multiple_new_jewelry_items_from_correction_when_they_appear_as_a_set(tmp_path) -> None:
    primary_items = (
        DetectedOutfitItem(category="top", color="white", item_label="티셔츠", query="화이트 티셔츠"),
        DetectedOutfitItem(category="accessory", color="white", item_label="양말", query="화이트 양말"),
    )
    correction_items = (
        DetectedOutfitItem(category="accessory", color="gray", item_label="목걸이", query="실버 목걸이"),
        DetectedOutfitItem(category="accessory", color="gray", item_label="팔찌", query="실버 팔찌"),
        DetectedOutfitItem(category="accessory", color="gray", item_label="반지", query="실버 반지"),
    )
    store = InMemoryStore(
        wishlist_store_path=tmp_path / "wishlist.json",
        vision_outfit_analyzer=VisionOutfitAnalyzer(
            VisionOutfitAnalyzerConfig(enabled=True, provider="mock"),
            mock_items=primary_items,
        ),
        gemini_correction_analyzer=VisionOutfitAnalyzer(
            VisionOutfitAnalyzerConfig(enabled=True, provider="mock"),
            mock_items=correction_items,
        ),
        enable_gemini_correction=True,
    )

    record = store.create_upload(
        user_id="local-user",
        filename="flatlay.png",
        content_type="image/png",
        size_bytes=0,
        content=build_flatlay_fixture(),
    )

    assert [item.query for item in record.analysis.detected_items if item.category == "accessory"] == [
        "실버 목걸이",
        "실버 팔찌",
        "실버 반지",
    ]


def test_store_does_not_use_rule_fallback_when_ai_returns_empty_result(tmp_path) -> None:
    store = InMemoryStore(
        wishlist_store_path=tmp_path / "wishlist.json",
        vision_outfit_analyzer=VisionOutfitAnalyzer(
            VisionOutfitAnalyzerConfig(enabled=True, provider="mock"),
            mock_items=(),
        ),
    )

    record = store.create_upload(
        user_id="local-user",
        filename="flatlay.png",
        content_type="image/png",
        size_bytes=0,
        content=build_flatlay_fixture(),
    )

    assert record.analysis.analysis_source == "vision"
    assert record.analysis.query_source == "none"
    assert record.analysis.fallback_reason is None
    assert record.analysis.category_query_hints == {}
    assert record.analysis.detected_items == ()


def test_resolve_detected_items_prefers_vision_and_applies_correction_without_rule_fill() -> None:
    detected_items, analysis_source, fallback_reason = resolve_detected_items(
        b"fixture",
        vision_predictor=lambda _content: [
            DetectedOutfitItem(category="top", color="white", item_label="셔츠", query="화이트 셔츠"),
        ],
        correction_predictor=lambda _content: [
            DetectedOutfitItem(category="top", color="white", item_label="슬리브리스 탑", query="화이트 슬리브리스 탑"),
            DetectedOutfitItem(category="shoes", color="gray", item_label="스니커즈", query="그레이 스니커즈"),
        ],
        enable_gemini_correction=True,
        rule_predictor=lambda _content: [
            DetectedOutfitItem(category="shoes", color="gray", item_label="스니커즈", query="그레이 스니커즈"),
        ],
    )

    assert [(item.category, item.query) for item in detected_items] == [
        ("top", "화이트 슬리브리스 탑"),
    ]
    assert analysis_source == "vision"
    assert fallback_reason is None


def test_resolve_detected_items_supplements_missing_bag_from_rule_signal() -> None:
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
        ("bag", "브라운 숄더백"),
    ]
    assert analysis_source == "vision"
    assert fallback_reason is None


def test_resolve_detected_items_keeps_empty_ai_result_without_rule_fallback() -> None:
    detected_items, analysis_source, fallback_reason = resolve_detected_items(
        b"fixture",
        vision_predictor=lambda _content: [],
        rule_predictor=lambda _content: [
            DetectedOutfitItem(category="outer", color="black", item_label="자켓", query="블랙 자켓"),
        ],
    )

    assert detected_items == ()
    assert analysis_source == "vision"
    assert fallback_reason is None


def test_resolve_detected_items_uses_rule_only_when_ai_raises() -> None:
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


def test_store_falls_back_immediately_when_local_ollama_is_unreachable(tmp_path, monkeypatch) -> None:
    def fake_create_connection(*_args, **_kwargs):
        raise ConnectionRefusedError("ollama is not running")

    monkeypatch.setattr("src.services.vision_outfit_analyzer.socket.create_connection", fake_create_connection)

    store = InMemoryStore(
        wishlist_store_path=tmp_path / "wishlist.json",
        vision_outfit_analyzer=VisionOutfitAnalyzer(
            VisionOutfitAnalyzerConfig(
                enabled=True,
                provider="ollama",
                model_name="gemma3:4b",
                api_base_url="http://127.0.0.1:11434/api/chat",
                timeout_seconds=120.0,
            )
        ),
    )

    record = store.create_upload(
        user_id="local-user",
        filename="flatlay.png",
        content_type="image/png",
        size_bytes=0,
        content=build_flatlay_fixture(),
    )

    assert record.analysis.analysis_source == "rule_fallback"
    assert record.analysis.query_source == "rule_fallback"
    assert record.analysis.fallback_reason == "provider_unreachable"
    assert record.analysis.category_query_hints["top"] == "화이트 셔츠"


def test_local_provider_reachability_probe_skips_remote_hosts(monkeypatch) -> None:
    called = False

    def fake_create_connection(*_args, **_kwargs):
        nonlocal called
        called = True
        raise AssertionError("remote host should not be probed")

    monkeypatch.setattr("src.services.vision_outfit_analyzer.socket.create_connection", fake_create_connection)

    ensure_local_provider_reachable("https://api.openai.com/v1/responses")

    assert called is False


def test_openai_provider_uses_structured_response_and_normalizes_items(monkeypatch) -> None:
    analyzer = VisionOutfitAnalyzer(
        VisionOutfitAnalyzerConfig(
            enabled=True,
            provider="openai",
            model_name="gpt-4o",
            api_key="test-key",
        )
    )
    captured_payload: dict[str, object] = {}

    def fake_post_json(url: str, payload: dict[str, object], headers: dict[str, str]) -> dict[str, object]:
        captured_payload["url"] = url
        captured_payload["headers"] = headers
        captured_payload.update(payload)
        return {
            "output": [
                {
                    "content": [
                        {
                            "type": "output_text",
                            "text": '{"items":[{"category":"outer","color":"blue","item_label":"가디건","query":"블루 가디건"},{"category":"accessory","color":"gray","item_label":"목걸이","query":""}]}',
                        }
                    ]
                }
            ]
        }

    monkeypatch.setattr(analyzer, "_post_json", fake_post_json)

    items = analyzer.analyze(build_flatlay_fixture())

    assert captured_payload["model"] == "gpt-4o"
    user_content = captured_payload["input"][1]["content"]
    assert user_content[1]["type"] == "input_image"
    assert user_content[1]["image_url"].startswith("data:image/png;base64,")
    assert [item.query for item in items] == ["블루 가디건", "실버 목걸이"]


def test_gemini_provider_uses_generate_content_payload(monkeypatch) -> None:
    analyzer = VisionOutfitAnalyzer(
        VisionOutfitAnalyzerConfig(
            enabled=True,
            provider="gemini",
            model_name="gemini-2.5-flash",
            api_key="gemini-key",
        )
    )
    captured: dict[str, object] = {}

    def fake_post_json(url: str, payload: dict[str, object], headers: dict[str, str]) -> dict[str, object]:
        captured["url"] = url
        captured["payload"] = payload
        captured["headers"] = headers
        return {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "text": '{"items":[{"category":"outer","color":"blue","item_label":"가디건","query":"블루 가디건"},{"category":"accessory","color":"gray","item_label":"목걸이","query":"그레이 목걸이"}]}'
                            }
                        ]
                    }
                }
            ]
        }

    monkeypatch.setattr(analyzer, "_post_json", fake_post_json)

    items = analyzer.analyze(build_flatlay_fixture())

    assert "generativelanguage.googleapis.com" in captured["url"]
    assert "gemini-2.5-flash:generateContent" in captured["url"]
    assert captured["headers"]["Content-Type"] == "application/json"
    parts = captured["payload"]["contents"][0]["parts"]
    assert parts[1]["inline_data"]["mime_type"] == "image/png"
    assert [item.query for item in items] == ["블루 가디건", "실버 목걸이"]


def test_ollama_provider_uses_chat_with_images_and_schema(monkeypatch) -> None:
    analyzer = VisionOutfitAnalyzer(
        VisionOutfitAnalyzerConfig(
            enabled=True,
            provider="ollama",
            model_name="gemma3:4b",
            api_base_url="http://127.0.0.1:11434/api/chat",
        )
    )
    captured: dict[str, object] = {}

    monkeypatch.setattr("src.services.vision_outfit_analyzer.ensure_local_provider_reachable", lambda *_args, **_kwargs: None)

    def fake_post_json(url: str, payload: dict[str, object], headers: dict[str, str]) -> dict[str, object]:
        captured["url"] = url
        captured["payload"] = payload
        captured["headers"] = headers
        return {
            "message": {
                "content": '{"items":[{"category":"outer","color":"blue","item_label":"가디건","query":"블루 가디건"},{"category":"accessory","color":"gray","item_label":"목걸이","query":"그레이 목걸이"}]}'
            }
        }

    monkeypatch.setattr(analyzer, "_post_json", fake_post_json)

    items = analyzer.analyze(build_flatlay_fixture())

    assert captured["url"] == "http://127.0.0.1:11434/api/chat"
    assert captured["headers"]["Content-Type"] == "application/json"
    assert captured["payload"]["model"] == "gemma3:4b"
    assert captured["payload"]["stream"] is False
    assert captured["payload"]["messages"][1]["images"][0]
    assert captured["payload"]["format"]["type"] == "object"
    assert [item.query for item in items] == ["블루 가디건", "실버 목걸이"]


def test_ollama_provider_normalizes_lightweight_model_item_labels(monkeypatch) -> None:
    analyzer = VisionOutfitAnalyzer(
        VisionOutfitAnalyzerConfig(
            enabled=True,
            provider="ollama",
            model_name="gemma3:4b",
            api_base_url="http://127.0.0.1:11434/api/chat",
        )
    )

    monkeypatch.setattr("src.services.vision_outfit_analyzer.ensure_local_provider_reachable", lambda *_args, **_kwargs: None)

    def fake_post_json(url: str, payload: dict[str, object], headers: dict[str, str]) -> dict[str, object]:
        return {
            "message": {
                "content": json.dumps(
                    {
                        "items": [
                            {
                                "category": "top",
                                "color": "white",
                                "item_label": "나시",
                                "query": "화이트 나시",
                            },
                            {
                                "category": "bottom",
                                "color": "blue",
                                "item_label": "청바지 팬츠",
                                "query": "청바지 팬츠",
                            },
                            {
                                "category": "accessory",
                                "color": "black",
                                "item_label": "선글라스",
                                "query": "검정 선글라스",
                            },
                        ]
                    },
                    ensure_ascii=False,
                )
            }
        }

    monkeypatch.setattr(analyzer, "_post_json", fake_post_json)

    items = analyzer.analyze(build_flatlay_fixture())

    assert [item.item_label for item in items] == ["슬리브리스 탑", "데님 팬츠", "안경"]
    assert [item.query for item in items] == ["화이트 슬리브리스 탑", "블루 데님 팬츠", "블랙 안경"]


def test_ollama_provider_normalizes_shoes_generic_label(monkeypatch) -> None:
    analyzer = VisionOutfitAnalyzer(
        VisionOutfitAnalyzerConfig(
            enabled=True,
            provider="ollama",
            model_name="gemma3:4b",
            api_base_url="http://127.0.0.1:11434/api/chat",
        )
    )

    monkeypatch.setattr("src.services.vision_outfit_analyzer.ensure_local_provider_reachable", lambda *_args, **_kwargs: None)

    def fake_post_json(url: str, payload: dict[str, object], headers: dict[str, str]) -> dict[str, object]:
        return {
            "message": {
                "content": json.dumps(
                    {
                        "items": [
                            {
                                "category": "shoes",
                                "color": "white",
                                "item_label": "운동화",
                                "query": "화이트 운동화",
                            }
                        ]
                    },
                    ensure_ascii=False,
                )
            }
        }

    monkeypatch.setattr(analyzer, "_post_json", fake_post_json)

    items = analyzer.analyze(build_flatlay_fixture())

    assert [(item.item_label, item.query) for item in items] == [("스니커즈", "화이트 스니커즈")]


def test_ollama_provider_normalizes_jewelry_labels_and_defaults_unknown_color_to_gray(monkeypatch) -> None:
    analyzer = VisionOutfitAnalyzer(
        VisionOutfitAnalyzerConfig(
            enabled=True,
            provider="ollama",
            model_name="gemma3:4b",
            api_base_url="http://127.0.0.1:11434/api/chat",
        )
    )

    monkeypatch.setattr("src.services.vision_outfit_analyzer.ensure_local_provider_reachable", lambda *_args, **_kwargs: None)

    def fake_post_json(url: str, payload: dict[str, object], headers: dict[str, str]) -> dict[str, object]:
        return {
            "message": {
                "content": json.dumps(
                    {
                        "items": [
                            {
                                "category": "accessory",
                                "color": "unknown",
                                "item_label": "체인 팔찌",
                                "query": "체인 팔찌",
                            },
                            {
                                "category": "accessory",
                                "color": "neutral",
                                "item_label": "반지",
                                "query": "반지",
                            },
                        ]
                    },
                    ensure_ascii=False,
                )
            }
        }

    monkeypatch.setattr(analyzer, "_post_json", fake_post_json)

    items = analyzer.analyze(build_flatlay_fixture())

    assert [(item.color, item.item_label, item.query) for item in items] == [
        ("gray", "팔찌", "실버 팔찌"),
        ("gray", "반지", "실버 반지"),
    ]


def test_model_output_normalizes_outer_variants_and_recategorizes_bag(monkeypatch) -> None:
    analyzer = VisionOutfitAnalyzer(
        VisionOutfitAnalyzerConfig(
            enabled=True,
            provider="ollama",
            model_name="gemma3:4b",
            api_base_url="http://127.0.0.1:11434/api/chat",
        )
    )

    monkeypatch.setattr("src.services.vision_outfit_analyzer.ensure_local_provider_reachable", lambda *_args, **_kwargs: None)

    def fake_post_json(url: str, payload: dict[str, object], headers: dict[str, str]) -> dict[str, object]:
        return {
            "message": {
                "content": json.dumps(
                    {
                        "items": [
                            {
                                "category": "outer",
                                "color": "black",
                                "item_label": "블랙 재킷",
                                "query": "블랙 재킷",
                            },
                            {
                                "category": "outer",
                                "color": "black",
                                "item_label": "점프수트",
                                "query": "블랙 점프수트",
                            },
                            {
                                "category": "outer",
                                "color": "brown",
                                "item_label": "가방",
                                "query": "브라운 가방",
                            },
                        ]
                    },
                    ensure_ascii=False,
                )
            }
        }

    monkeypatch.setattr(analyzer, "_post_json", fake_post_json)

    items = analyzer.analyze(build_flatlay_fixture())

    assert [(item.category, item.item_label, item.query) for item in items] == [
        ("outer", "자켓", "블랙 자켓"),
        ("outer", "원피스", "블랙 원피스"),
        ("bag", "가방", "브라운 가방"),
    ]


def test_settings_support_openai_vision_alias_names(monkeypatch) -> None:
    monkeypatch.delenv("VISION_OUTFIT_ANALYZER_ENABLED", raising=False)
    monkeypatch.delenv("VISION_OUTFIT_ANALYZER_PROVIDER", raising=False)
    monkeypatch.delenv("VISION_OUTFIT_ANALYZER_MODEL_NAME", raising=False)
    monkeypatch.delenv("VISION_OUTFIT_ANALYZER_MAX_IMAGE_BYTES", raising=False)
    monkeypatch.delenv("VISION_OUTFIT_ANALYZER_TIMEOUT_SECONDS", raising=False)
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_VISION_ENABLED", "true")
    monkeypatch.setenv("OPENAI_VISION_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_VISION_MODEL", "gpt-4o")
    monkeypatch.setenv("OPENAI_VISION_MAX_IMAGE_BYTES", "1234")
    monkeypatch.setenv("OPENAI_VISION_TIMEOUT_SECONDS", "9.5")

    settings = Settings(_env_file=None)

    assert settings.openai_api_key == "test-key"
    assert settings.vision_outfit_analyzer_enabled is True
    assert settings.vision_outfit_analyzer_provider == "openai"
    assert settings.vision_outfit_analyzer_model_name == "gpt-4o"
    assert settings.vision_outfit_analyzer_max_image_bytes == 1234
    assert settings.vision_outfit_analyzer_timeout_seconds == 9.5


def test_settings_support_gemini_alias_names(monkeypatch) -> None:
    monkeypatch.delenv("VISION_OUTFIT_ANALYZER_ENABLED", raising=False)
    monkeypatch.delenv("VISION_OUTFIT_ANALYZER_PROVIDER", raising=False)
    monkeypatch.delenv("VISION_OUTFIT_ANALYZER_MODEL_NAME", raising=False)
    monkeypatch.delenv("VISION_OUTFIT_ANALYZER_MAX_IMAGE_BYTES", raising=False)
    monkeypatch.delenv("VISION_OUTFIT_ANALYZER_TIMEOUT_SECONDS", raising=False)
    monkeypatch.delenv("OPENAI_VISION_ENABLED", raising=False)
    monkeypatch.delenv("OPENAI_VISION_PROVIDER", raising=False)
    monkeypatch.delenv("OPENAI_VISION_MODEL", raising=False)
    monkeypatch.delenv("OPENAI_VISION_MAX_IMAGE_BYTES", raising=False)
    monkeypatch.delenv("OPENAI_VISION_TIMEOUT_SECONDS", raising=False)
    monkeypatch.setenv("GEMINI_API_KEY", "gemini-key")
    monkeypatch.setenv("GEMINI_VISION_ENABLED", "true")
    monkeypatch.setenv("GEMINI_VISION_PROVIDER", "gemini")
    monkeypatch.setenv("GEMINI_VISION_MODEL", "gemini-2.5-flash")
    monkeypatch.setenv("GEMINI_VISION_MAX_IMAGE_BYTES", "4567")
    monkeypatch.setenv("GEMINI_VISION_TIMEOUT_SECONDS", "8.0")

    settings = Settings(_env_file=None)

    assert settings.gemini_api_key == "gemini-key"
    assert settings.vision_outfit_analyzer_enabled is True
    assert settings.vision_outfit_analyzer_provider == "gemini"
    assert settings.vision_outfit_analyzer_model_name == "gemini-2.5-flash"
    assert settings.vision_outfit_analyzer_max_image_bytes == 4567
    assert settings.vision_outfit_analyzer_timeout_seconds == 8.0


def test_settings_support_ollama_alias_names(monkeypatch) -> None:
    monkeypatch.delenv("VISION_OUTFIT_ANALYZER_ENABLED", raising=False)
    monkeypatch.delenv("VISION_OUTFIT_ANALYZER_PROVIDER", raising=False)
    monkeypatch.delenv("VISION_OUTFIT_ANALYZER_MODEL_NAME", raising=False)
    monkeypatch.delenv("VISION_OUTFIT_ANALYZER_MAX_IMAGE_BYTES", raising=False)
    monkeypatch.delenv("VISION_OUTFIT_ANALYZER_TIMEOUT_SECONDS", raising=False)
    monkeypatch.delenv("VISION_OUTFIT_ANALYZER_API_BASE_URL", raising=False)
    monkeypatch.delenv("OPENAI_VISION_ENABLED", raising=False)
    monkeypatch.delenv("OPENAI_VISION_PROVIDER", raising=False)
    monkeypatch.delenv("OPENAI_VISION_MODEL", raising=False)
    monkeypatch.delenv("OPENAI_VISION_MAX_IMAGE_BYTES", raising=False)
    monkeypatch.delenv("OPENAI_VISION_TIMEOUT_SECONDS", raising=False)
    monkeypatch.delenv("GEMINI_VISION_ENABLED", raising=False)
    monkeypatch.delenv("GEMINI_VISION_PROVIDER", raising=False)
    monkeypatch.delenv("GEMINI_VISION_MODEL", raising=False)
    monkeypatch.delenv("GEMINI_VISION_MAX_IMAGE_BYTES", raising=False)
    monkeypatch.delenv("GEMINI_VISION_TIMEOUT_SECONDS", raising=False)
    monkeypatch.setenv("OLLAMA_API_KEY", "ollama-key")
    monkeypatch.setenv("OLLAMA_VISION_ENABLED", "true")
    monkeypatch.setenv("OLLAMA_VISION_PROVIDER", "ollama")
    monkeypatch.setenv("OLLAMA_VISION_MODEL", "qwen2.5vl:7b")
    monkeypatch.setenv("OLLAMA_VISION_MAX_IMAGE_BYTES", "7654")
    monkeypatch.setenv("OLLAMA_VISION_TIMEOUT_SECONDS", "11.0")
    monkeypatch.setenv("OLLAMA_API_BASE_URL", "http://127.0.0.1:11434/api/chat")

    settings = Settings(_env_file=None)

    assert settings.ollama_api_key == "ollama-key"
    assert settings.vision_outfit_analyzer_enabled is True
    assert settings.vision_outfit_analyzer_provider == "ollama"
    assert settings.vision_outfit_analyzer_model_name == "qwen2.5vl:7b"
    assert settings.vision_outfit_analyzer_max_image_bytes == 7654
    assert settings.vision_outfit_analyzer_timeout_seconds == 11.0
    assert settings.vision_outfit_analyzer_api_base_url == "http://127.0.0.1:11434/api/chat"


def test_settings_support_gemini_correction_alias_name(monkeypatch) -> None:
    monkeypatch.setenv("GEMINI_CORRECTION_ENABLED", "false")

    settings = Settings(_env_file=None)

    assert settings.vision_outfit_analyzer_gemini_correction_enabled is False


def test_runtime_config_prefers_ollama_alias_over_stale_gemini_model(monkeypatch) -> None:
    monkeypatch.delenv("VISION_OUTFIT_ANALYZER_MODEL_NAME", raising=False)
    monkeypatch.setenv("GEMINI_VISION_MODEL", "gemini-2.5-flash")
    monkeypatch.setenv("OLLAMA_VISION_MODEL", "qwen2.5vl:7b")
    monkeypatch.setenv("OLLAMA_API_BASE_URL", "http://127.0.0.1:11434/api/chat")
    monkeypatch.setenv("OLLAMA_API_KEY", "ollama-key")

    settings = Settings(_env_file=None)
    runtime_config = resolve_vision_outfit_analyzer_runtime_config(settings, provider_override="ollama", env_values={})

    assert runtime_config["provider"] == "ollama"
    assert runtime_config["model_name"] == "qwen2.5vl:7b"
    assert runtime_config["api_base_url"] == "http://127.0.0.1:11434/api/chat"
    assert runtime_config["api_key"] == "ollama-key"


def test_runtime_config_uses_longer_default_timeout_for_ollama(monkeypatch) -> None:
    monkeypatch.delenv("VISION_OUTFIT_ANALYZER_TIMEOUT_SECONDS", raising=False)
    monkeypatch.delenv("OLLAMA_VISION_TIMEOUT_SECONDS", raising=False)

    settings = Settings(_env_file=None)
    runtime_config = resolve_vision_outfit_analyzer_runtime_config(settings, provider_override="ollama", env_values={})

    assert runtime_config["timeout_seconds"] == 90.0


def test_settings_support_recommendation_scoring_overrides(monkeypatch) -> None:
    monkeypatch.setenv("RECOMMENDATION_SCORE_ITEM_LABEL_MATCH_BONUS", "0.22")
    monkeypatch.setenv("RECOMMENDATION_SCORE_VISION_SIMILARITY_WEIGHT", "0.31")

    settings = Settings(_env_file=None)

    assert settings.recommendation_score_item_label_match_bonus == 0.22
    assert settings.recommendation_score_vision_similarity_weight == 0.31


def test_settings_support_naver_shopping_query_tuning_overrides(monkeypatch) -> None:
    monkeypatch.setenv("NAVER_SHOPPING_SORT", "date")
    monkeypatch.setenv("NAVER_SHOPPING_FILTER", "naverpay")
    monkeypatch.setenv("NAVER_SHOPPING_EXCLUDE", "used:rental:cbshop")

    settings = Settings(_env_file=None)

    assert settings.naver_shopping_sort == "date"
    assert settings.naver_shopping_filter == "naverpay"
    assert settings.naver_shopping_exclude == "used:rental:cbshop"


def test_runtime_config_prefers_provider_specific_timeout_when_provider_overridden(monkeypatch) -> None:
    monkeypatch.setenv("VISION_OUTFIT_ANALYZER_TIMEOUT_SECONDS", "20")
    monkeypatch.setenv("OLLAMA_VISION_TIMEOUT_SECONDS", "120")

    settings = Settings(_env_file=None)
    runtime_config = resolve_vision_outfit_analyzer_runtime_config(settings, provider_override="ollama", env_values={})

    assert runtime_config["timeout_seconds"] == 120.0


def test_runtime_config_prefers_provider_specific_model_for_current_ollama_provider(monkeypatch) -> None:
    monkeypatch.setenv("VISION_OUTFIT_ANALYZER_PROVIDER", "ollama")
    monkeypatch.setenv("VISION_OUTFIT_ANALYZER_MODEL_NAME", "gemini-2.5-flash")
    monkeypatch.setenv("OLLAMA_VISION_MODEL", "gemma3:4b")
    monkeypatch.setenv("OLLAMA_API_BASE_URL", "http://127.0.0.1:11434/api/chat")

    settings = Settings(_env_file=None)
    runtime_config = resolve_vision_outfit_analyzer_runtime_config(settings, env_values={})

    assert runtime_config["provider"] == "ollama"
    assert runtime_config["model_name"] == "gemma3:4b"
    assert runtime_config["api_base_url"] == "http://127.0.0.1:11434/api/chat"


def test_guess_mime_type_and_query_builder_cover_common_defaults() -> None:
    assert guess_mime_type(build_flatlay_fixture()) == "image/png"
    assert build_item_query(category="shoes", color="gray", item_label="스니커즈") == "그레이 스니커즈"
    assert build_item_query(category="shoes", color="gray", item_label="스니커즈", brand_hint="뉴발란스") == "뉴발란스 그레이 스니커즈"
    assert build_item_query(category="shoes", color="black", item_label="부츠", query_hint="블랙 가죽 부츠") == "블랙 가죽 부츠"
    assert build_item_query(category="bag", color="brown", item_label="숄더백", query_hint="브라운 스웨이드 숄더백") == "브라운 스웨이드 숄더백"
    assert build_item_query(category="top", color="brown", item_label="셔츠", query_hint="브라운 스트라이프 실크 셔츠") == "브라운 스트라이프 실크 셔츠"
    assert build_item_query(category="top", color="white", item_label="블라우스", query_hint="화이트 무지 실크 블라우스") == "화이트 민무늬 실크 블라우스"
    assert build_item_query(category="top", color="white", item_label="블라우스", query_hint="화이트 레이스 쉬폰 블라우스") == "화이트 레이스 쉬폰 블라우스"
    assert build_item_query(category="bag", color="brown", item_label="숄더백", query_hint="브라운 체크 가죽 숄더백") == "브라운 체크 가죽 숄더백"
    assert build_item_query(category="outer", color="brown", item_label="자켓", query_hint="브라운 트위드 자켓") == "브라운 트위드 자켓"
    assert build_item_query(category="accessory", color="gray", item_label="목걸이") == "실버 목걸이"
    assert build_item_query(category="accessory", color="black", item_label="안경", query_hint="블랙 메탈 안경테") == "블랙 메탈 안경"
    assert build_item_query(category="accessory", color="white", item_label="귀걸이", query_hint="화이트 진주 귀걸이") == "화이트 진주 귀걸이"
    assert build_item_query(category="outer", color="black", item_label="자켓", query_hint="가죽 재킷") == "블랙 가죽 자켓"
    assert build_item_query(category="outer", color="black", item_label="레더 자켓", query_hint="블랙 가죽 재킷") == "블랙 레더 자켓"
    assert build_item_query(category="bottom", color="black", item_label="미니 스커트", query_hint="검은색 도트 미니 스커트") == "블랙 도트 미니 스커트"


def test_model_output_normalizes_denim_and_stripe_labels() -> None:
    analyzer = VisionOutfitAnalyzer(VisionOutfitAnalyzerConfig(enabled=True, provider="mock"))

    items = analyzer.coerce_detected_items(
        {
            "items": [
                {
                    "category": "top",
                    "color": "blue",
                    "item_label": "네이비 스트라이프 스웨터",
                    "query": "네이비 스트라이프 스웨터",
                },
                {
                    "category": "bottom",
                    "color": "navy",
                    "item_label": "와이드 팬츠",
                    "query": "네이비 와이드 팬츠",
                },
                {
                    "category": "bottom",
                    "color": "blue",
                    "item_label": "와이드 데님 팬츠",
                    "query": "블루 와이드 데님 팬츠",
                },
                {
                    "category": "bottom",
                    "color": "black",
                    "item_label": "검은색 도트 미니 스커트",
                    "query": "검은색 도트 미니 스커트",
                },
            ]
        }
    )

    assert [(item.category, item.color, item.item_label, item.query) for item in items] == [
        ("top", "navy", "스트라이프 니트 탑", "네이비 스트라이프 니트 탑"),
        ("bottom", "navy", "와이드 데님 팬츠", "네이비 와이드 데님 팬츠"),
        ("bottom", "blue", "와이드 데님 팬츠", "블루 와이드 데님 팬츠"),
        ("bottom", "black", "미니 스커트", "블랙 도트 미니 스커트"),
    ]


def test_model_output_preserves_pattern_and_material_descriptor_order() -> None:
    analyzer = VisionOutfitAnalyzer(VisionOutfitAnalyzerConfig(enabled=True, provider="mock"))

    items = analyzer.coerce_detected_items(
        {
            "items": [
                {
                    "category": "shoes",
                    "color": "gray",
                    "item_label": "운동화",
                    "query": "뉴발란스 그레이 운동화",
                    "brand": "new balance",
                },
                {
                    "category": "top",
                    "color": "brown",
                    "item_label": "실크 블라우스",
                    "query": "브라운 스트라이프 실크 블라우스",
                },
                {
                    "category": "bag",
                    "color": "brown",
                    "item_label": "가방",
                    "query": "브라운 체크 가죽 가방",
                },
                {
                    "category": "top",
                    "color": "white",
                    "item_label": "블라우스",
                    "query": "화이트 무지 실크 블라우스",
                },
                {
                    "category": "top",
                    "color": "white",
                    "item_label": "블라우스",
                    "query": "화이트 레이스 쉬폰 블라우스",
                },
                {
                    "category": "outer",
                    "color": "brown",
                    "item_label": "자켓",
                    "query": "브라운 트위드 자켓",
                },
            ]
        }
    )

    assert [(item.category, item.color, item.item_label, item.query) for item in items] == [
        ("shoes", "gray", "스니커즈", "뉴발란스 그레이 스니커즈"),
        ("top", "brown", "블라우스", "브라운 스트라이프 실크 블라우스"),
        ("bag", "brown", "가방", "브라운 체크 가죽 가방"),
        ("top", "white", "블라우스", "화이트 민무늬 실크 블라우스"),
        ("top", "white", "블라우스", "화이트 레이스 쉬폰 블라우스"),
        ("outer", "brown", "자켓", "브라운 트위드 자켓"),
    ]
    assert items[0].brand == "뉴발란스"


def test_model_output_preserves_accessory_descriptors_and_filters_noise_labels() -> None:
    analyzer = VisionOutfitAnalyzer(VisionOutfitAnalyzerConfig(enabled=True, provider="mock"))

    items = analyzer.coerce_detected_items(
        {
            "items": [
                {
                    "category": "accessory",
                    "color": "black",
                    "item_label": "메탈 안경테",
                    "query": "블랙 메탈 안경테",
                },
                {
                    "category": "accessory",
                    "color": "unknown",
                    "item_label": "진주 귀걸이",
                    "query": "진주 귀걸이",
                },
                {
                    "category": "accessory",
                    "color": "white",
                    "item_label": "화이트 칼라",
                    "query": "화이트 칼라",
                },
            ]
        }
    )

    assert [(item.category, item.color, item.item_label, item.query) for item in items] == [
        ("accessory", "black", "안경", "블랙 메탈 안경"),
        ("accessory", "white", "귀걸이", "화이트 진주 귀걸이"),
    ]
