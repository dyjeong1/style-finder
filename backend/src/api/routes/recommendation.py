from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional

from src.core.auth import get_current_user
from src.core.config import get_settings
from src.core.response import ok_response
from src.services.auth_service import AuthUser
from src.services.naver_shopping import NaverShoppingClient, NaverShoppingConfig, build_naver_query
from src.services.store import store

router = APIRouter()


@router.get("")
def get_recommendations(
    uploaded_image_id: str = Query(...),
    category: Optional[str] = Query(default=None),
    min_price: Optional[int] = Query(default=None, ge=0),
    max_price: Optional[int] = Query(default=None, ge=0),
    sort: str = Query(default="similarity_desc"),
    limit: int = Query(default=30, ge=1, le=100),
    _: AuthUser = Depends(get_current_user),
) -> dict:
    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "VALIDATION_INVALID_PARAM",
                "message": "max_price must be greater than or equal to min_price.",
                "detail": {"field": "max_price"},
            },
        )

    if sort not in {"similarity_desc", "price_asc", "price_desc"}:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "VALIDATION_INVALID_PARAM",
                "message": "sort must be one of similarity_desc, price_asc, price_desc.",
                "detail": {"field": "sort"},
            },
        )

    if store.get_upload(uploaded_image_id) is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "RECOMMENDATION_NOT_FOUND",
                "message": "Recommendation result does not exist for uploaded_image_id.",
                "detail": {"uploaded_image_id": uploaded_image_id},
            },
        )

    upload = store.get_upload(uploaded_image_id)
    settings = get_settings()
    naver_client = NaverShoppingClient(
        NaverShoppingConfig(
            client_id=settings.naver_shopping_client_id,
            client_secret=settings.naver_shopping_client_secret,
            display=settings.naver_shopping_display,
            timeout_seconds=settings.naver_shopping_timeout_seconds,
        )
    )
    query = build_naver_query(upload.analysis, category) if upload is not None else "패션 의류"
    naver_result = naver_client.search(query=query, category=category, limit=limit)
    naver_products = naver_result.products

    if naver_products:
        store.register_products(naver_products)

    items = store.list_recommendations(
        uploaded_image_id=uploaded_image_id,
        category=category,
        min_price=min_price,
        max_price=max_price,
        sort=sort,
        limit=limit,
        candidate_products=naver_products or None,
    )
    return ok_response(
        {
            "items": items,
            "total_count": len(items),
            "source": "naver_shopping" if naver_products else "mock",
            "query": query,
            "fallback_reason": naver_result.fallback_reason,
            "fallback_message": naver_result.fallback_message,
        }
    )
