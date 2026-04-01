from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from secrets import token_urlsafe

from src.core.config import get_settings


@dataclass
class AuthUser:
    user_id: str
    email: str
    role: str


class AuthService:
    def __init__(self) -> None:
        self._tokens: dict[str, dict] = {}

    def login(self, email: str, password: str) -> tuple[str, int]:
        settings = get_settings()
        if email != settings.dev_login_email or password != settings.dev_login_password:
            raise ValueError("invalid_credentials")

        token = token_urlsafe(32)
        expires_at = datetime.now(timezone.utc) + timedelta(seconds=settings.access_token_expires_in)
        self._tokens[token] = {
            "user": AuthUser(
                user_id="dev-user-001",
                email=email,
                role="admin",
            ),
            "expires_at": expires_at,
        }
        return token, settings.access_token_expires_in

    def get_user_by_token(self, token: str) -> AuthUser | None:
        token_payload = self._tokens.get(token)
        if token_payload is None:
            return None

        if datetime.now(timezone.utc) >= token_payload["expires_at"]:
            self._tokens.pop(token, None)
            return None

        return token_payload["user"]


auth_service = AuthService()
