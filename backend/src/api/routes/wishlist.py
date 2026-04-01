from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel

from src.core.auth import get_current_user
from src.core.response import ok_response
from src.services.auth_service import AuthUser
from src.services.store import store

router = APIRouter()


class WishlistCreateRequest(BaseModel):
    product_id: str


@router.get("")
def get_wishlist(
    category: str | None = None,
    user: AuthUser = Depends(get_current_user),
) -> dict:
    items = store.list_wishlist(user_id=user.user_id, category=category)
    return ok_response({"items": items, "total_count": len(items)})


@router.post("")
def add_wishlist(
    payload: WishlistCreateRequest,
    user: AuthUser = Depends(get_current_user),
) -> dict:
    if not store.has_product(payload.product_id):
        raise HTTPException(
            status_code=404,
            detail={
                "code": "WISHLIST_PRODUCT_NOT_FOUND",
                "message": "Product does not exist.",
                "detail": {"product_id": payload.product_id},
            },
        )

    inserted = store.add_wishlist(user_id=user.user_id, product_id=payload.product_id)
    if not inserted:
        raise HTTPException(
            status_code=409,
            detail={
                "code": "WISHLIST_ALREADY_EXISTS",
                "message": "The product is already in wishlist.",
                "detail": {},
            },
        )

    items = store.list_wishlist(user_id=user.user_id, category=None)
    created = next((item for item in items if item["product_id"] == payload.product_id), None)
    return ok_response(created)


@router.delete("/{product_id}")
def remove_wishlist(
    product_id: str,
    user: AuthUser = Depends(get_current_user),
) -> Response:
    deleted = store.remove_wishlist(user_id=user.user_id, product_id=product_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "WISHLIST_NOT_FOUND",
                "message": "The wishlist item does not exist.",
                "detail": {},
            },
        )

    return Response(status_code=204)
