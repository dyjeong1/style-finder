from __future__ import annotations

from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def _login_headers() -> dict:
    response = client.post(
        "/auth/login",
        json={"email": "admin@stylematch.com", "password": "stylematch1234"},
    )
    assert response.status_code == 200
    token = response.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _upload_image(headers: dict) -> str:
    response = client.post(
        "/images/upload",
        headers=headers,
        files={"image": ("case.png", b"dummy-bytes", "image/png")},
    )
    assert response.status_code == 200
    return response.json()["data"]["id"]


def test_auth_login_fail() -> None:
    response = client.post(
        "/auth/login",
        json={"email": "admin@stylematch.com", "password": "wrong-password"},
    )
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "AUTH_LOGIN_FAILED"


def test_protected_route_without_token() -> None:
    response = client.get("/wishlist")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "AUTH_UNAUTHORIZED"


def test_recommendation_invalid_param() -> None:
    headers = _login_headers()
    uploaded_image_id = _upload_image(headers)

    response = client.get(
        "/recommendations",
        headers=headers,
        params={
            "uploaded_image_id": uploaded_image_id,
            "min_price": 90000,
            "max_price": 1000,
        },
    )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "VALIDATION_INVALID_PARAM"


def test_wishlist_duplicate_and_delete_not_found() -> None:
    headers = _login_headers()
    uploaded_image_id = _upload_image(headers)

    rec_response = client.get(
        "/recommendations",
        headers=headers,
        params={"uploaded_image_id": uploaded_image_id, "limit": 1},
    )
    assert rec_response.status_code == 200
    product_id = rec_response.json()["data"]["items"][0]["product_id"]

    # cleanup for deterministic test run
    client.delete(f"/wishlist/{product_id}", headers=headers)

    first_add = client.post("/wishlist", headers=headers, json={"product_id": product_id})
    assert first_add.status_code == 200

    second_add = client.post("/wishlist", headers=headers, json={"product_id": product_id})
    assert second_add.status_code == 409
    assert second_add.json()["error"]["code"] == "WISHLIST_ALREADY_EXISTS"

    deleted = client.delete(f"/wishlist/{product_id}", headers=headers)
    assert deleted.status_code == 204

    deleted_again = client.delete(f"/wishlist/{product_id}", headers=headers)
    assert deleted_again.status_code == 404
    assert deleted_again.json()["error"]["code"] == "WISHLIST_NOT_FOUND"
