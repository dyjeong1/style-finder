from __future__ import annotations

from fastapi.testclient import TestClient

from src.main import app


def test_core_e2e_flow() -> None:
    client = TestClient(app)

    upload_resp = client.post(
        "/images/upload",
        files={"image": ("outfit.png", b"fake-image-bytes", "image/png")},
    )
    assert upload_resp.status_code == 200
    upload_data = upload_resp.json()["data"]
    uploaded_image_id = upload_data["id"]
    assert upload_data["analysis"]["dominant_tone"] in {"warm", "cool", "neutral"}
    assert upload_data["analysis"]["style_mood"] in {"minimal", "casual", "street", "feminine"}
    assert len(upload_data["analysis"]["preferred_categories"]) >= 1

    rec_resp = client.get(
        "/recommendations",
        params={"uploaded_image_id": uploaded_image_id, "limit": 3},
    )
    assert rec_resp.status_code == 200
    rec_items = rec_resp.json()["data"]["items"]
    assert len(rec_items) >= 1
    assert "score_breakdown" in rec_items[0]
    assert "matched_signals" in rec_items[0]
    first_product_id = rec_items[0]["product_id"]

    add_wishlist_resp = client.post(
        "/wishlist",
        json={"product_id": first_product_id},
    )
    assert add_wishlist_resp.status_code == 200

    list_wishlist_resp = client.get("/wishlist")
    assert list_wishlist_resp.status_code == 200
    wishlist_items = list_wishlist_resp.json()["data"]["items"]
    matched_item = next((item for item in wishlist_items if item["product_id"] == first_product_id), None)
    assert matched_item is not None
    assert matched_item["product_name"]
    assert matched_item["source"] in {"zigzag", "29cm"}
    assert matched_item["category"] in {"top", "bottom", "outer", "shoes", "bag"}
    assert matched_item["price"] > 0
    assert matched_item["product_url"].startswith("https://")

    delete_wishlist_resp = client.delete(f"/wishlist/{first_product_id}")
    assert delete_wishlist_resp.status_code == 204

    list_after_delete_resp = client.get("/wishlist")
    assert list_after_delete_resp.status_code == 200
    wishlist_items_after_delete = list_after_delete_resp.json()["data"]["items"]
    assert all(item["product_id"] != first_product_id for item in wishlist_items_after_delete)
