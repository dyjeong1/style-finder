from fastapi import APIRouter

router = APIRouter()


@router.get("")
def get_wishlist() -> dict:
    return {
        "data": {"items": []},
        "error": None,
        "meta": {},
    }
