from __future__ import annotations

from dataclasses import dataclass
import hashlib
import html
import json
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from src.services.image_analysis import analyze_image_content, infer_color_from_text
from src.services.store import ProductRecord, UploadAnalysis


CATEGORY_QUERIES = {
    "top": "상의",
    "bottom": "하의",
    "outer": "아우터",
    "shoes": "신발",
    "bag": "가방",
    "accessory": "악세서리",
}

CATEGORY_ORDER = ("top", "bottom", "outer", "shoes", "bag", "accessory")

CATEGORY_KEYWORDS = {
    "top": (
        "상의",
        "셔츠",
        "남방",
        "티셔츠",
        "반팔",
        "긴팔",
        "니트",
        "스웨터",
        "블라우스",
        "맨투맨",
        "후드",
        "후드티",
        "민소매",
        "나시",
        "탱크탑",
        "크롭티",
        "카라티",
        "폴로",
        "베스트",
        "뷔스티에",
        "튜브탑",
    ),
    "bottom": (
        "하의",
        "팬츠",
        "바지",
        "스커트",
        "데님",
        "청바지",
        "슬랙스",
        "와이드팬츠",
        "조거팬츠",
        "카고팬츠",
        "트레이닝팬츠",
        "쇼츠",
        "반바지",
        "미니스커트",
        "롱스커트",
        "플리츠스커트",
        "레깅스",
        "큐롯",
    ),
    "outer": (
        "아우터",
        "자켓",
        "재킷",
        "코트",
        "점퍼",
        "가디건",
        "트렌치",
        "트렌치코트",
        "블레이저",
        "패딩",
        "다운",
        "파카",
        "야상",
        "봄버",
        "항공점퍼",
        "바람막이",
        "무스탕",
        "후리스",
        "플리스",
        "집업",
        "라이더",
    ),
    "shoes": (
        "신발",
        "슈즈",
        "스니커즈",
        "운동화",
        "로퍼",
        "부츠",
        "샌들",
        "메리제인",
        "구두",
        "슬리퍼",
        "플랫",
        "플랫슈즈",
        "힐",
        "펌프스",
        "뮬",
        "블로퍼",
        "옥스포드화",
        "워커",
        "쪼리",
    ),
    "bag": (
        "가방",
        "백팩",
        "토트백",
        "토트",
        "숄더백",
        "숄더",
        "크로스백",
        "크로스",
        "미니백",
        "호보백",
        "호보",
        "버킷백",
        "클러치",
        "파우치",
        "에코백",
        "메신저백",
        "체인백",
        "보스턴백",
        "새들백",
        "힙색",
        "벨트백",
    ),
    "accessory": (
        "악세서리",
        "액세서리",
        "안경",
        "선글라스",
        "머플러",
        "스카프",
        "목도리",
        "모자",
        "캡",
        "비니",
        "벨트",
        "양말",
        "목걸이",
        "귀걸이",
        "반지",
        "헤어핀",
        "스크런치",
    ),
}

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

COLOR_QUERIES = {
    "black": "블랙",
    "white": "화이트",
    "gray": "그레이",
    "beige": "베이지",
    "brown": "브라운",
    "navy": "네이비",
    "blue": "블루",
    "green": "그린",
    "red": "레드",
    "pink": "핑크",
    "yellow": "옐로우",
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
    analyze_product_images: bool = False
    image_timeout_seconds: float = 1.0
    max_image_bytes: int = 2_000_000
    max_product_image_analysis_count: int = 12

    @property
    def enabled(self) -> bool:
        return bool(self.client_id and self.client_secret)


@dataclass(frozen=True)
class NaverShoppingSearchResult:
    products: list[ProductRecord]
    fallback_reason: str | None = None
    fallback_message: str | None = None


def build_naver_query(analysis: UploadAnalysis, category: str | None) -> str:
    if category and analysis.category_query_hints.get(category):
        return analysis.category_query_hints[category]

    category_keyword = CATEGORY_QUERIES.get(category or "")
    if category_keyword is None:
        first_preferred = analysis.preferred_categories[0] if analysis.preferred_categories else "top"
        category_keyword = CATEGORY_QUERIES.get(first_preferred, "패션")

    query_parts = [
        COLOR_QUERIES.get(analysis.dominant_color, ""),
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


def infer_custom_query_categories(custom_query: str) -> list[str]:
    normalized_query = " ".join(custom_query.split())

    return [
        category
        for category in CATEGORY_ORDER
        if any(keyword in normalized_query for keyword in CATEGORY_KEYWORDS[category])
    ]


def build_naver_category_queries(analysis: UploadAnalysis) -> list[tuple[str, str]]:
    categories = [
        category
        for category in CATEGORY_ORDER
        if not analysis.category_query_hints or category in analysis.category_query_hints
    ]
    return [(category, build_naver_query(analysis, category)) for category in categories]


def build_custom_naver_category_queries(custom_query: str) -> list[tuple[str, str]]:
    inferred_categories = infer_custom_query_categories(custom_query)
    categories = inferred_categories or list(CATEGORY_ORDER)

    return [(category, build_custom_naver_query(custom_query, category)) for category in categories]


class NaverShoppingClient:
    api_url = "https://openapi.naver.com/v1/search/shop.json"

    def __init__(self, config: NaverShoppingConfig) -> None:
        self.config = config
        self._product_image_analysis_attempts = 0

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

            product = self._parse_item(item=item, category_hint=category, query=query)
            if product is not None:
                products.append(product)

        if not products:
            return NaverShoppingSearchResult(
                products=[],
                fallback_reason="no_products",
                fallback_message="네이버 쇼핑에서 조건에 맞는 상품을 찾지 못해 샘플 데이터로 표시하고 있습니다.",
            )

        return NaverShoppingSearchResult(products=products)

    def _parse_item(self, item: dict, category_hint: str | None, query: str | None = None) -> ProductRecord | None:
        title = _strip_html(str(item.get("title") or "")).strip()
        link = str(item.get("link") or "").strip()
        image_url = str(item.get("image") or "").strip()
        if not title or not link:
            return None

        price = _parse_price(item.get("lprice"))
        if price <= 0:
            return None

        source_id = str(item.get("productId") or _stable_digest(link)[:16])
        inferred_category = _infer_category(item=item, title=title)
        if category_hint and not _matches_category_query(item=item, title=title, category_hint=category_hint, query=query):
            return None
        category = category_hint or inferred_category
        fingerprint = f"{title}:{link}".encode("utf-8")
        digest = hashlib.sha256(fingerprint).digest()
        image_analysis = self._analyze_product_image(image_url)
        dominant_color = image_analysis.dominant_color if image_analysis else infer_color_from_text(title)
        feature_vector = (
            image_analysis.feature_vector
            if image_analysis
            else tuple(round(digest[idx] / 255, 4) for idx in range(4))
        )

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
            feature_vector=feature_vector,
            dominant_color=dominant_color,
        )

    def _analyze_product_image(self, image_url: str):
        if not self.config.analyze_product_images or not image_url.startswith(("http://", "https://")):
            return None
        if self._product_image_analysis_attempts >= self.config.max_product_image_analysis_count:
            return None

        self._product_image_analysis_attempts += 1

        request = Request(
            image_url,
            headers={"User-Agent": "StyleMatchLocal/0.1"},
            method="GET",
        )

        try:
            with urlopen(request, timeout=self.config.image_timeout_seconds) as response:
                content_length = response.headers.get("Content-Length")
                if content_length and int(content_length) > self.config.max_image_bytes:
                    return None

                content = response.read(self.config.max_image_bytes + 1)
        except (HTTPError, URLError, TimeoutError, OSError, ValueError):
            return None

        if len(content) > self.config.max_image_bytes:
            return None

        return analyze_image_content(content)


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
    if any(keyword in haystack for keyword in ("안경", "선글라스", "머플러", "스카프", "목도리", "모자", "벨트", "양말", "악세서리", "액세서리")):
        return "accessory"
    if any(keyword in haystack for keyword in ("자켓", "재킷", "코트", "점퍼", "가디건", "아우터")):
        return "outer"
    if any(keyword in haystack for keyword in ("팬츠", "바지", "스커트", "데님", "슬랙스")):
        return "bottom"
    return "top"


def _matches_category_query(item: dict, title: str, category_hint: str, query: str | None) -> bool:
    haystack = " ".join(
        str(item.get(key) or "")
        for key in ("category1", "category2", "category3", "category4")
    ) + f" {title}"

    if not any(keyword in haystack for keyword in CATEGORY_KEYWORDS.get(category_hint, ())):
        return False

    specific_keywords = _extract_specific_query_keywords(query or "", category_hint)
    if not specific_keywords:
        return True

    return any(keyword in haystack for keyword in specific_keywords)


def _extract_specific_query_keywords(query: str, category_hint: str) -> list[str]:
    normalized_query = " ".join(query.split())
    if not normalized_query:
        return []

    generic_keywords = {
        CATEGORY_QUERIES.get(category_hint, ""),
        "패션",
        "의류",
        "신발",
        "가방",
        "악세서리",
        "악세서리",
        "상의",
        "하의",
        "아우터",
    }
    color_keywords = {label for label in COLOR_QUERIES.values()}
    tone_keywords = {label for label in TONE_QUERIES.values()}
    mood_keywords = {label for label in MOOD_QUERIES.values()}

    return [
        keyword
        for keyword in CATEGORY_KEYWORDS.get(category_hint, ())
        if keyword in normalized_query
        and keyword not in generic_keywords
        and keyword not in color_keywords
        and keyword not in tone_keywords
        and keyword not in mood_keywords
    ]


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
