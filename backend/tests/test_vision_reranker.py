from __future__ import annotations

from io import BytesIO

from PIL import Image

from src.services.store import ProductRecord
from src.services.vision_reranker import VisionReranker, VisionRerankerConfig


def _make_image_bytes(color: tuple[int, int, int]) -> bytes:
    image = Image.new("RGB", (24, 24), color)
    output = BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()


def _make_product(product_id: str) -> ProductRecord:
    return ProductRecord(
        id=product_id,
        source="naver",
        product_name=f"{product_id} 상품",
        category="top",
        price=10000,
        product_url=f"https://example.com/{product_id}",
        image_url=f"https://example.com/{product_id}.png",
        dominant_tone="neutral",
        style_mood="minimal",
        silhouette="balanced",
        feature_vector=(0.1, 0.2, 0.3, 0.4),
    )


def test_vision_reranker_returns_empty_when_disabled() -> None:
    reranker = VisionReranker(VisionRerankerConfig(enabled=False))

    scores = reranker.score_products(_make_image_bytes((255, 255, 255)), [_make_product("demo")])

    assert scores == {}


def test_vision_reranker_uses_runtime_when_available(monkeypatch) -> None:
    reranker = VisionReranker(VisionRerankerConfig(enabled=True, max_candidates=2))

    class FakeRuntime:
        def compute_image_similarities(self, images: list[object]) -> list[float]:
            assert len(images) == 3
            return [0.88, 0.41]

    monkeypatch.setattr("src.services.vision_reranker._load_clip_runtime", lambda _model_name: FakeRuntime())
    monkeypatch.setattr(reranker, "_load_remote_image", lambda _image_url: Image.new("RGB", (24, 24), (0, 0, 0)))

    scores = reranker.score_products(
        _make_image_bytes((255, 255, 255)),
        [_make_product("first"), _make_product("second"), _make_product("ignored")],
    )

    assert scores == {
        "first": 0.88,
        "second": 0.41,
    }
