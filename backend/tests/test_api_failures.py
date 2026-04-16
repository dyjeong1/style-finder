from __future__ import annotations

from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def _upload_image() -> str:
    response = client.post(
        "/images/upload",
        files={"image": ("case.png", b"dummy-bytes", "image/png")},
    )
    assert response.status_code == 200
    return response.json()["data"]["id"]


def test_upload_rejects_non_image_file() -> None:
    response = client.post(
        "/images/upload",
        files={"image": ("notes.txt", b"not-an-image", "text/plain")},
    )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "VALIDATION_INVALID_PARAM"


def test_recommendation_invalid_param() -> None:
    uploaded_image_id = _upload_image()

    response = client.get(
        "/recommendations",
        params={
            "uploaded_image_id": uploaded_image_id,
            "min_price": 90000,
            "max_price": 1000,
        },
    )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "VALIDATION_INVALID_PARAM"


def test_wishlist_duplicate_and_delete_not_found() -> None:
    uploaded_image_id = _upload_image()

    rec_response = client.get(
        "/recommendations",
        params={"uploaded_image_id": uploaded_image_id, "limit": 1},
    )
    assert rec_response.status_code == 200
    product_id = rec_response.json()["data"]["items"][0]["product_id"]

    # cleanup for deterministic test run
    client.delete(f"/wishlist/{product_id}")

    first_add = client.post("/wishlist", json={"product_id": product_id})
    assert first_add.status_code == 200

    second_add = client.post("/wishlist", json={"product_id": product_id})
    assert second_add.status_code == 409
    assert second_add.json()["error"]["code"] == "WISHLIST_ALREADY_EXISTS"

    deleted = client.delete(f"/wishlist/{product_id}")
    assert deleted.status_code == 204

    deleted_again = client.delete(f"/wishlist/{product_id}")
    assert deleted_again.status_code == 404
    assert deleted_again.json()["error"]["code"] == "WISHLIST_NOT_FOUND"


def test_recommendation_changes_by_uploaded_image_features() -> None:
    first_upload = client.post(
        "/images/upload",
        files={"image": ("cool-look.png", b"cool-minimal-look", "image/png")},
    )
    second_upload = client.post(
        "/images/upload",
        files={"image": ("warm-look.png", b"warm-street-look-with-layer", "image/png")},
    )

    assert first_upload.status_code == 200
    assert second_upload.status_code == 200

    first_id = first_upload.json()["data"]["id"]
    second_id = second_upload.json()["data"]["id"]

    first_rec = client.get("/recommendations", params={"uploaded_image_id": first_id, "limit": 3})
    second_rec = client.get("/recommendations", params={"uploaded_image_id": second_id, "limit": 3})

    assert first_rec.status_code == 200
    assert second_rec.status_code == 200

    first_items = first_rec.json()["data"]["items"]
    second_items = second_rec.json()["data"]["items"]

    assert [item["similarity_score"] for item in first_items] != [item["similarity_score"] for item in second_items]
    assert first_upload.json()["data"]["analysis"] != second_upload.json()["data"]["analysis"]
