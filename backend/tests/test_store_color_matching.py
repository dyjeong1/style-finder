from __future__ import annotations

from pathlib import Path

from src.services.image_analysis import DetectedOutfitItem
from src.services.store import InMemoryStore, ProductRecord, RecommendationScoringConfig


def make_product(
    product_id: str,
    product_name: str,
    category: str = "shoes",
    feature_vector: tuple[float, ...] = (0.9, 0.9, 0.9, 0.9),
    dominant_color: str = "unknown",
) -> ProductRecord:
    return ProductRecord(
        id=product_id,
        source="naver",
        product_name=product_name,
        category=category,
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


def test_vision_similarity_bonus_promotes_matching_product(tmp_path: Path) -> None:
    store = InMemoryStore(wishlist_store_path=tmp_path / "wishlist.json")
    upload = store.create_upload(
        user_id="local-user",
        filename="outfit.png",
        content_type="image/png",
        size_bytes=10,
        content=b"not-a-real-image",
    )
    upload.analysis.feature_vector = (0.9, 0.9, 0.9, 0.9)

    items = store.list_recommendations(
        uploaded_image_id=upload.id,
        category="shoes",
        min_price=None,
        max_price=None,
        sort="similarity_desc",
        limit=2,
        candidate_products=[
            make_product("vision-high", "메리제인 슈즈"),
            make_product("vision-low", "메리제인 슈즈"),
        ],
        vision_similarity_by_product={
            "vision-high": 0.9,
            "vision-low": 0.1,
        },
    )

    assert items[0]["product_id"] == "vision-high"
    assert items[0]["score_breakdown"]["vision_similarity"] == 0.9
    assert items[0]["score_breakdown"]["vision_bonus"] > items[1]["score_breakdown"]["vision_bonus"]


def test_item_label_bonus_promotes_specific_product_name_match(tmp_path: Path) -> None:
    store = InMemoryStore(
        wishlist_store_path=tmp_path / "wishlist.json",
        recommendation_scoring=RecommendationScoringConfig(item_label_match_bonus=0.14),
    )
    upload = store.create_upload(
        user_id="local-user",
        filename="outfit.png",
        content_type="image/png",
        size_bytes=10,
        content=b"not-a-real-image",
    )
    upload.analysis.feature_vector = (0.9, 0.9, 0.9, 0.9)
    upload.analysis.preferred_categories = ("shoes",)
    upload.analysis.detected_items = (
        DetectedOutfitItem(category="shoes", color="brown", item_label="메리제인 슈즈", query="브라운 메리제인 슈즈"),
    )
    upload.analysis.category_query_hints = {"shoes": "브라운 메리제인 슈즈"}

    items = store.list_recommendations(
        uploaded_image_id=upload.id,
        category="shoes",
        min_price=None,
        max_price=None,
        sort="similarity_desc",
        limit=2,
        candidate_products=[
            make_product("maryjane", "메리제인 슈즈"),
            make_product("flat", "플랫 슈즈"),
        ],
    )

    assert items[0]["product_id"] == "maryjane"
    assert items[0]["score_breakdown"]["item_label_bonus"] == 0.14
    assert items[0]["matched_signals"]["target_item_label"] == "메리제인 슈즈"
    assert items[1]["score_breakdown"]["item_label_bonus"] == 0.0


def test_item_label_bonus_rewards_family_and_descriptor_alignment_when_exact_label_differs(tmp_path: Path) -> None:
    store = InMemoryStore(
        wishlist_store_path=tmp_path / "wishlist.json",
        recommendation_scoring=RecommendationScoringConfig(item_label_match_bonus=0.1),
    )
    upload = store.create_upload(
        user_id="local-user",
        filename="outfit.png",
        content_type="image/png",
        size_bytes=10,
        content=b"not-a-real-image",
    )
    upload.analysis.feature_vector = (0.9, 0.9, 0.9, 0.9)
    upload.analysis.preferred_categories = ("bag",)
    upload.analysis.detected_items = (
        DetectedOutfitItem(category="bag", color="black", item_label="숄더백", query="블랙 가죽 숄더백"),
    )
    upload.analysis.category_query_hints = {"bag": "블랙 가죽 숄더백"}

    items = store.list_recommendations(
        uploaded_image_id=upload.id,
        category="bag",
        min_price=None,
        max_price=None,
        sort="similarity_desc",
        limit=2,
        candidate_products=[
            make_product("hobo", "블랙 가죽 호보백", category="bag"),
            make_product("canvas", "블랙 캔버스 토트백", category="bag"),
        ],
    )

    assert items[0]["product_id"] == "hobo"
    assert items[0]["score_breakdown"]["item_label_bonus"] > items[1]["score_breakdown"]["item_label_bonus"]


def test_vision_similarity_weight_can_be_tuned_independently(tmp_path: Path) -> None:
    store = InMemoryStore(
        wishlist_store_path=tmp_path / "wishlist.json",
        recommendation_scoring=RecommendationScoringConfig(
            item_label_match_bonus=0.0,
            vision_similarity_weight=0.0,
        ),
    )
    upload = store.create_upload(
        user_id="local-user",
        filename="outfit.png",
        content_type="image/png",
        size_bytes=10,
        content=b"not-a-real-image",
    )
    upload.analysis.feature_vector = (0.9, 0.9, 0.9, 0.9)

    items = store.list_recommendations(
        uploaded_image_id=upload.id,
        category="shoes",
        min_price=None,
        max_price=None,
        sort="similarity_desc",
        limit=2,
        candidate_products=[
            make_product("vision-high-zero", "기본 슈즈"),
            make_product("vision-low-zero", "기본 슈즈"),
        ],
        vision_similarity_by_product={
            "vision-high-zero": 0.9,
            "vision-low-zero": 0.1,
        },
    )

    assert items[0]["score_breakdown"]["vision_bonus"] == 0.0
    assert items[1]["score_breakdown"]["vision_bonus"] == 0.0
    assert items[0]["similarity_score"] == items[1]["similarity_score"]


def test_intent_keyword_bonus_preserves_model_query_intent_synonyms(tmp_path: Path) -> None:
    store = InMemoryStore(
        wishlist_store_path=tmp_path / "wishlist.json",
        recommendation_scoring=RecommendationScoringConfig(item_label_match_bonus=0.12),
    )
    upload = store.create_upload(
        user_id="local-user",
        filename="outfit.png",
        content_type="image/png",
        size_bytes=10,
        content=b"not-a-real-image",
    )
    upload.analysis.feature_vector = (0.9, 0.9, 0.9, 0.9)
    upload.analysis.preferred_categories = ("top",)
    upload.analysis.detected_items = (
        DetectedOutfitItem(category="top", color="navy", item_label="티셔츠", query="남색 롱슬리브 티셔츠"),
    )
    upload.analysis.category_query_hints = {"top": "남색 롱슬리브 티셔츠"}

    items = store.list_recommendations(
        uploaded_image_id=upload.id,
        category="top",
        min_price=None,
        max_price=None,
        sort="similarity_desc",
        limit=2,
        candidate_products=[
            ProductRecord(
                id="long-sleeve-top",
                source="naver",
                product_name="네이비 긴팔 티셔츠",
                category="top",
                price=32000,
                product_url="https://example.com/long-sleeve-top",
                image_url="https://example.com/long-sleeve-top.jpg",
                dominant_tone="cool",
                style_mood="minimal",
                silhouette="slim",
                feature_vector=(0.9, 0.9, 0.9, 0.9),
                dominant_color="navy",
            ),
            ProductRecord(
                id="short-sleeve-top",
                source="naver",
                product_name="네이비 반팔 티셔츠",
                category="top",
                price=32000,
                product_url="https://example.com/short-sleeve-top",
                image_url="https://example.com/short-sleeve-top.jpg",
                dominant_tone="cool",
                style_mood="minimal",
                silhouette="slim",
                feature_vector=(0.9, 0.9, 0.9, 0.9),
                dominant_color="navy",
            ),
        ],
    )

    assert items[0]["product_id"] == "long-sleeve-top"
    assert items[0]["score_breakdown"]["item_label_bonus"] == 0.12
    assert items[0]["matched_signals"]["target_intent_keywords"] == ["긴팔"]
    assert items[1]["score_breakdown"]["item_label_bonus"] == 0.0


def test_rgb_color_classifier_maps_common_outfit_colors(tmp_path: Path) -> None:
    store = InMemoryStore(wishlist_store_path=tmp_path / "wishlist.json")

    assert store._classify_rgb_color(12, 12, 12) == "black"
    assert store._classify_rgb_color(248, 247, 244) == "white"
    assert store._classify_rgb_color(211, 189, 154) == "beige"
    assert store._classify_rgb_color(42, 59, 110) == "navy"


def test_registered_products_do_not_leak_into_default_recommendation_fallback(tmp_path: Path) -> None:
    store = InMemoryStore(wishlist_store_path=tmp_path / "wishlist.json")
    upload = store.create_upload(
        user_id="local-user",
        filename="outfit.png",
        content_type="image/png",
        size_bytes=10,
        content=b"not-a-real-image",
    )

    leaked_product = ProductRecord(
        id="naver-top-999",
        source="naver",
        product_name="이전 업로드 전용 상품",
        category="top",
        price=99000,
        product_url="https://example.com/naver-top-999",
        image_url="https://example.com/naver-top-999.jpg",
        dominant_tone="cool",
        style_mood="minimal",
        silhouette="balanced",
        feature_vector=(0.9, 0.9, 0.9, 0.9),
    )
    store.register_products([leaked_product])

    items = store.list_recommendations(
        uploaded_image_id=upload.id,
        category=None,
        min_price=None,
        max_price=None,
        sort="similarity_desc",
        limit=20,
        candidate_products=None,
    )

    assert all(item["product_id"] != "naver-top-999" for item in items)


def test_detected_accessory_category_survives_overall_limit(tmp_path: Path) -> None:
    store = InMemoryStore(wishlist_store_path=tmp_path / "wishlist.json")
    upload = store.create_upload(
        user_id="local-user",
        filename="outfit.png",
        content_type="image/png",
        size_bytes=10,
        content=b"not-a-real-image",
    )
    upload.analysis.feature_vector = (0.9, 0.9, 0.9, 0.9)
    upload.analysis.preferred_categories = ("top", "bottom", "accessory")
    upload.analysis.category_query_hints = {
        "top": "그레이 니트 탑",
        "bottom": "화이트 미니 스커트",
        "accessory": "그레이 악세서리",
    }
    upload.analysis.detected_items = (
        DetectedOutfitItem(category="top", color="gray", item_label="니트 탑", query="그레이 니트 탑"),
        DetectedOutfitItem(category="bottom", color="white", item_label="미니 스커트", query="화이트 미니 스커트"),
        DetectedOutfitItem(category="accessory", color="gray", item_label="악세서리", query="그레이 악세서리"),
    )

    items = store.list_recommendations(
        uploaded_image_id=upload.id,
        category=None,
        min_price=None,
        max_price=None,
        sort="similarity_desc",
        limit=3,
        candidate_products=[
            make_product("top-1", "그레이 니트 탑", category="top", feature_vector=(0.9, 0.9, 0.9, 0.9)),
            make_product("bottom-1", "화이트 미니 스커트", category="bottom", feature_vector=(0.89, 0.89, 0.89, 0.89)),
            make_product("outer-1", "네이비 가디건", category="outer", feature_vector=(0.88, 0.88, 0.88, 0.88)),
            make_product("accessory-1", "그레이 헤어핀", category="accessory", feature_vector=(0.1, 0.1, 0.1, 0.1)),
        ],
    )

    assert [item["product_id"] for item in items] == ["top-1", "bottom-1", "accessory-1"]
    assert [item["category"] for item in items] == ["top", "bottom", "accessory"]
    assert all(item["product_id"] != "outer-1" for item in items)
