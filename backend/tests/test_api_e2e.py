from __future__ import annotations

from fastapi.testclient import TestClient

from src.main import app


def test_core_e2e_flow() -> None:
    client = TestClient(app)

    login_resp = client.post(
        "/auth/login",
        json={"email": "admin@stylematch.com", "password": "stylematch1234"},
    )
    assert login_resp.status_code == 200
    login_data = login_resp.json()["data"]
    token = login_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    upload_resp = client.post(
        "/images/upload",
        headers=headers,
        files={"image": ("outfit.png", b"fake-image-bytes", "image/png")},
    )
    assert upload_resp.status_code == 200
    upload_data = upload_resp.json()["data"]
    uploaded_image_id = upload_data["id"]

    rec_resp = client.get(
        "/recommendations",
        headers=headers,
        params={"uploaded_image_id": uploaded_image_id, "limit": 3},
    )
    assert rec_resp.status_code == 200
    rec_items = rec_resp.json()["data"]["items"]
    assert len(rec_items) >= 1
    first_product_id = rec_items[0]["product_id"]

    add_wishlist_resp = client.post(
        "/wishlist",
        headers=headers,
        json={"product_id": first_product_id},
    )
    assert add_wishlist_resp.status_code == 200

    list_wishlist_resp = client.get("/wishlist", headers=headers)
    assert list_wishlist_resp.status_code == 200
    wishlist_items = list_wishlist_resp.json()["data"]["items"]
    assert any(item["product_id"] == first_product_id for item in wishlist_items)

    delete_wishlist_resp = client.delete(f"/wishlist/{first_product_id}", headers=headers)
    assert delete_wishlist_resp.status_code == 204

    list_after_delete_resp = client.get("/wishlist", headers=headers)
    assert list_after_delete_resp.status_code == 200
    wishlist_items_after_delete = list_after_delete_resp.json()["data"]["items"]
    assert all(item["product_id"] != first_product_id for item in wishlist_items_after_delete)
