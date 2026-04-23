from __future__ import annotations

from dataclasses import dataclass
import hashlib
import html
import json
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from src.services.store import ProductRecord, UploadAnalysis


CATEGORY_QUERIES = {
    "top": "상의",
    "bottom": "하의",
    "outer": "아우터",
    "shoes": "신발",
    "bag": "가방",
}

CATEGORY_ORDER = ("top", "bottom", "outer", "shoes", "bag")

MOOD_QUERIES = {
    "minimal": "미니멀",
    "casual": "캐주얼",
    "street": "스트릿",
    "feminine": "페미닌",
}

TONE_QUERIES = {
    "warm": "웜톤",
    "cool": "쿨톤",
    "neutral": "뉴트럴",
}

TAG_VALUES = {
    "tone": ("warm", "cool", "neutral"),
    "mood": ("minimal", "casual", "street", "feminine"),
    "silhouette": ("relaxed", "slim", "layered", "balanced"),
}


@dataclass(frozen=True)
class NaverShoppingConfig:
    client_id: str | None
    client_secret: str | None
    display: int = 30
    timeout_seconds: float = 3.0

    @property
    def enabled(self) -> bool:
        return bool(self.client_id and self.client_secret)


@dataclass(frozen=True)
class NaverShoppingSearchResult:
    products: list[ProductRecord]
    fallback_reason: str | None = None
    fallback_message: str | None = None


def build_naver_query(analysis: UploadAnalysis, category: str | None) -> str:
    category_keyword = CATEGORY_QUERIES.get(category or "")
    if category_keyword is None:
        first_preferred = analysis.preferred_categories[0] if analysis.preferred_categories else "top"
        category_keyword = CATEGORY_QUERIES.get(first_preferred, "패션")

    query_parts = [
        TONE_QUERIES.get(analysis.dominant_tone, ""),
        MOOD_QUERIES.get(analysis.style_mood, ""),
        category_keyword,
    ]
    return " ".join(part for part in query_parts if part).strip() or "패션 의류"


def build_custom_naver_query(custom_query: str, category: str | None) -> str:
    normalized_query = " ".join(custom_query.split())
    category_keyword = CATEGORY_QUERIES.get(category or "")
    if category_keyword and category_keyword not in normalized_query:
        return f"{normalized_query} {category_keyword}".strip()

    return normalized_query or "패션 의류"


def build_naver_category_queries(analysis: UploadAnalysis) -> list[tuple[str, str]]:
    return [(category, build_naver_query(analysis, category)) for category in CATEGORY_ORDER]


def build_custom_naver_category_queries(custom_query: str) -> list[tuple[str, str]]:
    return [(category, build_custom_naver_query(custom_query, category)) for category in CATEGORY_ORDER]


class NaverShoppingClient:
    api_url = "https://openapi.naver.com/v1/search/shop.json"

    def __init__(self, config: NaverShoppingConfig) -> None:
        self.config = config

    def search_products(self, query: str, category: str | None, limit: int) -> list[ProductRecord]:
        return self.search(query=query, category=category, limit=limit).products

    def search(self, query: str, category: str | None, limit: int) -> NaverShoppingSearchResult:
        if not self.config.enabled:
            return NaverShoppingSearchResult(
                products=[],
                fallback_reason="credentials_missing",
                fallback_message="네이버 쇼핑 API 키가 없어 샘플 데이터로 표시하고 있습니다.",
            )

        display = max(1, min(limit, self.config.display, 100))
        params = urlencode({"query": query, "display": display, "start": 1, "sort": "sim"})
        request = Request(
            f"{self.api_url}?{params}",
            headers={
                "X-Naver-Client-Id": self.config.client_id or "",
                "X-Naver-Client-Secret": self.config.client_secret or "",
            },
            method="GET",
        )

        try:
            with urlopen(request, timeout=self.config.timeout_seconds) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            reason = "auth_failed" if error.code in {401, 403} else "api_error"
            return NaverShoppingSearchResult(
                products=[],
                fallback_reason=reason,
                fallback_message=_build_http_error_message(error),
            )
        except (URLError, TimeoutError, OSError):
            return NaverShoppingSearchResult(
                products=[],
                fallback_reason="network_error",
                fallback_message="네이버 쇼핑 API 연결이 원활하지 않아 샘플 데이터로 표시하고 있습니다.",
            )
        except json.JSONDecodeError:
            return NaverShoppingSearchResult(
                products=[],
                fallback_reason="invalid_response",
                fallback_message="네이버 쇼핑 API 응답을 해석하지 못해 샘플 데이터로 표시하고 있습니다.",
            )

        items = payload.get("items")
        if not isinstance(items, list):
            return NaverShoppingSearchResult(
                products=[],
                fallback_reason="invalid_response",
                fallback_message="네이버 쇼핑 API 응답 형식이 달라 샘플 데이터로 표시하고 있습니다.",
            )

        products: list[ProductRecord] = []
        for item in items:
            if not isinstance(item, dict):
                continue

            product = self._parse_item(item=item, category_hint=category)
            if product is not None:
                products.append(product)

        if not products:
            return NaverShoppingSearchResult(
                products=[],
                fallback_reason="no_products",
                fallback_message="네이버 쇼핑에서 조건에 맞는 상품을 찾지 못해 샘플 데이터로 표시하고 있습니다.",
            )

        return NaverShoppingSearchResult(products=products)

    def _parse_item(self, item: dict, category_hint: str | None) -> ProductRecord | None:
        title = _strip_html(str(item.get("title") or "")).strip()
        link = str(item.get("link") or "").strip()
        image_url = str(item.get("image") or "").strip()
        if not title or not link:
            return None

        price = _parse_price(item.get("lprice"))
        if price <= 0:
            return None

        source_id = str(item.get("productId") or _stable_digest(link)[:16])
        category = category_hint or _infer_category(item=item, title=title)
        fingerprint = f"{title}:{link}".encode("utf-8")
        digest = hashlib.sha256(fingerprint).digest()

        return ProductRecord(
            id=f"naver-{source_id}",
            source="naver",
            product_name=title,
            category=category,
            price=price,
            product_url=link,
            image_url=image_url or _fallback_image_url(title),
            dominant_tone=_pick_tag("tone", digest[0]),
            style_mood=_pick_tag("mood", digest[1]),
            silhouette=_pick_tag("silhouette", digest[2]),
            feature_vector=tuple(round(digest[idx] / 255, 4) for idx in range(4)),
        )


def _strip_html(value: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", value))


def _parse_price(value: object) -> int:
    try:
        return int(str(value or "0"))
    except ValueError:
        return 0


def _stable_digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _pick_tag(group: str, value: int) -> str:
    values = TAG_VALUES[group]
    return values[value % len(values)]


def _infer_category(item: dict, title: str) -> str:
    haystack = " ".join(
        str(item.get(key) or "")
        for key in ("category1", "category2", "category3", "category4")
    ) + f" {title}"

    if any(keyword in haystack for keyword in ("신발", "슈즈", "스니커즈", "운동화", "로퍼", "부츠")):
        return "shoes"
    if any(keyword in haystack for keyword in ("가방", "백", "토트", "숄더", "크로스")):
        return "bag"
    if any(keyword in haystack for keyword in ("자켓", "재킷", "코트", "점퍼", "가디건", "아우터")):
        return "outer"
    if any(keyword in haystack for keyword in ("팬츠", "바지", "스커트", "데님", "슬랙스")):
        return "bottom"
    return "top"


def _fallback_image_url(title: str) -> str:
    safe_title = _stable_digest(title)[:16]
    return f"https://example.com/naver/{safe_title}.jpg"


def _build_http_error_message(error: HTTPError) -> str:
    base_message = "네이버 쇼핑 API 인증에 실패해 샘플 데이터로 표시하고 있습니다."
    if error.code not in {401, 403}:
        base_message = "네이버 쇼핑 API 호출에 실패해 샘플 데이터로 표시하고 있습니다."

    try:
        payload = json.loads(error.read().decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError, OSError):
        return base_message

    raw_message = payload.get("errorMessage") if isinstance(payload, dict) else None
    if not isinstance(raw_message, str) or not raw_message:
        return base_message

    sanitized_message = re.sub(r"\s+", " ", raw_message).strip()
    return f"{base_message} 네이버 응답: {sanitized_message}"
