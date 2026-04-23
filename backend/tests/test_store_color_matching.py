from __future__ import annotations

from pathlib import Path

from src.services.store import InMemoryStore, ProductRecord


def make_product(product_id: str, product_name: str, feature_vector: tuple[float, ...] = (0.9, 0.9, 0.9, 0.9)) -> ProductRecord:
    return ProductRecord(
        id=product_id,
        source="naver",
        product_name=product_name,
        category="shoes",
        price=39000,
        product_url=f"https://example.com/{product_id}",
        image_url=f"https://example.com/{product_id}.jpg",
        dominant_tone="neutral",
        style_mood="minimal",
        silhouette="balanced",
        feature_vector=feature_vector,
    )


def test_color_keyword_bonus_promotes_visually_matching_name(tmp_path: Path) -> None:
    store = InMemoryStore(wishlist_store_path=tmp_path / "wishlist.json")
    upload = store.create_upload(
        user_id="local-user",
        filename="outfit.png",
        content_type="image/png",
        size_bytes=10,
        content=b"not-a-real-image",
    )
    upload.analysis.dominant_color = "black"
    upload.analysis.feature_vector = (0.9, 0.9, 0.9, 0.9)

    items = store.list_recommendations(
        uploaded_image_id=upload.id,
        category="shoes",
        min_price=None,
        max_price=None,
        sort="similarity_desc",
        limit=2,
        candidate_products=[
            make_product("black-maryjane", "블랙 메리제인 슈즈"),
            make_product("white-maryjane", "화이트 메리제인 슈즈"),
        ],
    )

    assert items[0]["product_id"] == "black-maryjane"
    assert items[0]["score_breakdown"]["color_bonus"] == 0.08
    assert items[1]["score_breakdown"]["color_bonus"] == 0.0


def test_rgb_color_classifier_maps_common_outfit_colors(tmp_path: Path) -> None:
    store = InMemoryStore(wishlist_store_path=tmp_path / "wishlist.json")

    assert store._classify_rgb_color(12, 12, 12) == "black"
    assert store._classify_rgb_color(248, 247, 244) == "white"
    assert store._classify_rgb_color(211, 189, 154) == "beige"
    assert store._classify_rgb_color(42, 59, 110) == "navy"
