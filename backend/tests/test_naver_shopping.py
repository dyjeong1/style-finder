from __future__ import annotations

from src.services.naver_shopping import NaverShoppingClient, NaverShoppingConfig, build_naver_query
from src.services.store import UploadAnalysis


def test_naver_shopping_client_disabled_without_credentials() -> None:
    client = NaverShoppingClient(NaverShoppingConfig(client_id=None, client_secret=None))

    assert client.search_products(query="미니멀 상의", category="top", limit=3) == []


def test_naver_shopping_item_parse_strips_html_and_maps_fields() -> None:
    client = NaverShoppingClient(NaverShoppingConfig(client_id="id", client_secret="secret"))

    product = client._parse_item(
        {
            "title": "<b>오버핏</b> 셔츠",
            "link": "https://smartstore.naver.com/demo/products/1",
            "image": "https://shopping-phinf.pstatic.net/main_1.jpg",
            "lprice": "29000",
            "productId": "12345",
            "category1": "패션의류",
            "category2": "여성의류",
            "category3": "셔츠",
        },
        category_hint=None,
    )

    assert product is not None
    assert product.id == "naver-12345"
    assert product.source == "naver"
    assert product.product_name == "오버핏 셔츠"
    assert product.product_url.startswith("https://smartstore.naver.com")
    assert product.image_url.startswith("https://shopping-phinf.pstatic.net")
    assert product.price == 29000
    assert product.category == "top"


def test_build_naver_query_uses_analysis_and_category() -> None:
    analysis = UploadAnalysis(
        checksum="abc",
        dominant_tone="cool",
        style_mood="minimal",
        silhouette="relaxed",
        preferred_categories=("outer",),
        feature_vector=(0.1, 0.2, 0.3, 0.4),
    )

    assert build_naver_query(analysis, "bag") == "쿨톤 미니멀 가방"
    assert build_naver_query(analysis, None) == "쿨톤 미니멀 아우터"
