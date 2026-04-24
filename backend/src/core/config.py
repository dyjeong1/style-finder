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
    naver_shopping_analyze_product_images: bool = True
    naver_shopping_image_timeout_seconds: float = 1.0
    naver_shopping_max_image_bytes: int = 2_000_000
    naver_shopping_max_product_image_analysis_count: int = 12
    vision_reranker_enabled: bool = False
    vision_reranker_provider: str = "clip"
    vision_reranker_model_name: str = "openai/clip-vit-base-patch32"
    vision_reranker_timeout_seconds: float = 1.5
    vision_reranker_max_image_bytes: int = 2_000_000
    vision_reranker_max_candidates: int = 10
    vision_outfit_analyzer_enabled: bool = False
    vision_outfit_analyzer_provider: str = "disabled"
    vision_outfit_analyzer_model_name: str = ""
    vision_outfit_analyzer_max_image_bytes: int = 2_000_000

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
