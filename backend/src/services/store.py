from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import colorsys
import hashlib
from io import BytesIO
import json
import math
from pathlib import Path
from uuid import uuid4

try:
    from PIL import Image
except ImportError:  # pragma: no cover - local fallback when Pillow is unavailable
    Image = None


@dataclass
class UploadAnalysis:
    checksum: str
    dominant_tone: str
    style_mood: str
    silhouette: str
    preferred_categories: tuple[str, ...]
    feature_vector: tuple[float, ...]
    dominant_color: str = "unknown"


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


COLOR_TITLE_KEYWORDS = {
    "black": ("블랙", "검정", "검은", "흑청"),
    "white": ("화이트", "아이보리", "크림", "오트밀", "흰색", "하얀"),
    "gray": ("그레이", "차콜", "회색", "실버"),
    "beige": ("베이지", "샌드", "카멜", "카키베이지"),
    "brown": ("브라운", "초코", "모카", "탄", "밤색"),
    "navy": ("네이비", "남색"),
    "blue": ("블루", "파랑", "소라", "스카이블루", "청"),
    "green": ("그린", "카키", "올리브", "민트"),
    "red": ("레드", "버건디", "와인"),
    "pink": ("핑크", "로즈"),
    "yellow": ("옐로우", "노랑", "머스타드"),
}


class InMemoryStore:
    def __init__(self, wishlist_store_path: Path | None = None) -> None:
        self.uploads: dict[str, UploadedImageRecord] = {}
        self.products: dict[str, ProductRecord] = self._seed_products()
        self.wishlist_store_path = wishlist_store_path or Path(__file__).resolve().parents[2] / "data" / "wishlist.json"
        self.wishlist_by_user: dict[str, dict[str, str]] = self._load_wishlist()

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

        tones = ("warm", "cool", "neutral")
        moods = ("minimal", "casual", "street", "feminine")
        silhouettes = ("relaxed", "slim", "layered", "balanced")
        categories = ("top", "bottom", "outer", "shoes", "bag")

        image_color_feature = self._extract_image_color_feature(content)
        if image_color_feature is None:
            dominant_color = self._fallback_color_from_digest(digest)
            feature_vector = tuple(round((digest[idx] / 255), 4) for idx in range(4))
        else:
            dominant_color = str(image_color_feature["dominant_color"])
            feature_vector = tuple(image_color_feature["feature_vector"])

        preferred_categories = tuple(
            dict.fromkeys(
                (
                    categories[digest[4] % len(categories)],
                    categories[digest[5] % len(categories)],
                )
            )
        )

        return UploadAnalysis(
            checksum=digest.hex()[:16],
            dominant_tone=tones[digest[0] % len(tones)],
            style_mood=moods[digest[1] % len(moods)],
            silhouette=silhouettes[digest[2] % len(silhouettes)],
            preferred_categories=preferred_categories,
            feature_vector=feature_vector,
            dominant_color=dominant_color,
        )

    def _extract_image_color_feature(self, content: bytes) -> dict[str, object] | None:
        if Image is None or not content:
            return None

        try:
            with Image.open(BytesIO(content)) as image:
                image = image.convert("RGB")
                image.thumbnail((96, 96))
                pixels = list(image.getdata())
        except Exception:
            return None

        if not pixels:
            return None

        sample_step = max(1, len(pixels) // 1800)
        sampled_pixels = pixels[::sample_step]
        red = sum(pixel[0] for pixel in sampled_pixels) / len(sampled_pixels)
        green = sum(pixel[1] for pixel in sampled_pixels) / len(sampled_pixels)
        blue = sum(pixel[2] for pixel in sampled_pixels) / len(sampled_pixels)
        brightness = (red + green + blue) / (255 * 3)
        saturation = colorsys.rgb_to_hsv(red / 255, green / 255, blue / 255)[1]

        return {
            "dominant_color": self._classify_rgb_color(red, green, blue),
            "feature_vector": (
                round(red / 255, 4),
                round(green / 255, 4),
                round(blue / 255, 4),
                round((brightness + saturation) / 2, 4),
            ),
        }

    def _classify_rgb_color(self, red: float, green: float, blue: float) -> str:
        hue, saturation, value = colorsys.rgb_to_hsv(red / 255, green / 255, blue / 255)
        hue_degrees = hue * 360

        if value < 0.22:
            return "black"
        if saturation < 0.12 and value > 0.86:
            return "white"
        if saturation < 0.16:
            return "gray"
        if 25 <= hue_degrees < 55 and saturation < 0.38 and value > 0.45:
            return "beige"
        if 15 <= hue_degrees < 45:
            return "brown"
        if 200 <= hue_degrees < 245 and value < 0.45:
            return "navy"
        if 185 <= hue_degrees < 255:
            return "blue"
        if 75 <= hue_degrees < 170:
            return "green"
        if 330 <= hue_degrees or hue_degrees < 15:
            return "red"
        if 280 <= hue_degrees < 330:
            return "pink"
        if 45 <= hue_degrees < 75:
            return "yellow"
        return "neutral"

    def _fallback_color_from_digest(self, digest: bytes) -> str:
        colors = ("black", "white", "gray", "beige", "brown", "navy", "blue", "green", "red", "pink", "yellow")
        return colors[digest[6] % len(colors)]

    def _has_color_keyword(self, product_name: str, dominant_color: str) -> bool:
        return any(keyword in product_name for keyword in COLOR_TITLE_KEYWORDS.get(dominant_color, ()))

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
            color_bonus = 0.08 if self._has_color_keyword(item.product_name, upload.analysis.dominant_color) else 0.0
            similarity = round(
                min(
                    0.99,
                    0.35
                    + (vector_similarity * 0.45)
                    + tone_bonus
                    + mood_bonus
                    + silhouette_bonus
                    + category_bonus
                    + color_bonus,
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
                    },
                    "matched_signals": {
                        "dominant_tone": upload.analysis.dominant_tone,
                        "dominant_color": upload.analysis.dominant_color,
                        "style_mood": upload.analysis.style_mood,
                        "silhouette": upload.analysis.silhouette,
                        "preferred_categories": list(upload.analysis.preferred_categories),
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


store = InMemoryStore()
