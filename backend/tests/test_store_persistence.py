from __future__ import annotations

from pathlib import Path

from src.services.store import InMemoryStore


def test_wishlist_persists_to_file(tmp_path: Path) -> None:
    wishlist_file = tmp_path / "wishlist.json"

    store = InMemoryStore(wishlist_store_path=wishlist_file)
    assert store.add_wishlist(user_id="local-user", product_id="prd-top-001") is True
    assert wishlist_file.exists()

    reloaded_store = InMemoryStore(wishlist_store_path=wishlist_file)
    persisted_items = reloaded_store.list_wishlist(user_id="local-user", category=None)

    assert len(persisted_items) == 1
    assert persisted_items[0]["product_id"] == "prd-top-001"
    assert persisted_items[0]["product_name"] == "오버핏 스트라이프 셔츠"


def test_wishlist_remove_updates_persisted_file(tmp_path: Path) -> None:
    wishlist_file = tmp_path / "wishlist.json"

    store = InMemoryStore(wishlist_store_path=wishlist_file)
    store.add_wishlist(user_id="local-user", product_id="prd-top-001")
    store.add_wishlist(user_id="local-user", product_id="prd-bag-001")

    assert store.remove_wishlist(user_id="local-user", product_id="prd-top-001") is True

    reloaded_store = InMemoryStore(wishlist_store_path=wishlist_file)
    persisted_items = reloaded_store.list_wishlist(user_id="local-user", category=None)

    assert [item["product_id"] for item in persisted_items] == ["prd-bag-001"]
