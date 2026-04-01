from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import uuid4


@dataclass
class UploadedImageRecord:
    id: str
    user_id: str
    image_url: str
    filename: str
    content_type: str
    size_bytes: int
    created_at: str


@dataclass
class ProductRecord:
    id: str
    source: str
    product_name: str
    category: str
    price: int
    product_url: str
    image_url: str


class InMemoryStore:
    def __init__(self) -> None:
        self.uploads: dict[str, UploadedImageRecord] = {}
        self.products: dict[str, ProductRecord] = self._seed_products()
        self.wishlist_by_user: dict[str, set[str]] = {}

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
            ),
            ProductRecord(
                id="prd-bottom-001",
                source="29cm",
                product_name="와이드 데님 팬츠",
                category="bottom",
                price=59000,
                product_url="https://example.com/products/prd-bottom-001",
                image_url="https://example.com/images/prd-bottom-001.jpg",
            ),
            ProductRecord(
                id="prd-outer-001",
                source="zigzag",
                product_name="크롭 블루종 자켓",
                category="outer",
                price=89000,
                product_url="https://example.com/products/prd-outer-001",
                image_url="https://example.com/images/prd-outer-001.jpg",
            ),
            ProductRecord(
                id="prd-shoes-001",
                source="29cm",
                product_name="레더 스니커즈",
                category="shoes",
                price=99000,
                product_url="https://example.com/products/prd-shoes-001",
                image_url="https://example.com/images/prd-shoes-001.jpg",
            ),
            ProductRecord(
                id="prd-bag-001",
                source="zigzag",
                product_name="미니 숄더백",
                category="bag",
                price=45000,
                product_url="https://example.com/products/prd-bag-001",
                image_url="https://example.com/images/prd-bag-001.jpg",
            ),
            ProductRecord(
                id="prd-top-002",
                source="29cm",
                product_name="베이직 니트 탑",
                category="top",
                price=32000,
                product_url="https://example.com/products/prd-top-002",
                image_url="https://example.com/images/prd-top-002.jpg",
            ),
        ]
        return {item.id: item for item in seeded}

    def create_upload(
        self,
        user_id: str,
        filename: str,
        content_type: str,
        size_bytes: int,
    ) -> UploadedImageRecord:
        upload_id = str(uuid4())
        created_at = datetime.now(timezone.utc).isoformat()
        image_url = f"/mock-storage/{upload_id}-{filename}"

        record = UploadedImageRecord(
            id=upload_id,
            user_id=user_id,
            image_url=image_url,
            filename=filename,
            content_type=content_type,
            size_bytes=size_bytes,
            created_at=created_at,
        )
        self.uploads[upload_id] = record
        return record

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
    ) -> list[dict]:
        if uploaded_image_id not in self.uploads:
            return []

        items = list(self.products.values())
        if category:
            items = [item for item in items if item.category == category]
        if min_price is not None:
            items = [item for item in items if item.price >= min_price]
        if max_price is not None:
            items = [item for item in items if item.price <= max_price]

        scored: list[dict] = []
        for idx, item in enumerate(items):
            # mock score for deterministic sorting
            similarity = round(max(0.1, 0.95 - (idx * 0.08)), 4)
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

    def has_product(self, product_id: str) -> bool:
        return product_id in self.products

    def add_wishlist(self, user_id: str, product_id: str) -> bool:
        if user_id not in self.wishlist_by_user:
            self.wishlist_by_user[user_id] = set()

        user_wishlist = self.wishlist_by_user[user_id]
        if product_id in user_wishlist:
            return False

        user_wishlist.add(product_id)
        return True

    def remove_wishlist(self, user_id: str, product_id: str) -> bool:
        user_wishlist = self.wishlist_by_user.get(user_id)
        if not user_wishlist or product_id not in user_wishlist:
            return False

        user_wishlist.remove(product_id)
        return True

    def list_wishlist(self, user_id: str, category: str | None) -> list[dict]:
        user_wishlist = self.wishlist_by_user.get(user_id, set())
        items: list[dict] = []
        for product_id in user_wishlist:
            product = self.products.get(product_id)
            if product is None:
                continue
            if category and product.category != category:
                continue
            items.append(
                {
                    "id": f"wsh-{product.id}",
                    "product_id": product.id,
                    "created_at": datetime.now(timezone.utc).isoformat(),
                }
            )

        items.sort(key=lambda x: x["product_id"])
        return items


store = InMemoryStore()
