from __future__ import annotations

import base64
from dataclasses import dataclass, field
import json
import logging
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from src.services.image_analysis import CATEGORY_QUERY_LABELS, COLOR_QUERY_LABELS, DEFAULT_ITEM_LABELS, DetectedOutfitItem


OPENAI_ALLOWED_CATEGORIES = ("top", "outer", "bottom", "shoes", "bag", "accessory")
OPENAI_ALLOWED_COLORS = tuple(COLOR_QUERY_LABELS) + ("neutral", "unknown")
GEMINI_GENERATE_CONTENT_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
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
        if not self.config.enabled or not content:
            return []
        if len(content) > self.config.max_image_bytes:
            return []

        provider = (self.config.provider or "disabled").lower()
        if provider == "mock":
            return list(self.mock_items)
        if provider == "openai":
            try:
                return self._analyze_with_openai(content)
            except Exception as exc:
                logger.warning("OpenAI Vision provider fallback: %s", summarize_provider_error(exc))
                return []
        if provider == "gemini":
            try:
                return self._analyze_with_gemini(content)
            except Exception as exc:
                logger.warning("Gemini Vision provider fallback: %s", summarize_provider_error(exc))
                return []

        # 실제 비전 provider 연동은 다음 TASK에서 연결한다.
        return []

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

            query = str(raw_item.get("query", "")).strip() or build_item_query(category=category, color=color, item_label=item_label)
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
    covered_categories: set[str] = set()

    for item in vision_items:
        merged_items.append(item)
        covered_categories.add(item.category)
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
    if color_prefix and color_prefix not in normalized_label:
        return f"{color_prefix} {normalized_label}".strip()
    return normalized_label


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
