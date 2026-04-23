from __future__ import annotations

from pathlib import Path

from src.services.store import InMemoryStore, ProductRecord


def make_product(
    product_id: str,
    product_name: str,
    feature_vector: tuple[float, ...] = (0.9, 0.9, 0.9, 0.9),
    dominant_color: str = "unknown",
) -> ProductRecord:
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
        dominant_color=dominant_color,
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


def test_product_image_color_bonus_promotes_visually_matching_image(tmp_path: Path) -> None:
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
            make_product("image-black", "메리제인 슈즈", dominant_color="black"),
            make_product("image-white", "메리제인 슈즈", dominant_color="white"),
        ],
    )

    assert items[0]["product_id"] == "image-black"
    assert items[0]["score_breakdown"]["product_image_color_bonus"] == 0.12
    assert items[0]["matched_signals"]["product_dominant_color"] == "black"
    assert items[1]["score_breakdown"]["product_image_color_bonus"] == 0.0


def test_category_query_hint_color_drives_category_specific_color_bonus(tmp_path: Path) -> None:
    store = InMemoryStore(wishlist_store_path=tmp_path / "wishlist.json")
    upload = store.create_upload(
        user_id="local-user",
        filename="outfit.png",
        content_type="image/png",
        size_bytes=10,
        content=b"not-a-real-image",
    )
    upload.analysis.dominant_color = "beige"
    upload.analysis.category_query_hints = {"outer": "블랙 니트 베스트"}
    upload.analysis.feature_vector = (0.9, 0.9, 0.9, 0.9)

    items = store.list_recommendations(
        uploaded_image_id=upload.id,
        category="outer",
        min_price=None,
        max_price=None,
        sort="similarity_desc",
        limit=2,
        candidate_products=[
            ProductRecord(
                id="black-vest",
                source="naver",
                product_name="니트 베스트",
                category="outer",
                price=39000,
                product_url="https://example.com/black-vest",
                image_url="https://example.com/black-vest.jpg",
                dominant_tone="neutral",
                style_mood="minimal",
                silhouette="balanced",
                feature_vector=(0.9, 0.9, 0.9, 0.9),
                dominant_color="black",
            ),
            ProductRecord(
                id="beige-vest",
                source="naver",
                product_name="니트 베스트",
                category="outer",
                price=39000,
                product_url="https://example.com/beige-vest",
                image_url="https://example.com/beige-vest.jpg",
                dominant_tone="neutral",
                style_mood="minimal",
                silhouette="balanced",
                feature_vector=(0.9, 0.9, 0.9, 0.9),
                dominant_color="beige",
            ),
        ],
    )

    assert items[0]["product_id"] == "black-vest"
    assert items[0]["matched_signals"]["category_target_color"] == "black"
    assert items[0]["score_breakdown"]["product_image_color_bonus"] == 0.12
    assert items[1]["score_breakdown"]["product_image_color_bonus"] == 0.0


def test_rgb_color_classifier_maps_common_outfit_colors(tmp_path: Path) -> None:
    store = InMemoryStore(wishlist_store_path=tmp_path / "wishlist.json")

    assert store._classify_rgb_color(12, 12, 12) == "black"
    assert store._classify_rgb_color(248, 247, 244) == "white"
    assert store._classify_rgb_color(211, 189, 154) == "beige"
    assert store._classify_rgb_color(42, 59, 110) == "navy"
