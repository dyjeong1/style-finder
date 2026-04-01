from fastapi import APIRouter

router = APIRouter()


@router.post("/login")
def login() -> dict:
    return {
        "data": {"message": "TODO: implement login"},
        "error": None,
        "meta": {},
    }
