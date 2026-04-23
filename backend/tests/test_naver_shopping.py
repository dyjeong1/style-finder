from __future__ import annotations

from io import BytesIO
from urllib.error import HTTPError

import pytest

from src.services.naver_shopping import (
    CATEGORY_ORDER,
    NaverShoppingClient,
    NaverShoppingConfig,
    build_custom_naver_category_queries,
    build_custom_naver_query,
    build_naver_category_queries,
    build_naver_query,
    infer_custom_query_categories,
)
from src.services.store import UploadAnalysis


def test_naver_shopping_client_disabled_without_credentials() -> None:
    client = NaverShoppingClient(NaverShoppingConfig(client_id=None, client_secret=None))

    assert client.search_products(query="미니멀 상의", category="top", limit=3) == []

    result = client.search(query="미니멀 상의", category="top", limit=3)
    assert result.products == []
    assert result.fallback_reason == "credentials_missing"


def test_naver_shopping_client_reports_auth_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    client = NaverShoppingClient(NaverShoppingConfig(client_id="id", client_secret="secret"))
    error_body = b'{"errorMessage":"NID AUTH Result Invalid (1000) : Authentication failed.","errorCode":"024"}'

    def raise_http_error(*_: object, **__: object) -> None:
        raise HTTPError(
            url="https://openapi.naver.com/v1/search/shop.json",
            code=401,
            msg="Unauthorized",
            hdrs={},
            fp=BytesIO(error_body),
        )

    monkeypatch.setattr("src.services.naver_shopping.urlopen", raise_http_error)

    result = client.search(query="미니멀 상의", category="top", limit=3)

    assert result.products == []
    assert result.fallback_reason == "auth_failed"
    assert "네이버 쇼핑 API 인증에 실패" in (result.fallback_message or "")
    assert "Authentication failed" in (result.fallback_message or "")


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


def test_build_naver_category_queries_covers_all_recommendation_categories() -> None:
    analysis = UploadAnalysis(
        checksum="abc",
        dominant_tone="neutral",
        style_mood="feminine",
        silhouette="layered",
        preferred_categories=("bag",),
        feature_vector=(0.1, 0.2, 0.3, 0.4),
    )

    queries = build_naver_category_queries(analysis)

    assert [category for category, _ in queries] == list(CATEGORY_ORDER)
    assert queries == [
        ("top", "뉴트럴 페미닌 상의"),
        ("bottom", "뉴트럴 페미닌 하의"),
        ("outer", "뉴트럴 페미닌 아우터"),
        ("shoes", "뉴트럴 페미닌 신발"),
        ("bag", "뉴트럴 페미닌 가방"),
    ]


def test_build_custom_naver_query_appends_category_when_missing() -> None:
    assert build_custom_naver_query("블랙 미니멀", "outer") == "블랙 미니멀 아우터"
    assert build_custom_naver_query("블랙 미니멀 아우터", "outer") == "블랙 미니멀 아우터"
    assert build_custom_naver_query("  블랙   미니멀  ", None) == "블랙 미니멀"


def test_build_custom_naver_category_queries_covers_all_recommendation_categories() -> None:
    queries = build_custom_naver_category_queries("블랙 미니멀")

    assert [category for category, _ in queries] == list(CATEGORY_ORDER)
    assert queries == [
        ("top", "블랙 미니멀 상의"),
        ("bottom", "블랙 미니멀 하의"),
        ("outer", "블랙 미니멀 아우터"),
        ("shoes", "블랙 미니멀 신발"),
        ("bag", "블랙 미니멀 가방"),
    ]


def test_infer_custom_query_categories_detects_product_group_keywords() -> None:
    assert infer_custom_query_categories("검은색 신발") == ["shoes"]
    assert infer_custom_query_categories("블랙 메리제인") == ["shoes"]
    assert infer_custom_query_categories("브라운 로퍼") == ["shoes"]
    assert infer_custom_query_categories("여름 슬리퍼") == ["shoes"]
    assert infer_custom_query_categories("미니멀 구두") == ["shoes"]
    assert infer_custom_query_categories("미니멀 재킷과 토트백") == ["outer", "bag"]
    assert infer_custom_query_categories("블랙 미니멀") == []


def test_build_custom_naver_category_queries_limits_to_explicit_product_group() -> None:
    assert build_custom_naver_category_queries("검은색 신발") == [("shoes", "검은색 신발")]
    assert build_custom_naver_category_queries("블랙 메리제인") == [("shoes", "블랙 메리제인 신발")]
    assert build_custom_naver_category_queries("미니멀 재킷과 토트백") == [
        ("outer", "미니멀 재킷과 토트백 아우터"),
        ("bag", "미니멀 재킷과 토트백 가방"),
    ]
