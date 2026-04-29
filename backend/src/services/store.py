from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
from uuid import uuid4

from src.core.config import get_settings, resolve_vision_outfit_analyzer_runtime_config
from src.services.image_analysis import (
    DetectedOutfitItem,
    analyze_outfit_category_query_hints,
    analyze_outfit_items,
    analyze_image_content,
    classify_rgb_color,
    fallback_color_from_digest,
    has_color_keyword,
    infer_color_from_text,
)
from src.services.vision_outfit_analyzer import (
    VisionOutfitAnalyzer,
    VisionOutfitAnalyzerConfig,
    merge_detected_items,
)


WARM_COLORS = {"beige", "brown", "red", "pink", "yellow"}
COOL_COLORS = {"blue", "navy", "green"}


@dataclass
class UploadAnalysis:
    checksum: str
    dominant_tone: str
    style_mood: str
    silhouette: str
    preferred_categories: tuple[str, ...]
    feature_vector: tuple[float, ...]
    dominant_color: str = "unknown"
    category_query_hints: dict[str, str] = field(default_factory=dict)
    detected_items: tuple[DetectedOutfitItem, ...] = ()


@dataclass
class UploadedImageRecord:
    id: str
    user_id: str
    image_url: str
    filename: str
    content_type: str
    size_bytes: int
    content: bytes
    created_at: str
    analysis: UploadAnalysis


@dataclass
class ProductRecord:
    id: str
    source: str
    product_name: str
    category: str
    price: int
    product_url: str
    image_url: str
    dominant_tone: str
    style_mood: str
    silhouette: str
    feature_vector: tuple[float, ...]
    dominant_color: str = "unknown"


class InMemoryStore:
    def __init__(
        self,
        wishlist_store_path: Path | None = None,
        vision_outfit_analyzer: VisionOutfitAnalyzer | None = None,
        gemini_correction_analyzer: VisionOutfitAnalyzer | None = None,
        enable_gemini_correction: bool = False,
    ) -> None:
        self.uploads: dict[str, UploadedImageRecord] = {}
        self.products: dict[str, ProductRecord] = self._seed_products()
        self.wishlist_store_path = wishlist_store_path or Path(__file__).resolve().parents[2] / "data" / "wishlist.json"
        self.wishlist_by_user: dict[str, dict[str, str]] = self._load_wishlist()
        self.vision_outfit_analyzer = vision_outfit_analyzer or VisionOutfitAnalyzer(VisionOutfitAnalyzerConfig())
        self.gemini_correction_analyzer = gemini_correction_analyzer
        self.enable_gemini_correction = enable_gemini_correction and gemini_correction_analyzer is not None

    def _load_wishlist(self) -> dict[str, dict[str, str]]:
        if not self.wishlist_store_path.exists():
            return {}

        try:
            raw_payload = json.loads(self.wishlist_store_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}

        if not isinstance(raw_payload, dict):
            return {}

        restored: dict[str, dict[str, str]] = {}
        for user_id, items in raw_payload.items():
            if not isinstance(user_id, str) or not isinstance(items, dict):
                continue

            restored[user_id] = {
                product_id: created_at
                for product_id, created_at in items.items()
                if isinstance(product_id, str) and isinstance(created_at, str)
            }

        return restored

    def _persist_wishlist(self) -> None:
        self.wishlist_store_path.parent.mkdir(parents=True, exist_ok=True)
        self.wishlist_store_path.write_text(
            json.dumps(self.wishlist_by_user, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _seed_products(self) -> dict[str, ProductRecord]:
        seeded = [
            ProductRecord(
                id="prd-top-001",
                source="zigzag",
                product_name="오버핏 스트라이프 셔츠",
                category="top",
                price=39000,
                product_url="https://example.com/products/prd-top-001",
                image_url="https://example.com/images/prd-top-001.jpg",
                dominant_tone="cool",
                style_mood="casual",
                silhouette="relaxed",
                feature_vector=(0.91, 0.58, 0.27, 0.73),
            ),
            ProductRecord(
                id="prd-bottom-001",
                source="29cm",
                product_name="와이드 데님 팬츠",
                category="bottom",
                price=59000,
                product_url="https://example.com/products/prd-bottom-001",
                image_url="https://example.com/images/prd-bottom-001.jpg",
                dominant_tone="cool",
                style_mood="minimal",
                silhouette="relaxed",
                feature_vector=(0.84, 0.22, 0.36, 0.64),
            ),
            ProductRecord(
                id="prd-outer-001",
                source="zigzag",
                product_name="크롭 블루종 자켓",
                category="outer",
                price=89000,
                product_url="https://example.com/products/prd-outer-001",
                image_url="https://example.com/images/prd-outer-001.jpg",
                dominant_tone="neutral",
                style_mood="street",
                silhouette="layered",
                feature_vector=(0.38, 0.92, 0.71, 0.42),
            ),
            ProductRecord(
                id="prd-shoes-001",
                source="29cm",
                product_name="레더 스니커즈",
                category="shoes",
                price=99000,
                product_url="https://example.com/products/prd-shoes-001",
                image_url="https://example.com/images/prd-shoes-001.jpg",
                dominant_tone="neutral",
                style_mood="minimal",
                silhouette="balanced",
                feature_vector=(0.19, 0.31, 0.95, 0.53),
            ),
            ProductRecord(
                id="prd-bag-001",
                source="zigzag",
                product_name="미니 숄더백",
                category="bag",
                price=45000,
                product_url="https://example.com/products/prd-bag-001",
                image_url="https://example.com/images/prd-bag-001.jpg",
                dominant_tone="warm",
                style_mood="feminine",
                silhouette="balanced",
                feature_vector=(0.67, 0.41, 0.88, 0.24),
            ),
            ProductRecord(
                id="prd-top-002",
                source="29cm",
                product_name="베이직 니트 탑",
                category="top",
                price=32000,
                product_url="https://example.com/products/prd-top-002",
                image_url="https://example.com/images/prd-top-002.jpg",
                dominant_tone="warm",
                style_mood="minimal",
                silhouette="slim",
                feature_vector=(0.55, 0.17, 0.61, 0.89),
            ),
        ]
        return {item.id: item for item in seeded}

    def create_upload(
        self,
        user_id: str,
        filename: str,
        content_type: str,
        size_bytes: int,
        content: bytes,
    ) -> UploadedImageRecord:
        upload_id = str(uuid4())
        created_at = datetime.now(timezone.utc).isoformat()
        image_url = f"/images/{upload_id}/file"
        analysis = self._analyze_upload(content=content, filename=filename, content_type=content_type)

        record = UploadedImageRecord(
            id=upload_id,
            user_id=user_id,
            image_url=image_url,
            filename=filename,
            content_type=content_type,
            size_bytes=size_bytes,
            content=content,
            created_at=created_at,
            analysis=analysis,
        )
        self.uploads[upload_id] = record
        return record

    def _analyze_upload(self, content: bytes, filename: str, content_type: str) -> UploadAnalysis:
        source = content or f"{filename}:{content_type}".encode()
        digest = hashlib.sha256(source).digest()

        image_color_feature = analyze_image_content(content)
        if image_color_feature is None:
            dominant_color = fallback_color_from_digest(digest)
            feature_vector = tuple(round((digest[idx] / 255), 4) for idx in range(4))
        else:
            dominant_color = image_color_feature.dominant_color
            feature_vector = image_color_feature.feature_vector

        rule_detected_items = analyze_outfit_items(content)
        vision_detected_items = self.vision_outfit_analyzer.analyze(content)
        detected_items = tuple(merge_detected_items(vision_detected_items, rule_detected_items))
        if self.enable_gemini_correction:
            correction_categories = select_gemini_correction_categories(
                vision_items=vision_detected_items,
                fallback_items=rule_detected_items,
                merged_items=detected_items,
            )
            if correction_categories:
                correction_items = self.gemini_correction_analyzer.analyze(content)
                if correction_items:
                    detected_items = tuple(
                        apply_selective_category_corrections(
                            base_items=detected_items,
                            correction_items=correction_items,
                            categories=correction_categories,
                        )
                    )
        category_query_hints: dict[str, str] = {}
        for item in detected_items:
            category_query_hints.setdefault(item.category, item.query)

        if not category_query_hints:
            category_query_hints = analyze_outfit_category_query_hints(content)
        preferred_categories = tuple(category_query_hints) or self._fallback_preferred_categories(digest)

        return UploadAnalysis(
            checksum=digest.hex()[:16],
            dominant_tone=self._derive_tone(dominant_color),
            style_mood=self._derive_mood(dominant_color, preferred_categories),
            silhouette=self._derive_silhouette(preferred_categories),
            preferred_categories=preferred_categories,
            feature_vector=feature_vector,
            dominant_color=dominant_color,
            category_query_hints=category_query_hints,
            detected_items=detected_items,
        )

    def _fallback_preferred_categories(self, digest: bytes) -> tuple[str, ...]:
        categories = ("top", "bottom", "outer", "shoes", "bag", "accessory")
        return tuple(
            dict.fromkeys(
                (
                    categories[digest[4] % len(categories)],
                    categories[digest[5] % len(categories)],
                )
            )
        )

    def _derive_tone(self, dominant_color: str) -> str:
        if dominant_color in WARM_COLORS:
            return "warm"
        if dominant_color in COOL_COLORS:
            return "cool"
        return "neutral"

    def _derive_mood(self, dominant_color: str, preferred_categories: tuple[str, ...]) -> str:
        if dominant_color in {"pink", "white", "beige"} and any(category in preferred_categories for category in {"bag", "accessory"}):
            return "feminine"
        if dominant_color in {"black", "gray", "navy"} and any(category in preferred_categories for category in {"outer", "shoes"}):
            return "street"
        if any(category in preferred_categories for category in {"bottom", "shoes"}):
            return "casual"
        return "minimal"

    def _derive_silhouette(self, preferred_categories: tuple[str, ...]) -> str:
        if "outer" in preferred_categories and "top" in preferred_categories:
            return "layered"
        if "bottom" in preferred_categories and "shoes" in preferred_categories:
            return "balanced"
        if "top" in preferred_categories:
            return "slim"
        return "relaxed"

    def _classify_rgb_color(self, red: float, green: float, blue: float) -> str:
        return classify_rgb_color(red, green, blue)

    def _cosine_similarity(self, left: tuple[float, ...], right: tuple[float, ...]) -> float:
        numerator = sum(a * b for a, b in zip(left, right))
        left_norm = math.sqrt(sum(a * a for a in left))
        right_norm = math.sqrt(sum(b * b for b in right))
        if left_norm == 0 or right_norm == 0:
            return 0.0
        return numerator / (left_norm * right_norm)

    def get_upload(self, upload_id: str) -> UploadedImageRecord | None:
        return self.uploads.get(upload_id)

    def list_recommendations(
        self,
        uploaded_image_id: str,
        category: str | None,
        min_price: int | None,
        max_price: int | None,
        sort: str,
        limit: int,
        candidate_products: list[ProductRecord] | None = None,
        vision_similarity_by_product: dict[str, float] | None = None,
    ) -> list[dict]:
        upload = self.uploads.get(uploaded_image_id)
        if upload is None:
            return []

        items = candidate_products or list(self.products.values())
        if category:
            items = [item for item in items if item.category == category]
        if min_price is not None:
            items = [item for item in items if item.price >= min_price]
        if max_price is not None:
            items = [item for item in items if item.price <= max_price]

        scored: list[dict] = []
        for item in items:
            vector_similarity = self._cosine_similarity(upload.analysis.feature_vector, item.feature_vector)
            tone_bonus = 0.08 if upload.analysis.dominant_tone == item.dominant_tone else 0.0
            mood_bonus = 0.06 if upload.analysis.style_mood == item.style_mood else 0.0
            silhouette_bonus = 0.05 if upload.analysis.silhouette == item.silhouette else 0.0
            category_bonus = 0.04 if item.category in upload.analysis.preferred_categories else 0.0
            category_target_color = infer_color_from_text(upload.analysis.category_query_hints.get(item.category, ""))
            target_color = category_target_color if category_target_color != "unknown" else upload.analysis.dominant_color
            color_bonus = 0.08 if has_color_keyword(item.product_name, target_color) else 0.0
            product_image_color_bonus = (
                0.12
                if item.dominant_color != "unknown" and item.dominant_color == target_color
                else 0.0
            )
            vision_similarity = (vision_similarity_by_product or {}).get(item.id, 0.0)
            vision_bonus = max(0.0, vision_similarity) * 0.18
            similarity = round(
                min(
                    0.99,
                    0.35
                    + (vector_similarity * 0.45)
                    + tone_bonus
                    + mood_bonus
                    + silhouette_bonus
                    + category_bonus
                    + color_bonus
                    + product_image_color_bonus
                    + vision_bonus
                ),
                4,
            )
            scored.append(
                {
                    "product_id": item.id,
                    "source": item.source,
                    "product_name": item.product_name,
                    "category": item.category,
                    "price": item.price,
                    "product_url": item.product_url,
                    "image_url": item.image_url,
                    "similarity_score": similarity,
                    "score_breakdown": {
                        "vector_similarity": round(vector_similarity, 4),
                        "tone_bonus": round(tone_bonus, 4),
                        "mood_bonus": round(mood_bonus, 4),
                        "silhouette_bonus": round(silhouette_bonus, 4),
                        "category_bonus": round(category_bonus, 4),
                        "color_bonus": round(color_bonus, 4),
                        "product_image_color_bonus": round(product_image_color_bonus, 4),
                        "vision_similarity": round(vision_similarity, 4),
                        "vision_bonus": round(vision_bonus, 4),
                    },
                    "matched_signals": {
                        "dominant_tone": upload.analysis.dominant_tone,
                        "dominant_color": upload.analysis.dominant_color,
                        "category_target_color": target_color,
                        "product_dominant_color": item.dominant_color,
                        "style_mood": upload.analysis.style_mood,
                        "silhouette": upload.analysis.silhouette,
                        "preferred_categories": list(upload.analysis.preferred_categories),
                        "vision_reranked": bool(vision_similarity_by_product and item.id in vision_similarity_by_product),
                    },
                }
            )

        if sort == "price_asc":
            scored.sort(key=lambda x: x["price"])
        elif sort == "price_desc":
            scored.sort(key=lambda x: x["price"], reverse=True)
        else:
            scored.sort(key=lambda x: x["similarity_score"], reverse=True)

        for rank, item in enumerate(scored, start=1):
            item["rank"] = rank

        return scored[:limit]

    def register_products(self, products: list[ProductRecord]) -> None:
        for product in products:
            self.products[product.id] = product

    def has_product(self, product_id: str) -> bool:
        return product_id in self.products

    def add_wishlist(self, user_id: str, product_id: str) -> bool:
        if user_id not in self.wishlist_by_user:
            self.wishlist_by_user[user_id] = {}

        user_wishlist = self.wishlist_by_user[user_id]
        if product_id in user_wishlist:
            return False

        user_wishlist[product_id] = datetime.now(timezone.utc).isoformat()
        self._persist_wishlist()
        return True

    def remove_wishlist(self, user_id: str, product_id: str) -> bool:
        user_wishlist = self.wishlist_by_user.get(user_id)
        if not user_wishlist or product_id not in user_wishlist:
            return False

        user_wishlist.pop(product_id, None)
        self._persist_wishlist()
        return True

    def list_wishlist(self, user_id: str, category: str | None) -> list[dict]:
        user_wishlist = self.wishlist_by_user.get(user_id, {})
        items: list[dict] = []
        for product_id, created_at in user_wishlist.items():
            product = self.products.get(product_id)
            if product is None:
                continue
            if category and product.category != category:
                continue
            items.append(
                {
                    "id": f"wsh-{product.id}",
                    "product_id": product.id,
                    "product_name": product.product_name,
                    "source": product.source,
                    "category": product.category,
                    "price": product.price,
                    "product_url": product.product_url,
                    "image_url": product.image_url,
                    "created_at": created_at,
                }
            )

        items.sort(key=lambda x: x["created_at"], reverse=True)
        return items


def select_gemini_correction_categories(
    vision_items: list[DetectedOutfitItem],
    fallback_items: list[DetectedOutfitItem],
    merged_items: tuple[DetectedOutfitItem, ...] | list[DetectedOutfitItem],
) -> tuple[str, ...]:
    target_order = ("top", "outer", "bottom", "accessory")
    generic_labels = {
        "top": {"탑", "셔츠", "티셔츠", "니트 탑", "블라우스"},
        "outer": {"가디건", "자켓", "점퍼", "베스트"},
        "bottom": {"팬츠", "바지", "데님 팬츠", "스커트"},
        "accessory": {"안경", "양말", "목걸이", "귀걸이"},
    }
    vision_by_category = _first_item_by_category(vision_items)
    fallback_by_category = _first_item_by_category(fallback_items)
    merged_categories = {item.category for item in merged_items}
    categories: list[str] = []

    if {"top", "outer"}.issubset(merged_categories):
        categories.extend(["top", "outer"])

    for category in target_order:
        vision_item = vision_by_category.get(category)
        fallback_item = fallback_by_category.get(category)

        if vision_item and fallback_item:
            if vision_item.color != fallback_item.color or vision_item.item_label != fallback_item.item_label:
                categories.append(category)
                continue

        item_to_check = vision_item or fallback_item
        if item_to_check and item_to_check.item_label in generic_labels.get(category, set()):
            categories.append(category)
            continue

        if not vision_item and fallback_item and category in {"top", "outer", "accessory"}:
            categories.append(category)

    return tuple(dict.fromkeys(category for category in categories if category in target_order))


def apply_selective_category_corrections(
    base_items: tuple[DetectedOutfitItem, ...] | list[DetectedOutfitItem],
    correction_items: list[DetectedOutfitItem],
    categories: tuple[str, ...],
) -> list[DetectedOutfitItem]:
    if not categories:
        return list(base_items)

    correction_by_category: dict[str, list[DetectedOutfitItem]] = {}
    for item in correction_items:
        if item.category in categories:
            correction_by_category.setdefault(item.category, []).append(item)

    if not correction_by_category:
        return list(base_items)

    result: list[DetectedOutfitItem] = []
    replaced: set[str] = set()
    for item in base_items:
        if item.category in correction_by_category:
            if item.category in replaced:
                continue
            result.extend(correction_by_category[item.category])
            replaced.add(item.category)
            continue
        result.append(item)

    for category in categories:
        if category in replaced:
            continue
        if category in correction_by_category:
            result.extend(correction_by_category[category])
            replaced.add(category)

    ordered_categories = ("top", "outer", "bottom", "shoes", "bag", "accessory")
    order_map = {category: index for index, category in enumerate(ordered_categories)}
    return [
        item
        for _, item in sorted(
            enumerate(result),
            key=lambda pair: (order_map.get(pair[1].category, len(order_map)), pair[0]),
        )
    ]


def _first_item_by_category(items: tuple[DetectedOutfitItem, ...] | list[DetectedOutfitItem]) -> dict[str, DetectedOutfitItem]:
    first_items: dict[str, DetectedOutfitItem] = {}
    for item in items:
        first_items.setdefault(item.category, item)
    return first_items

settings = get_settings()
vision_runtime_config = resolve_vision_outfit_analyzer_runtime_config(settings)
enable_gemini_correction = (
    bool(settings.vision_outfit_analyzer_gemini_correction_enabled)
    and bool(vision_runtime_config["enabled"])
    and str(vision_runtime_config["provider"]).lower() == "ollama"
    and bool(settings.gemini_api_key)
)
gemini_correction_runtime_config = (
    resolve_vision_outfit_analyzer_runtime_config(settings, provider_override="gemini")
    if enable_gemini_correction
    else None
)
store = InMemoryStore(
    vision_outfit_analyzer=VisionOutfitAnalyzer(
        VisionOutfitAnalyzerConfig(
            enabled=bool(vision_runtime_config["enabled"]),
            provider=str(vision_runtime_config["provider"]),
            model_name=str(vision_runtime_config["model_name"]),
            max_image_bytes=int(vision_runtime_config["max_image_bytes"]),
            timeout_seconds=float(vision_runtime_config["timeout_seconds"]),
            api_base_url=str(vision_runtime_config["api_base_url"]),
            api_key=(
                str(vision_runtime_config["api_key"])
                if vision_runtime_config["api_key"] is not None
                else None
            ),
        )
    ),
    gemini_correction_analyzer=(
        VisionOutfitAnalyzer(
            VisionOutfitAnalyzerConfig(
                enabled=bool(gemini_correction_runtime_config["enabled"]),
                provider=str(gemini_correction_runtime_config["provider"]),
                model_name=str(gemini_correction_runtime_config["model_name"]),
                max_image_bytes=int(gemini_correction_runtime_config["max_image_bytes"]),
                timeout_seconds=float(gemini_correction_runtime_config["timeout_seconds"]),
                api_base_url=str(gemini_correction_runtime_config["api_base_url"]),
                api_key=(
                    str(gemini_correction_runtime_config["api_key"])
                    if gemini_correction_runtime_config["api_key"] is not None
                    else None
                ),
            )
        )
        if gemini_correction_runtime_config is not None
        else None
    ),
    enable_gemini_correction=enable_gemini_correction,
)
