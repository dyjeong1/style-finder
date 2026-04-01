from fastapi import APIRouter

router = APIRouter()


@router.post("/upload")
def upload_image() -> dict:
    return {
        "data": {"message": "TODO: implement image upload"},
        "error": None,
        "meta": {},
    }
