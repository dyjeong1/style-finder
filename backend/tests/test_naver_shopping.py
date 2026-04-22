from __future__ import annotations

from io import BytesIO
from urllib.error import HTTPError

import pytest

from src.services.naver_shopping import NaverShoppingClient, NaverShoppingConfig, build_naver_query
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
