from __future__ import annotations

import base64
from dataclasses import dataclass, field
import json
import logging
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from src.services.image_analysis import (
    CATEGORY_QUERY_LABELS,
    COLOR_QUERY_LABELS,
    DEFAULT_ITEM_LABELS,
    DetectedOutfitItem,
    infer_color_from_text,
)


OPENAI_ALLOWED_CATEGORIES = ("top", "outer", "bottom", "shoes", "bag", "accessory")
OPENAI_ALLOWED_COLORS = tuple(COLOR_QUERY_LABELS) + ("neutral", "unknown")
GEMINI_GENERATE_CONTENT_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
OLLAMA_CHAT_URL = "http://127.0.0.1:11434/api/chat"
logger = logging.getLogger(__name__)
OPENAI_RESPONSE_SCHEMA = {
    "name": "outfit_analysis",
    "strict": True,
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "category": {"type": "string", "enum": list(OPENAI_ALLOWED_CATEGORIES)},
                        "color": {"type": "string", "enum": list(OPENAI_ALLOWED_COLORS)},
                        "item_label": {"type": "string"},
                        "query": {"type": "string"},
                    },
                    "required": ["category", "color", "item_label", "query"],
                },
            }
        },
        "required": ["items"],
    },
}
OPENAI_SYSTEM_PROMPT = """당신은 패션 코디 이미지를 분석하는 한국어 스타일 분석기다.

목표:
- 이미지 안에 실제로 보이는 패션 아이템만 식별한다.
- 허용 카테고리는 top, outer, bottom, shoes, bag, accessory 뿐이다.
- 카테고리가 보이지 않으면 절대 추측해서 넣지 않는다.
- 같은 카테고리에 여러 품목이 보이면 모두 반환할 수 있다. 예: accessory의 안경과 목걸이.
- 배경, 사람의 신체, 휴대폰, 컵, 의자, 테이블, 벽, 거울, 그림자, 텍스트, 스티커는 제외한다.
- outer와 top이 동시에 보이면 분리한다. 예: 가디건 + 나시.
- 어깨에 걸친 가디건이나 니트도 outer로 본다.
- query는 쇼핑 검색에 바로 쓸 수 있는 간결한 한국어 검색어여야 한다.

출력 규칙:
- color는 enum 안에서 가장 가까운 값 하나만 사용한다.
- item_label은 한국어 세부 품목명으로 작성한다.
- query는 가능하면 '색상 + 품목명' 형태로 작성한다.
"""
GEMINI_SYSTEM_PROMPT = OPENAI_SYSTEM_PROMPT

ITEM_LABEL_NORMALIZATION_RULES = {
    "top": (
        (("슬리브리스", "나시", "탱크"), "슬리브리스 탑"),
        (("스트라이프", "니트"), "스트라이프 니트 탑"),
        (("스트라이프", "스웨터"), "스트라이프 니트 탑"),
        (("골지 상의", "골지 탑", "이너 탑", "이너웨어"), "탑"),
        (("이너",), "탑"),
        (("상의",), "탑"),
        (("블라우스",), "블라우스"),
        (("셔츠",), "셔츠"),
        (("티셔츠", "티 ", "tee"), "티셔츠"),
        (("스웨터",), "니트 탑"),
        (("니트",), "니트 탑"),
    ),
    "outer": (
        (("가디건",), "가디건"),
        (("니트 조끼", "브이넥 니트 조끼"), "니트 베스트"),
        (("니트 베스트",), "니트 베스트"),
        (("베스트",), "베스트"),
        (("레더", "가죽", "라이더"), "레더 자켓"),
        (("재킷",), "자켓"),
        (("블레이저", "자켓"), "자켓"),
        (("점퍼", "블루종", "집업"), "점퍼"),
        (("민소매 원피스", "점프수트"), "원피스"),
        (("원피스",), "원피스"),
        (("코트",), "코트"),
    ),
    "bottom": (
        (("도트", "미니", "스커트"), "미니 스커트"),
        (("플리츠", "스커트"), "플리츠 스커트"),
        (("레이스", "스커트"), "레이스 스커트"),
        (("미니", "스커트"), "미니 스커트"),
        (("스커트",), "스커트"),
        (("와이드", "청바지"), "와이드 데님 팬츠"),
        (("와이드", "데님"), "와이드 데님 팬츠"),
        (("청바지",), "데님 팬츠"),
        (("데님",), "데님 팬츠"),
        (("슬랙스",), "슬랙스"),
        (("와이드", "팬츠"), "와이드 팬츠"),
        (("팬츠",), "팬츠"),
    ),
    "shoes": (
        (("메리제인",), "메리제인 슈즈"),
        (("로퍼",), "로퍼"),
        (("부츠",), "부츠"),
        (("운동화",), "스니커즈"),
        (("스니커",), "스니커즈"),
        (("구두",), "구두"),
    ),
    "bag": (
        (("숄더",), "숄더백"),
        (("크로스",), "크로스백"),
        (("토트",), "토트백"),
        (("백팩",), "백팩"),
        (("가방",), "가방"),
    ),
    "accessory": (
        (("선글라스",), "안경"),
        (("안경테",), "안경"),
        (("아이웨어",), "안경"),
        (("안경",), "안경"),
        (("목걸이", "네크리스"), "목걸이"),
        (("귀걸이", "이어링"), "귀걸이"),
        (("체인 팔찌",), "팔찌"),
        (("팔찌", "브레이슬릿"), "팔찌"),
        (("반지", "링"), "반지"),
        (("머플러", "스카프"), "머플러"),
        (("모자", "캡", "비니", "버킷", "베레모"), "모자"),
        (("머리끈", "스크런치", "헤어밴드", "리본"), "머리끈"),
        (("양말", "삭스"), "양말"),
        (("벨트",), "벨트"),
    ),
}
ALL_KEYWORD_NORMALIZATION_LABELS = {
    "도트 미니 스커트",
    "플리츠 스커트",
    "레이스 스커트",
    "미니 스커트",
    "와이드 데님 팬츠",
    "와이드 팬츠",
}


@dataclass(frozen=True)
class VisionOutfitAnalyzerConfig:
    enabled: bool = False
    provider: str = "disabled"
    model_name: str = ""
    max_image_bytes: int = 2_000_000
    timeout_seconds: float = 20.0
    api_base_url: str = ""
    api_key: str | None = None


@dataclass
class VisionOutfitAnalyzer:
    config: VisionOutfitAnalyzerConfig
    mock_items: tuple[DetectedOutfitItem, ...] = field(default_factory=tuple)

    def analyze(self, content: bytes) -> list[DetectedOutfitItem]:
        try:
            return self.analyze_or_raise(content)
        except Exception as exc:
            provider = (self.config.provider or "disabled").lower()
            provider_label = "Vision"
            if provider == "openai":
                provider_label = "OpenAI Vision"
            elif provider == "gemini":
                provider_label = "Gemini Vision"
            elif provider == "ollama":
                provider_label = "Ollama Vision"
            logger.warning("%s provider fallback: %s", provider_label, summarize_provider_error(exc))
            return []

    def analyze_or_raise(self, content: bytes) -> list[DetectedOutfitItem]:
        if not self.config.enabled or not content:
            return []
        if len(content) > self.config.max_image_bytes:
            return []

        provider = (self.config.provider or "disabled").lower()
        if provider == "mock":
            return list(self.mock_items)
        if provider == "openai":
            return self._analyze_with_openai(content)
        if provider == "gemini":
            return self._analyze_with_gemini(content)
        if provider == "ollama":
            return self._analyze_with_ollama(content)

        return []

    def coerce_detected_items(self, parsed_payload: dict[str, Any]) -> list[DetectedOutfitItem]:
        return self._coerce_detected_items(parsed_payload)

    def _analyze_with_openai(self, content: bytes) -> list[DetectedOutfitItem]:
        if not self.config.api_key:
            return []

        payload = {
            "model": self.config.model_name or "gpt-4o",
            "input": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": OPENAI_SYSTEM_PROMPT,
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": "이미지를 분석해 지정된 JSON schema에 맞는 착장 품목만 반환해줘.",
                        },
                        {
                            "type": "input_image",
                            "image_url": self._build_data_url(content),
                        },
                    ],
                },
            ],
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": OPENAI_RESPONSE_SCHEMA["name"],
                    "strict": OPENAI_RESPONSE_SCHEMA["strict"],
                    "schema": OPENAI_RESPONSE_SCHEMA["schema"],
                }
            },
        }
        response_payload = self._post_json(
            url=self.config.api_base_url or "https://api.openai.com/v1/responses",
            payload=payload,
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            },
        )
        parsed_payload = self._extract_response_payload(response_payload)
        return self._coerce_detected_items(parsed_payload)

    def _analyze_with_gemini(self, content: bytes) -> list[DetectedOutfitItem]:
        if not self.config.api_key:
            return []

        model_name = self.config.model_name or "gemini-2.5-flash"
        url = self.config.api_base_url or GEMINI_GENERATE_CONTENT_URL.format(model=model_name)
        payload = {
            "system_instruction": {"parts": [{"text": GEMINI_SYSTEM_PROMPT}]},
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": "이미지를 분석해 지정된 JSON schema에 맞는 착장 품목만 반환해줘."},
                        {
                            "inline_data": {
                                "mime_type": guess_mime_type(content),
                                "data": base64.b64encode(content).decode("ascii"),
                            }
                        },
                    ],
                }
            ],
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseJsonSchema": OPENAI_RESPONSE_SCHEMA["schema"],
            },
        }
        response_payload = self._post_json(
            url=f"{url}?key={self.config.api_key}",
            payload=payload,
            headers={"Content-Type": "application/json"},
        )
        parsed_payload = self._extract_gemini_payload(response_payload)
        return self._coerce_detected_items(parsed_payload)

    def _analyze_with_ollama(self, content: bytes) -> list[DetectedOutfitItem]:
        model_name = self.config.model_name or "qwen2.5vl:7b"
        payload = {
            "model": model_name,
            "stream": False,
            "format": OPENAI_RESPONSE_SCHEMA["schema"],
            "options": {"temperature": 0},
            "messages": [
                {
                    "role": "system",
                    "content": OPENAI_SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": "이미지를 분석해 지정된 JSON schema에 맞는 착장 품목만 반환해줘.",
                    "images": [base64.b64encode(content).decode("ascii")],
                },
            ],
        }
        headers = {"Content-Type": "application/json"}
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"

        response_payload = self._post_json(
            url=self.config.api_base_url or OLLAMA_CHAT_URL,
            payload=payload,
            headers=headers,
        )
        parsed_payload = self._extract_ollama_payload(response_payload)
        return self._coerce_detected_items(parsed_payload)

    def _post_json(self, url: str, payload: dict[str, Any], headers: dict[str, str]) -> dict[str, Any]:
        request = Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )

        try:
            with urlopen(request, timeout=self.config.timeout_seconds) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError:
            raise
        except URLError:
            raise

    def _extract_response_payload(self, response_payload: dict[str, Any]) -> dict[str, Any]:
        if isinstance(response_payload.get("output_text"), str):
            return json.loads(response_payload["output_text"])

        for output_item in response_payload.get("output", []):
            for content_item in output_item.get("content", []):
                if isinstance(content_item.get("parsed"), dict):
                    return content_item["parsed"]
                if isinstance(content_item.get("json"), dict):
                    return content_item["json"]
                text_value = content_item.get("text")
                if isinstance(text_value, str) and text_value.strip():
                    return json.loads(text_value)

        raise ValueError("OpenAI response did not contain structured JSON output")

    def _extract_gemini_payload(self, response_payload: dict[str, Any]) -> dict[str, Any]:
        for candidate in response_payload.get("candidates", []):
            content = candidate.get("content", {})
            for part in content.get("parts", []):
                text_value = part.get("text")
                if isinstance(text_value, str) and text_value.strip():
                    return json.loads(text_value)

        raise ValueError("Gemini response did not contain structured JSON output")

    def _extract_ollama_payload(self, response_payload: dict[str, Any]) -> dict[str, Any]:
        message = response_payload.get("message", {})
        text_value = message.get("content")
        if isinstance(text_value, str) and text_value.strip():
            return json.loads(text_value)
        raise ValueError("Ollama response did not contain structured JSON output")

    def _coerce_detected_items(self, parsed_payload: dict[str, Any]) -> list[DetectedOutfitItem]:
        raw_items = parsed_payload.get("items", [])
        if not isinstance(raw_items, list):
            return []

        normalized_items: list[DetectedOutfitItem] = []
        seen: set[tuple[str, str, str, str]] = set()

        for raw_item in raw_items:
            if not isinstance(raw_item, dict):
                continue

            category = str(raw_item.get("category", "")).strip().lower()
            if category not in OPENAI_ALLOWED_CATEGORIES:
                continue

            color = str(raw_item.get("color", "unknown")).strip().lower()
            if color not in OPENAI_ALLOWED_COLORS:
                color = "unknown"

            item_label = str(raw_item.get("item_label", "")).strip()
            if not item_label:
                item_label = DEFAULT_ITEM_LABELS.get(category, {}).get(color, CATEGORY_QUERY_LABELS.get(category, category))

            query = str(raw_item.get("query", "")).strip()
            color = _normalize_item_color(category=category, color=color, item_label=item_label, query=query)
            item_label = _normalize_item_label(category=category, color=color, item_label=item_label, query=query)
            category = _normalize_item_category(category=category, item_label=item_label, query=query)
            query = build_item_query(category=category, color=color, item_label=item_label)
            normalized = DetectedOutfitItem(
                category=category,
                color=color,
                item_label=item_label,
                query=query,
            )
            dedupe_key = (normalized.category, normalized.color, normalized.item_label, normalized.query)
            if dedupe_key in seen:
                continue

            seen.add(dedupe_key)
            normalized_items.append(normalized)

        return normalized_items

    def _build_data_url(self, content: bytes) -> str:
        mime_type = guess_mime_type(content)
        encoded = base64.b64encode(content).decode("ascii")
        return f"data:{mime_type};base64,{encoded}"


def merge_detected_items(
    vision_items: list[DetectedOutfitItem],
    fallback_items: list[DetectedOutfitItem],
) -> list[DetectedOutfitItem]:
    merged_items: list[DetectedOutfitItem] = []
    fallback_by_category: dict[str, list[DetectedOutfitItem]] = {}

    for item in fallback_items:
        fallback_by_category.setdefault(item.category, []).append(item)

    vision_by_category: dict[str, list[DetectedOutfitItem]] = {}
    for item in vision_items:
        category = _reassign_category_with_fallback(item, fallback_by_category)
        normalized_item = item if category == item.category else DetectedOutfitItem(
            category=category,
            color=item.color,
            item_label=item.item_label,
            query=build_item_query(category=category, color=item.color, item_label=item.item_label),
        )
        vision_by_category.setdefault(category, []).append(normalized_item)

    covered_categories: set[str] = set()
    for category, items in vision_by_category.items():
        if category == "accessory":
            merged_items.extend(items)
            covered_categories.add(category)
            continue

        primary_item = items[0]
        fallback_candidates = fallback_by_category.get(category, [])
        if fallback_candidates:
            primary_item = _reconcile_with_fallback(primary_item, fallback_candidates[0])
        merged_items.append(primary_item)
        covered_categories.add(category)

    for item in fallback_items:
        if item.category in covered_categories:
            continue
        merged_items.append(item)
        covered_categories.add(item.category)

    ordered_categories = ("top", "outer", "bottom", "shoes", "bag", "accessory")
    order_map = {category: index for index, category in enumerate(ordered_categories)}
    return [
        item
        for _, item in sorted(
            enumerate(merged_items),
            key=lambda pair: (order_map.get(pair[1].category, len(order_map)), pair[0]),
        )
    ]


def build_item_query(category: str, color: str, item_label: str) -> str:
    color_prefix = COLOR_QUERY_LABELS.get(color, "")
    category_label = CATEGORY_QUERY_LABELS.get(category, category)
    normalized_label = item_label.strip() or category_label
    if category == "accessory":
        family = _item_family(normalized_label)
        if family in {"목걸이", "귀걸이", "팔찌", "반지"}:
            if color == "gray":
                color_prefix = "실버"
            elif color == "yellow":
                color_prefix = "골드"
    if color_prefix and color_prefix not in normalized_label:
        return f"{color_prefix} {normalized_label}".strip()
    return normalized_label


def _reconcile_with_fallback(vision_item: DetectedOutfitItem, fallback_item: DetectedOutfitItem) -> DetectedOutfitItem:
    if vision_item.category != fallback_item.category:
        return vision_item

    vision_family = _item_family(vision_item.item_label)
    fallback_family = _item_family(fallback_item.item_label)
    if vision_item.category == "bottom":
        if vision_family in {"데님 팬츠", "와이드 데님 팬츠"} and fallback_family in {"데님 팬츠", "와이드 데님 팬츠"}:
            if _specificity_score(fallback_item.item_label) >= _specificity_score(vision_item.item_label):
                return fallback_item
        if vision_family in {"와이드 팬츠", "팬츠", "바지"} and fallback_family in {"와이드 팬츠", "팬츠", "바지", "슬랙스"}:
            if _specificity_score(fallback_item.item_label) > _specificity_score(vision_item.item_label):
                return fallback_item

    if vision_item.category == "bag":
        if vision_family in {"숄더백", "크로스백", "토트백", "백팩", "가방"} and fallback_family in {"숄더백", "크로스백", "토트백", "백팩", "가방"}:
            if _specificity_score(fallback_item.item_label) > _specificity_score(vision_item.item_label):
                return fallback_item

    if vision_item.category == "outer" and vision_family == "가디건":
        if fallback_family == "가디건" and fallback_item.color not in {"unknown", "neutral"} and fallback_item.color != vision_item.color:
            return fallback_item

    if vision_family and fallback_family and vision_family != fallback_family:
        return vision_item

    if vision_item.category == "accessory" and fallback_family == vision_family and fallback_item.color != vision_item.color:
        return fallback_item

    if _specificity_score(fallback_item.item_label) > _specificity_score(vision_item.item_label) and fallback_family == vision_family:
        return fallback_item

    return vision_item


def _reassign_category_with_fallback(
    vision_item: DetectedOutfitItem,
    fallback_by_category: dict[str, list[DetectedOutfitItem]],
) -> str:
    family = _item_family(vision_item.item_label)
    if not family:
        return vision_item.category

    if vision_item.category == "top" and family in {"가디건", "니트 베스트", "베스트", "자켓", "레더 자켓", "점퍼", "코트", "원피스"}:
        fallback_outer = fallback_by_category.get("outer", [])
        if fallback_outer and _item_family(fallback_outer[0].item_label) == family:
            return "outer"

    if vision_item.category == "outer" and family in {"슬리브리스 탑", "블라우스", "셔츠", "티셔츠", "니트 탑", "탑"}:
        fallback_top = fallback_by_category.get("top", [])
        if fallback_top and _item_family(fallback_top[0].item_label) == family:
            return "top"

    return vision_item.category


def _item_family(item_label: str) -> str:
    label = item_label.strip()
    for family in (
        "가디건",
        "니트 베스트",
        "베스트",
        "자켓",
        "레더 자켓",
        "점퍼",
        "원피스",
        "슬리브리스 탑",
        "블라우스",
        "셔츠",
        "티셔츠",
        "니트 탑",
        "탑",
        "와이드 데님 팬츠",
        "데님 팬츠",
        "와이드 팬츠",
        "팬츠",
        "바지",
        "슬랙스",
        "스커트",
        "도트 미니 스커트",
        "플리츠 스커트",
        "레이스 스커트",
        "미니 스커트",
        "메리제인 슈즈",
        "스니커즈",
        "로퍼",
        "부츠",
        "숄더백",
        "크로스백",
        "토트백",
        "가방",
        "안경",
        "목걸이",
        "귀걸이",
        "머리끈",
        "양말",
        "벨트",
        "모자",
        "머플러",
    ):
        if family in label:
            return family
    return label


def _specificity_score(item_label: str) -> int:
    label = item_label.strip()
    score = len(label)
    if any(keyword in label for keyword in ("와이드", "브이넥", "스트라이프", "레이스", "플리츠", "슬리브리스", "메리제인", "레더", "도트")):
        score += 5
    return score


def _normalize_item_color(category: str, color: str, item_label: str, query: str) -> str:
    combined_text = " ".join(part for part in (item_label, query) if part).strip()
    inferred_color = infer_color_from_text(combined_text)
    if inferred_color != "unknown":
        return inferred_color
    if category == "accessory":
        if any(keyword in combined_text for keyword in ("실버", "은", "실버톤", "메탈")):
            return "gray"
        if any(keyword in combined_text for keyword in ("골드", "금", "골드톤")):
            return "yellow"
        if any(keyword in combined_text for keyword in ("목걸이", "네크리스", "귀걸이", "이어링", "팔찌", "브레이슬릿", "반지", "링")) and color in {"unknown", "neutral"}:
            return "gray"
    if category == "bottom" and any(keyword in combined_text for keyword in ("청바지", "데님")) and color in {"unknown", "neutral"}:
        return "blue"
    if color == "neutral":
        return "unknown"
    return color


def _normalize_item_label(category: str, color: str, item_label: str, query: str) -> str:
    combined_text = " ".join(part for part in (item_label, query) if part).strip()
    if not combined_text:
        return DEFAULT_ITEM_LABELS.get(category, {}).get(color, CATEGORY_QUERY_LABELS.get(category, category))

    if category == "bottom" and color in {"blue", "navy"}:
        if "와이드" in combined_text and "팬츠" in combined_text:
            return "와이드 데님 팬츠"
        if any(keyword in combined_text for keyword in ("팬츠", "바지")):
            return "데님 팬츠"

    for keywords, normalized_label in ITEM_LABEL_NORMALIZATION_RULES.get(category, ()):
        matcher = all if normalized_label in ALL_KEYWORD_NORMALIZATION_LABELS else any
        if matcher(keyword in combined_text for keyword in keywords):
            return normalized_label

    return item_label.strip() or DEFAULT_ITEM_LABELS.get(category, {}).get(color, CATEGORY_QUERY_LABELS.get(category, category))


def _normalize_item_category(category: str, item_label: str, query: str) -> str:
    combined_text = " ".join(part for part in (item_label, query) if part).strip()
    if category == "outer" and any(keyword in combined_text for keyword in ("숄더백", "크로스백", "토트백", "백팩", "가방")):
        return "bag"
    return category


def guess_mime_type(content: bytes) -> str:
    if content.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if content.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if content.startswith(b"RIFF") and content[8:12] == b"WEBP":
        return "image/webp"
    if content.startswith((b"GIF87a", b"GIF89a")):
        return "image/gif"
    return "application/octet-stream"


def summarize_provider_error(exc: Exception) -> str:
    if isinstance(exc, HTTPError):
        detail = ""
        try:
            detail = exc.read().decode("utf-8")
        except Exception:
            detail = ""
        return f"HTTP {exc.code} {exc.reason}: {detail}".strip()
    if isinstance(exc, URLError):
        return f"URL error: {exc.reason}"
    return str(exc)
