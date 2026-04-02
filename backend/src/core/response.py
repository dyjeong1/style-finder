from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_meta(request_id: str | None = None) -> dict:
    return {
        "request_id": request_id or f"req_{uuid4().hex[:8]}",
        "timestamp": _timestamp(),
    }


def ok_response(data: dict | list | str | int | float | None, request_id: str | None = None) -> dict:
    return {
        "data": data,
        "error": None,
        "meta": build_meta(request_id),
    }


def error_response(code: str, message: str, detail: dict | None = None, request_id: str | None = None) -> dict:
    return {
        "data": None,
        "error": {
            "code": code,
            "message": message,
            "detail": detail or {},
        },
        "meta": build_meta(request_id),
    }
