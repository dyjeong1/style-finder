from pydantic import BaseModel, EmailStr, Field
from fastapi import APIRouter, HTTPException

from src.core.response import ok_response
from src.services.auth_service import auth_service

router = APIRouter()


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


@router.post("/login")
def login(payload: LoginRequest) -> dict:
    try:
        access_token, expires_in = auth_service.login(payload.email, payload.password)
    except ValueError as exc:
        if str(exc) == "invalid_credentials":
            raise HTTPException(
                status_code=401,
                detail={
                    "code": "AUTH_LOGIN_FAILED",
                    "message": "Invalid email or password.",
                    "detail": {},
                },
            )
        raise

    return ok_response(
        {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": expires_in,
        }
    )
