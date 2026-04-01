from fastapi import APIRouter, Depends

from src.core.auth import get_current_user
from src.services.auth_service import AuthUser

router = APIRouter()


@router.post("/upload")
def upload_image(_: AuthUser = Depends(get_current_user)) -> dict:
    return {
        "data": {"message": "TODO: implement image upload"},
        "error": None,
        "meta": {},
    }
