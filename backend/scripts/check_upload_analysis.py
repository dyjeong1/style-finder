from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.core.config import get_settings, resolve_vision_outfit_analyzer_runtime_config
from src.services.store import InMemoryStore, VisionOutfitAnalyzer, VisionOutfitAnalyzerConfig


def main() -> int:
    parser = argparse.ArgumentParser(description="단일 이미지의 업로드 분석 결과를 확인")
    parser.add_argument("--image", required=True, help="분석할 이미지 경로")
    parser.add_argument("--user-id", default="local-user", help="업로드 사용자 ID")
    parser.add_argument(
        "--provider",
        default=None,
        choices=("openai", "gemini", "ollama"),
        help="특정 비전 provider로 강제 실행",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=None,
        help="이번 실행에만 적용할 provider 타임아웃(초)",
    )
    args = parser.parse_args()

    image_path = Path(args.image)
    if not image_path.exists():
        raise SystemExit(f"이미지 파일이 없습니다: {image_path}")

    settings = get_settings()
    runtime_config = resolve_vision_outfit_analyzer_runtime_config(settings, provider_override=args.provider)
    store = InMemoryStore(
        vision_outfit_analyzer=VisionOutfitAnalyzer(
            VisionOutfitAnalyzerConfig(
                enabled=bool(runtime_config["enabled"]),
                provider=str(runtime_config["provider"]),
                model_name=str(runtime_config["model_name"]),
                max_image_bytes=int(runtime_config["max_image_bytes"]),
                timeout_seconds=float(args.timeout_seconds or runtime_config["timeout_seconds"]),
                api_base_url=str(runtime_config["api_base_url"]),
                api_key=str(runtime_config["api_key"]) if runtime_config["api_key"] is not None else None,
            )
        )
    )

    content = image_path.read_bytes()
    record = store.create_upload(
        user_id=args.user_id,
        filename=image_path.name,
        content_type=_guess_content_type(image_path),
        size_bytes=len(content),
        content=content,
    )

    payload = {
        "id": record.id,
        "image_url": record.image_url,
        "analysis": {
            "dominant_tone": record.analysis.dominant_tone,
            "dominant_color": record.analysis.dominant_color,
            "style_mood": record.analysis.style_mood,
            "silhouette": record.analysis.silhouette,
            "preferred_categories": list(record.analysis.preferred_categories),
            "category_query_hints": record.analysis.category_query_hints,
            "detected_items": [
                {
                    "category": item.category,
                    "color": item.color,
                    "item_label": item.item_label,
                    "query": item.query,
                }
                for item in record.analysis.detected_items
            ],
        },
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def _guess_content_type(image_path: Path) -> str:
    suffix = image_path.suffix.lower()
    if suffix == ".png":
        return "image/png"
    if suffix in (".jpg", ".jpeg"):
        return "image/jpeg"
    if suffix == ".webp":
        return "image/webp"
    return "application/octet-stream"


if __name__ == "__main__":
    raise SystemExit(main())
