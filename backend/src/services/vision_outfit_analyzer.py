from __future__ import annotations

from dataclasses import dataclass, field

from src.services.image_analysis import DetectedOutfitItem


@dataclass(frozen=True)
class VisionOutfitAnalyzerConfig:
    enabled: bool = False
    provider: str = "disabled"
    model_name: str = ""
    max_image_bytes: int = 2_000_000


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

        # 실제 비전 provider 연동은 다음 TASK에서 연결한다.
        return []


def merge_detected_items(
    vision_items: list[DetectedOutfitItem],
    fallback_items: list[DetectedOutfitItem],
) -> list[DetectedOutfitItem]:
    merged_by_category: dict[str, DetectedOutfitItem] = {}

    for item in vision_items:
        merged_by_category.setdefault(item.category, item)
    for item in fallback_items:
        merged_by_category.setdefault(item.category, item)

    ordered_categories = ("top", "outer", "bottom", "shoes", "bag", "accessory")
    return [merged_by_category[category] for category in ordered_categories if category in merged_by_category]
