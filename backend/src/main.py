from fastapi import FastAPI

from src.api.router import api_router
from src.core.config import get_settings
from src.core.errors import register_exception_handlers
from src.core.logger import configure_logging


settings = get_settings()
configure_logging(settings.log_level)

app = FastAPI(
    title="StyleMatch Backend",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

register_exception_handlers(app)
app.include_router(api_router)
