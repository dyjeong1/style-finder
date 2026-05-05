from __future__ import annotations

INTENT_KEYWORD_ALIASES = {
    "긴팔": ("긴팔", "롱슬리브", "롱 슬리브", "long sleeve", "long-sleeve"),
    "반팔": ("반팔", "숏슬리브", "숏 슬리브", "short sleeve", "short-sleeve"),
    "민소매": ("민소매", "슬리브리스", "나시", "탱크탑", "sleeveless", "tank top"),
    "롱스커트": ("롱스커트", "맥시 스커트", "maxi skirt"),
    "미니스커트": ("미니스커트", "미니 스커트", "mini skirt"),
    "크롭": ("크롭", "크롭티", "cropped", "crop"),
    "와이드": ("와이드", "와이드핏", "wide fit", "wide"),
}


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


def _normalize_text(text: str) -> str:
    return " ".join(text.lower().split())
