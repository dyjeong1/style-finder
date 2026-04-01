from fastapi import APIRouter

from src.api.routes.auth import router as auth_router
from src.api.routes.health import router as health_router
from src.api.routes.recommendation import router as recommendation_router
from src.api.routes.upload import router as upload_router
from src.api.routes.wishlist import router as wishlist_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["Health"])
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(upload_router, prefix="/images", tags=["Upload"])
api_router.include_router(recommendation_router, prefix="/recommendations", tags=["Recommendation"])
api_router.include_router(wishlist_router, prefix="/wishlist", tags=["Wishlist"])
