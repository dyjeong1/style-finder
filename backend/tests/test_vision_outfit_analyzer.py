from __future__ import annotations

from io import BytesIO

from PIL import Image, ImageDraw

from src.core.config import Settings, resolve_vision_outfit_analyzer_runtime_config
from src.services.image_analysis import DetectedOutfitItem
from src.services.store import InMemoryStore
from src.services.vision_outfit_analyzer import (
    VisionOutfitAnalyzer,
    VisionOutfitAnalyzerConfig,
    build_item_query,
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
    assert [item.query for item in items] == ["블루 가디건", "그레이 목걸이"]


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
    assert [item.query for item in items] == ["블루 가디건", "그레이 목걸이"]


def test_ollama_provider_uses_chat_with_images_and_schema(monkeypatch) -> None:
    analyzer = VisionOutfitAnalyzer(
        VisionOutfitAnalyzerConfig(
            enabled=True,
            provider="ollama",
            model_name="qwen2.5vl:7b",
            api_base_url="http://127.0.0.1:11434/api/chat",
        )
    )
    captured: dict[str, object] = {}

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
    assert captured["payload"]["model"] == "qwen2.5vl:7b"
    assert captured["payload"]["stream"] is False
    assert captured["payload"]["messages"][1]["images"][0]
    assert captured["payload"]["format"]["type"] == "object"
    assert [item.query for item in items] == ["블루 가디건", "그레이 목걸이"]


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


def test_runtime_config_prefers_ollama_alias_over_stale_gemini_model(monkeypatch) -> None:
    monkeypatch.delenv("VISION_OUTFIT_ANALYZER_MODEL_NAME", raising=False)
    monkeypatch.setenv("GEMINI_VISION_MODEL", "gemini-2.5-flash")
    monkeypatch.setenv("OLLAMA_VISION_MODEL", "qwen2.5vl:7b")
    monkeypatch.setenv("OLLAMA_API_BASE_URL", "http://127.0.0.1:11434/api/chat")
    monkeypatch.setenv("OLLAMA_API_KEY", "ollama-key")

    settings = Settings(_env_file=None)
    runtime_config = resolve_vision_outfit_analyzer_runtime_config(settings, provider_override="ollama")

    assert runtime_config["provider"] == "ollama"
    assert runtime_config["model_name"] == "qwen2.5vl:7b"
    assert runtime_config["api_base_url"] == "http://127.0.0.1:11434/api/chat"
    assert runtime_config["api_key"] == "ollama-key"


def test_runtime_config_uses_longer_default_timeout_for_ollama(monkeypatch) -> None:
    monkeypatch.delenv("VISION_OUTFIT_ANALYZER_TIMEOUT_SECONDS", raising=False)
    monkeypatch.delenv("OLLAMA_VISION_TIMEOUT_SECONDS", raising=False)

    settings = Settings(_env_file=None)
    runtime_config = resolve_vision_outfit_analyzer_runtime_config(settings, provider_override="ollama")

    assert runtime_config["timeout_seconds"] == 90.0


def test_runtime_config_prefers_provider_specific_timeout_when_provider_overridden(monkeypatch) -> None:
    monkeypatch.setenv("VISION_OUTFIT_ANALYZER_TIMEOUT_SECONDS", "20")
    monkeypatch.setenv("OLLAMA_VISION_TIMEOUT_SECONDS", "120")

    settings = Settings(_env_file=None)
    runtime_config = resolve_vision_outfit_analyzer_runtime_config(settings, provider_override="ollama")

    assert runtime_config["timeout_seconds"] == 120.0


def test_guess_mime_type_and_query_builder_cover_common_defaults() -> None:
    assert guess_mime_type(build_flatlay_fixture()) == "image/png"
    assert build_item_query(category="shoes", color="gray", item_label="스니커즈") == "그레이 스니커즈"
