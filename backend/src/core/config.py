from __future__ import annotations

from functools import lru_cache
import os
from pathlib import Path
from typing import Optional

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


ENV_FILE_PATH = Path(__file__).resolve().parents[2] / ".env"


def _read_env_file_values(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}

    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


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
    ollama_api_key: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("OLLAMA_API_KEY"),
    )
    openai_api_key: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("OPENAI_API_KEY"),
    )
    vision_outfit_analyzer_enabled: bool = Field(
        default=False,
        validation_alias=AliasChoices(
            "VISION_OUTFIT_ANALYZER_ENABLED",
            "OPENAI_VISION_ENABLED",
            "GEMINI_VISION_ENABLED",
            "OLLAMA_VISION_ENABLED",
        ),
    )
    vision_outfit_analyzer_provider: str = Field(
        default="disabled",
        validation_alias=AliasChoices(
            "VISION_OUTFIT_ANALYZER_PROVIDER",
            "OPENAI_VISION_PROVIDER",
            "GEMINI_VISION_PROVIDER",
            "OLLAMA_VISION_PROVIDER",
        ),
    )
    vision_outfit_analyzer_model_name: str = Field(
        default="",
        validation_alias=AliasChoices(
            "VISION_OUTFIT_ANALYZER_MODEL_NAME",
            "OPENAI_VISION_MODEL",
            "GEMINI_VISION_MODEL",
            "OLLAMA_VISION_MODEL",
        ),
    )
    vision_outfit_analyzer_max_image_bytes: int = Field(
        default=2_000_000,
        validation_alias=AliasChoices(
            "VISION_OUTFIT_ANALYZER_MAX_IMAGE_BYTES",
            "OPENAI_VISION_MAX_IMAGE_BYTES",
            "GEMINI_VISION_MAX_IMAGE_BYTES",
            "OLLAMA_VISION_MAX_IMAGE_BYTES",
        ),
    )
    vision_outfit_analyzer_timeout_seconds: float = Field(
        default=20.0,
        validation_alias=AliasChoices(
            "VISION_OUTFIT_ANALYZER_TIMEOUT_SECONDS",
            "OPENAI_VISION_TIMEOUT_SECONDS",
            "GEMINI_VISION_TIMEOUT_SECONDS",
            "OLLAMA_VISION_TIMEOUT_SECONDS",
        ),
    )
    vision_outfit_analyzer_api_base_url: str = Field(
        default="",
        validation_alias=AliasChoices(
            "VISION_OUTFIT_ANALYZER_API_BASE_URL",
            "OPENAI_VISION_API_BASE_URL",
            "OPENAI_API_BASE_URL",
            "GEMINI_VISION_API_BASE_URL",
            "OLLAMA_VISION_API_BASE_URL",
            "OLLAMA_API_BASE_URL",
        ),
    )
    vision_outfit_analyzer_gemini_correction_enabled: bool = Field(
        default=True,
        validation_alias=AliasChoices(
            "VISION_OUTFIT_ANALYZER_GEMINI_CORRECTION_ENABLED",
            "GEMINI_CORRECTION_ENABLED",
        ),
    )

    model_config = SettingsConfigDict(env_file=str(ENV_FILE_PATH), env_file_encoding="utf-8")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


def resolve_vision_outfit_analyzer_runtime_config(
    settings: Settings,
    provider_override: str | None = None,
    env_values: dict[str, str] | None = None,
) -> dict[str, object]:
    provider = (provider_override or settings.vision_outfit_analyzer_provider or "disabled").lower()
    env_file_values = _read_env_file_values(ENV_FILE_PATH) if env_values is None else env_values

    def lookup_env(key: str) -> str | None:
        value = os.getenv(key)
        if value not in (None, ""):
            return value
        return env_file_values.get(key)

    def resolve_value(common_key: str, provider_key: str, fallback: object) -> object:
        provider_value = lookup_env(provider_key)
        if provider_value not in (None, ""):
            return provider_value
        common_value = lookup_env(common_key)
        if common_value not in (None, ""):
            return common_value
        return fallback

    def resolve_int_value(common_key: str, provider_key: str, fallback: int) -> int:
        resolved = resolve_value(common_key, provider_key, fallback)
        try:
            return int(resolved)
        except (TypeError, ValueError):
            return fallback

    def resolve_float_value(common_key: str, provider_key: str, fallback: float) -> float:
        resolved = resolve_value(common_key, provider_key, fallback)
        try:
            return float(resolved)
        except (TypeError, ValueError):
            return fallback

    if provider == "gemini":
        model_name = resolve_value(
            "VISION_OUTFIT_ANALYZER_MODEL_NAME",
            "GEMINI_VISION_MODEL",
            "gemini-2.5-flash",
        )
        api_base_url = resolve_value(
            "VISION_OUTFIT_ANALYZER_API_BASE_URL",
            "GEMINI_VISION_API_BASE_URL",
            "",
        )
        api_key = settings.gemini_api_key
        max_image_bytes = resolve_int_value(
            "VISION_OUTFIT_ANALYZER_MAX_IMAGE_BYTES",
            "GEMINI_VISION_MAX_IMAGE_BYTES",
            2_000_000,
        )
        timeout_seconds = resolve_float_value(
            "VISION_OUTFIT_ANALYZER_TIMEOUT_SECONDS",
            "GEMINI_VISION_TIMEOUT_SECONDS",
            20.0,
        )
    elif provider == "ollama":
        model_name = resolve_value(
            "VISION_OUTFIT_ANALYZER_MODEL_NAME",
            "OLLAMA_VISION_MODEL",
            "gemma3:4b",
        )
        api_base_url = resolve_value(
            "VISION_OUTFIT_ANALYZER_API_BASE_URL",
            "OLLAMA_API_BASE_URL",
            "",
        )
        api_key = settings.ollama_api_key
        max_image_bytes = resolve_int_value(
            "VISION_OUTFIT_ANALYZER_MAX_IMAGE_BYTES",
            "OLLAMA_VISION_MAX_IMAGE_BYTES",
            2_000_000,
        )
        timeout_seconds = resolve_float_value(
            "VISION_OUTFIT_ANALYZER_TIMEOUT_SECONDS",
            "OLLAMA_VISION_TIMEOUT_SECONDS",
            90.0,
        )
    elif provider == "openai":
        model_name = resolve_value(
            "VISION_OUTFIT_ANALYZER_MODEL_NAME",
            "OPENAI_VISION_MODEL",
            "gpt-4o",
        )
        api_base_url = resolve_value(
            "VISION_OUTFIT_ANALYZER_API_BASE_URL",
            "OPENAI_API_BASE_URL",
            "",
        )
        api_key = settings.openai_api_key
        max_image_bytes = resolve_int_value(
            "VISION_OUTFIT_ANALYZER_MAX_IMAGE_BYTES",
            "OPENAI_VISION_MAX_IMAGE_BYTES",
            2_000_000,
        )
        timeout_seconds = resolve_float_value(
            "VISION_OUTFIT_ANALYZER_TIMEOUT_SECONDS",
            "OPENAI_VISION_TIMEOUT_SECONDS",
            20.0,
        )
    else:
        model_name = settings.vision_outfit_analyzer_model_name
        api_base_url = settings.vision_outfit_analyzer_api_base_url
        api_key = None
        max_image_bytes = settings.vision_outfit_analyzer_max_image_bytes
        timeout_seconds = settings.vision_outfit_analyzer_timeout_seconds

    return {
        "enabled": settings.vision_outfit_analyzer_enabled,
        "provider": provider,
        "model_name": model_name,
        "max_image_bytes": max_image_bytes,
        "timeout_seconds": timeout_seconds,
        "api_base_url": api_base_url,
        "api_key": api_key,
    }
