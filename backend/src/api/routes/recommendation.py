from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional

from src.core.auth import get_current_user
from src.core.config import get_settings
from src.core.response import ok_response
from src.services.auth_service import AuthUser
from src.services.naver_shopping import (
    NaverShoppingClient,
    NaverShoppingConfig,
    NaverShoppingSearchResult,
    build_custom_naver_category_queries,
    build_custom_naver_query,
    build_naver_category_queries,
    build_naver_query,
)
from src.services.store import ProductRecord, UploadAnalysis
from src.services.store import store

router = APIRouter()


def _search_naver_candidates(
    client: NaverShoppingClient,
    analysis: UploadAnalysis,
    category: str | None,
    limit: int,
    custom_query: str | None = None,
) -> tuple[list[ProductRecord], str, str | None, str | None]:
    if category:
        query = build_custom_naver_query(custom_query, category) if custom_query else build_naver_query(analysis, category)
        result = client.search(query=query, category=category, limit=limit)
        return result.products, query, result.fallback_reason, result.fallback_message

    category_queries = build_custom_naver_category_queries(custom_query) if custom_query else build_naver_category_queries(analysis)
    per_category_limit = max(3, (limit + len(category_queries) - 1) // len(category_queries))
    query_label = " / ".join(query for _, query in category_queries)
    fallback_result: NaverShoppingSearchResult | None = None
    products_by_id: dict[str, ProductRecord] = {}

    for item_category, query in category_queries:
        result = client.search(query=query, category=item_category, limit=per_category_limit)
        if fallback_result is None and result.fallback_reason:
            fallback_result = result

        for product in result.products:
            products_by_id.setdefault(product.id, product)

    fallback_reason = fallback_result.fallback_reason if fallback_result and not products_by_id else None
    fallback_message = fallback_result.fallback_message if fallback_result and not products_by_id else None
    return list(products_by_id.values()), query_label, fallback_reason, fallback_message


@router.get("")
def get_recommendations(
    uploaded_image_id: str = Query(...),
    category: Optional[str] = Query(default=None),
    min_price: Optional[int] = Query(default=None, ge=0),
    max_price: Optional[int] = Query(default=None, ge=0),
    sort: str = Query(default="similarity_desc"),
    limit: int = Query(default=30, ge=1, le=100),
    custom_query: Optional[str] = Query(default=None, min_length=1, max_length=80),
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
    normalized_custom_query = " ".join(custom_query.split()) if custom_query else None
    settings = get_settings()
    naver_client = NaverShoppingClient(
        NaverShoppingConfig(
            client_id=settings.naver_shopping_client_id,
            client_secret=settings.naver_shopping_client_secret,
            display=settings.naver_shopping_display,
            timeout_seconds=settings.naver_shopping_timeout_seconds,
        )
    )
    naver_products, query, fallback_reason, fallback_message = _search_naver_candidates(
        client=naver_client,
        analysis=upload.analysis,
        category=category,
        limit=limit,
        custom_query=normalized_custom_query,
    )

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
            "fallback_reason": fallback_reason,
            "fallback_message": fallback_message,
        }
    )
