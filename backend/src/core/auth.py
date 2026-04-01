from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.services.auth_service import AuthUser, auth_service

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> AuthUser:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=401,
            detail={
                "code": "AUTH_UNAUTHORIZED",
                "message": "Access token is missing or invalid.",
                "detail": {},
            },
        )

    user = auth_service.get_user_by_token(credentials.credentials)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail={
                "code": "AUTH_UNAUTHORIZED",
                "message": "Access token is missing or invalid.",
                "detail": {},
            },
        )

    return user
