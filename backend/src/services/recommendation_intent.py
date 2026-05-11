from __future__ import annotations

from dataclasses import dataclass

INTENT_KEYWORD_ALIASES = {
    "긴팔": ("긴팔", "롱슬리브", "롱 슬리브", "long sleeve", "long-sleeve"),
    "반팔": ("반팔", "숏슬리브", "숏 슬리브", "short sleeve", "short-sleeve"),
    "민소매": ("민소매", "슬리브리스", "나시", "탱크탑", "sleeveless", "tank top"),
    "롱스커트": ("롱스커트", "맥시 스커트", "maxi skirt"),
    "미니스커트": ("미니스커트", "미니 스커트", "mini skirt"),
    "크롭": ("크롭", "크롭티", "cropped", "crop"),
    "와이드": ("와이드", "와이드핏", "wide fit", "wide"),
}

ITEM_FAMILY_ALIASES = {
    "셔츠": ("셔츠", "남방"),
    "블라우스": ("블라우스",),
    "티셔츠": ("티셔츠", "티 ", "티셔츠", "tee"),
    "니트 탑": ("니트 탑", "니트", "스웨터"),
    "슬리브리스 탑": ("슬리브리스 탑", "슬리브리스", "민소매", "나시", "탱크탑"),
    "탑": ("탑",),
    "가디건": ("가디건",),
    "니트 베스트": ("니트 베스트", "니트 조끼", "베스트"),
    "자켓": ("자켓", "재킷", "블레이저"),
    "점퍼": ("점퍼", "집업", "블루종"),
    "코트": ("코트", "트렌치", "트렌치코트"),
    "데님 팬츠": ("데님 팬츠", "청바지", "데님", "진", "jeans"),
    "와이드 데님 팬츠": ("와이드 데님 팬츠", "와이드 청바지", "와이드 데님"),
    "슬랙스": ("슬랙스",),
    "와이드 팬츠": ("와이드 팬츠", "와이드핏 팬츠"),
    "팬츠": ("팬츠", "바지"),
    "플리츠 스커트": ("플리츠 스커트",),
    "미니 스커트": ("미니 스커트",),
    "스커트": ("스커트",),
    "메리제인 슈즈": ("메리제인 슈즈", "메리제인", "mary jane"),
    "플랫 슈즈": ("플랫 슈즈", "플랫슈즈", "플랫", "발레 슈즈", "발레 플랫", "ballerina", "ballet flat"),
    "로퍼": ("로퍼",),
    "스니커즈": ("스니커즈", "운동화", "스니커"),
    "부츠": ("부츠", "워커"),
    "샌들": ("샌들", "슬리퍼", "뮬", "블로퍼", "쪼리"),
    "구두": ("구두", "힐", "펌프스"),
    "숄더백": ("숄더백", "숄더", "호보백", "호보"),
    "토트백": ("토트백", "토트"),
    "크로스백": ("크로스백", "크로스"),
    "백팩": ("백팩",),
    "클러치": ("클러치", "파우치"),
    "버킷백": ("버킷백",),
    "에코백": ("에코백",),
    "가방": ("가방", "백"),
    "안경": ("안경", "선글라스", "아이웨어"),
    "목걸이": ("목걸이", "네크리스"),
    "귀걸이": ("귀걸이", "이어링"),
    "팔찌": ("팔찌", "브레이슬릿"),
    "반지": ("반지", "링"),
    "벨트": ("벨트",),
    "모자": ("모자", "캡", "비니", "버킷햇", "베레모"),
    "머플러": ("머플러", "스카프", "목도리"),
    "양말": ("양말", "삭스"),
    "머리끈": ("머리끈", "헤어밴드", "헤어핀", "스크런치", "리본"),
}

STYLE_DESCRIPTOR_ALIASES = {
    "스트라이프": ("스트라이프", "stripe", "striped"),
    "도트": ("도트", "polka", "dots"),
    "체크": ("체크", "check", "checked", "plaid"),
    "플라워": ("플라워", "플로럴", "꽃무늬", "floral"),
    "레이스": ("레이스", "lace"),
    "플리츠": ("플리츠", "pleats", "pleated"),
    "데님": ("데님", "청바지", "denim"),
    "가죽": ("가죽", "레더", "라이더", "leather"),
    "스웨이드": ("스웨이드", "suede"),
    "니트": ("니트", "knit"),
    "트위드": ("트위드", "tweed"),
    "린넨": ("린넨", "linen"),
    "벨벳": ("벨벳", "velvet", "velour"),
    "코듀로이": ("코듀로이", "corduroy"),
    "와이드": ("와이드", "wide"),
    "미니": ("미니", "mini"),
    "크롭": ("크롭", "crop", "cropped"),
    "체인": ("체인", "chain"),
    "진주": ("진주", "pearl", "펄"),
    "메탈": ("메탈", "metal", "실버", "골드"),
}

BRAND_KEYWORD_ALIASES = {
    "뉴발란스": ("뉴발란스", "new balance", "newbalance"),
    "나이키": ("나이키", "nike"),
    "아디다스": ("아디다스", "adidas"),
    "컨버스": ("컨버스", "converse"),
    "반스": ("반스", "vans"),
    "아식스": ("아식스", "asics"),
    "푸마": ("푸마", "puma"),
    "닥터마틴": ("닥터마틴", "dr. martens", "dr martens", "doc martens"),
}


@dataclass(frozen=True)
class SearchKeywordSignals:
    item_families: list[str]
    descriptors: list[str]
    brands: list[str]


def extract_intent_keywords(text: str) -> list[str]:
    normalized = _normalize_text(text)
    if not normalized:
        return []

    detected: list[str] = []
    for keyword, aliases in INTENT_KEYWORD_ALIASES.items():
        if any(alias in normalized for alias in aliases):
            detected.append(keyword)
    return detected


def matches_intent_keyword(text: str, keyword: str) -> bool:
    normalized = _normalize_text(text)
    if not normalized:
        return False

    aliases = INTENT_KEYWORD_ALIASES.get(keyword, (keyword,))
    return any(alias in normalized for alias in aliases)


def dedupe_keywords(values: list[str]) -> list[str]:
    deduped: list[str] = []
    seen: set[str] = set()
    for value in values:
        normalized = value.strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        deduped.append(normalized)
    return deduped


def extract_item_families(text: str) -> list[str]:
    normalized = _normalize_text(text)
    if not normalized:
        return []

    detected: list[str] = []
    for family, aliases in ITEM_FAMILY_ALIASES.items():
        if any(alias in normalized for alias in aliases):
            detected.append(family)
    return dedupe_keywords(detected)


def matches_item_family(text: str, family: str) -> bool:
    normalized = _normalize_text(text)
    if not normalized:
        return False

    aliases = ITEM_FAMILY_ALIASES.get(family, (family,))
    return any(alias in normalized for alias in aliases)


def extract_style_descriptors(text: str) -> list[str]:
    normalized = _normalize_text(text)
    if not normalized:
        return []

    detected: list[str] = []
    for descriptor, aliases in STYLE_DESCRIPTOR_ALIASES.items():
        if any(alias in normalized for alias in aliases):
            detected.append(descriptor)
    return dedupe_keywords(detected)


def matches_style_descriptor(text: str, descriptor: str) -> bool:
    normalized = _normalize_text(text)
    if not normalized:
        return False

    aliases = STYLE_DESCRIPTOR_ALIASES.get(descriptor, (descriptor,))
    return any(alias in normalized for alias in aliases)


def extract_brand_keywords(text: str) -> list[str]:
    normalized = _normalize_text(text)
    if not normalized:
        return []

    detected: list[str] = []
    for brand, aliases in BRAND_KEYWORD_ALIASES.items():
        if brand.lower() in normalized or any(alias in normalized for alias in aliases):
            detected.append(brand)
    return dedupe_keywords(detected)


def matches_brand_keyword(text: str, brand: str) -> bool:
    normalized = _normalize_text(text)
    if not normalized:
        return False

    aliases = BRAND_KEYWORD_ALIASES.get(brand, (brand,))
    return brand.lower() in normalized or any(alias in normalized for alias in aliases)


def extract_search_keyword_signals(text: str) -> SearchKeywordSignals:
    return SearchKeywordSignals(
        item_families=extract_item_families(text),
        descriptors=extract_style_descriptors(text),
        brands=extract_brand_keywords(text),
    )


def _normalize_text(text: str) -> str:
    return " ".join(text.lower().split())
