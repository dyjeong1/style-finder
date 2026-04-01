from datetime import datetime, timezone

from fastapi import APIRouter

from src.core.config import get_settings

router = APIRouter()


@router.get("/health")
def health() -> dict:
    settings = get_settings()
    return {
        "data": {
            "status": "ok",
            "service": settings.service_name,
        },
        "error": None,
        "meta": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    }
