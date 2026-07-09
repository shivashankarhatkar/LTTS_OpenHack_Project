"""
Application entry point.

Creates and configures the FastAPI application.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging_config import get_logger, setup_logging

setup_logging()

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events.
    """
    logger.info("Starting Enterprise Knowledge Assistant...")

    yield

    logger.info("Shutting down Enterprise Knowledge Assistant...")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        Configured FastAPI instance.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=settings.APP_DESCRIPTION,
        lifespan=lifespan,
    )

    app.include_router(
        api_router,
        prefix=settings.API_PREFIX,
    )

    logger.info("Application initialized successfully.")

    return app


app = create_app()