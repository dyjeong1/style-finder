from fastapi import APIRouter

router = APIRouter()


@router.get("")
def get_recommendations() -> dict:
    return {
        "data": {"items": []},
        "error": None,
        "meta": {},
    }
