from __future__ import annotations

from functools import lru_cache
from typing import Optional

from pydantic import AliasChoices, Field
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
    gemini_api_key: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("GEMINI_API_KEY"),
    )
    openai_api_key: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("OPENAI_API_KEY"),
    )
    vision_outfit_analyzer_enabled: bool = Field(
        default=False,
        validation_alias=AliasChoices("VISION_OUTFIT_ANALYZER_ENABLED", "OPENAI_VISION_ENABLED", "GEMINI_VISION_ENABLED"),
    )
    vision_outfit_analyzer_provider: str = Field(
        default="disabled",
        validation_alias=AliasChoices("VISION_OUTFIT_ANALYZER_PROVIDER", "OPENAI_VISION_PROVIDER", "GEMINI_VISION_PROVIDER"),
    )
    vision_outfit_analyzer_model_name: str = Field(
        default="",
        validation_alias=AliasChoices("VISION_OUTFIT_ANALYZER_MODEL_NAME", "OPENAI_VISION_MODEL", "GEMINI_VISION_MODEL"),
    )
    vision_outfit_analyzer_max_image_bytes: int = Field(
        default=2_000_000,
        validation_alias=AliasChoices(
            "VISION_OUTFIT_ANALYZER_MAX_IMAGE_BYTES",
            "OPENAI_VISION_MAX_IMAGE_BYTES",
            "GEMINI_VISION_MAX_IMAGE_BYTES",
        ),
    )
    vision_outfit_analyzer_timeout_seconds: float = Field(
        default=20.0,
        validation_alias=AliasChoices(
            "VISION_OUTFIT_ANALYZER_TIMEOUT_SECONDS",
            "OPENAI_VISION_TIMEOUT_SECONDS",
            "GEMINI_VISION_TIMEOUT_SECONDS",
        ),
    )
    vision_outfit_analyzer_api_base_url: str = Field(
        default="",
        validation_alias=AliasChoices(
            "VISION_OUTFIT_ANALYZER_API_BASE_URL",
            "OPENAI_VISION_API_BASE_URL",
            "OPENAI_API_BASE_URL",
            "GEMINI_VISION_API_BASE_URL",
        ),
    )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
