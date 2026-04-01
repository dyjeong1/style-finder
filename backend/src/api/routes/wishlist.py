from fastapi import APIRouter, Depends

from src.core.auth import get_current_user
from src.services.auth_service import AuthUser

router = APIRouter()


@router.get("")
def get_wishlist(_: AuthUser = Depends(get_current_user)) -> dict:
    return {
        "data": {"items": []},
        "error": None,
        "meta": {},
    }
