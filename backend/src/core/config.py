from __future__ import annotations

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    service_name: str = "stylematch-backend"
    env: str = "local"
    log_level: str = "INFO"

    dev_login_email: str = "admin@stylematch.com"
    dev_login_password: str = "stylematch1234"
    access_token_expires_in: int = 3600

    naver_shopping_client_id: Optional[str] = None
    naver_shopping_client_secret: Optional[str] = None
    naver_shopping_display: int = 30
    naver_shopping_timeout_seconds: float = 3.0

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
