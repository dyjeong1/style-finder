from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.core.response import error_response


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
        detail = exc.detail if isinstance(exc.detail, dict) else {}
        code = detail.get("code", f"HTTP_{exc.status_code}")
        message = detail.get("message", "Request failed.")
        detail_data = detail.get("detail", {})
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response(code=code, message=message, detail=detail_data),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=error_response(
                code="VALIDATION_INVALID_PARAM",
                message="Request validation failed.",
                detail={"errors": exc.errors()},
            ),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content=error_response(
                code="INTERNAL_SERVER_ERROR",
                message=str(exc),
                detail={},
            ),
        )
