"""
Application configuration.

This module provides centralized configuration management for the
Enterprise Knowledge Assistant. All application settings are loaded
from environment variables or a .env file using Pydantic Settings.

Every component in the application should access configuration through
the singleton `settings` object defined at the bottom of this module.
"""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# Base project directory
BASE_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    """
    Centralized application settings.

    Values are loaded from environment variables first and then from
    the project's .env file.
    """

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------
    APP_NAME: str = Field(
        default="Enterprise Knowledge Assistant",
        description="Application name.",
    )

    APP_VERSION: str = Field(
        default="1.0.0",
        description="Application version.",
    )

    APP_DESCRIPTION: str = Field(
        default="Enterprise Knowledge Graph + Hybrid GraphRAG Platform",
        description="Application description.",
    )

    DEBUG: bool = Field(
        default=True,
        description="Enable debug mode.",
    )

    ENVIRONMENT: str = Field(
        default="development",
        description="Current application environment.",
    )

    HOST: str = Field(
        default="0.0.0.0",
        description="Application host.",
    )

    PORT: int = Field(
        default=8000,
        description="Application port.",
    )

    API_PREFIX: str = Field(
        default="/api/v1",
        description="API prefix.",
    )

    # ------------------------------------------------------------------
    # Gemini
    # ------------------------------------------------------------------
    gemini_api_key: str = Field(
        default="",
        validation_alias="GEMINI_API_KEY",
        )

    gemini_model: str = Field(
        default="gemini-2.5-flash",
        validation_alias="GEMINI_MODEL",
    )

    GEMINI_TEMPERATURE: float = Field(
        default=0.2,
        ge=0.0,
        le=2.0,
        description="LLM temperature.",
    )

    GEMINI_MAX_OUTPUT_TOKENS: int = Field(
        default=4096,
        description="Maximum output tokens.",
    )

    # ------------------------------------------------------------------
    # Neo4j
    # ------------------------------------------------------------------
    NEO4J_URI: str = Field(
        default="",
        description="Neo4j connection URI.",
    )

    NEO4J_USERNAME: str = Field(
        default="neo4j",
        description="Neo4j username.",
    )

    NEO4J_PASSWORD: str = Field(
        default="",
        description="Neo4j password.",
    )

    NEO4J_DATABASE: str = Field(
        default="neo4j",
        description="Neo4j database.",
    )

    # ------------------------------------------------------------------
    # ChromaDB
    # ------------------------------------------------------------------
    # ==========================================================
    # ChromaDB
    # ==========================================================

    CHROMA_DB_PATH: str = Field(
        default="./data/chroma",
        description="Local ChromaDB storage path.",
    )

    CHROMA_COLLECTION: str = Field(
        default="enterprise_documents",
        description="Chroma collection name.",
    )

    # ------------------------------------------------------------------
    # Embedding Model
    # ------------------------------------------------------------------
    EMBEDDING_MODEL: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        description="Embedding model.",
    )

    # ------------------------------------------------------------------
    # Uploads
    # ------------------------------------------------------------------
    UPLOAD_DIRECTORY: Path = Field(
        default=BASE_DIR / "data" / "uploads",
        description="Document upload directory.",
    )

    MAX_UPLOAD_SIZE_MB: int = Field(
        default=100,
        description="Maximum upload size.",
    )

    # ------------------------------------------------------------------
    # Chunking
    # ------------------------------------------------------------------
    CHUNK_SIZE: int = Field(
        default=1000,
        description="Chunk size.",
    )

    CHUNK_OVERLAP: int = Field(
        default=200,
        description="Chunk overlap.",
    )

    # ------------------------------------------------------------------
    # JWT Authentication
    # ------------------------------------------------------------------
    JWT_SECRET_KEY: str = Field(
        default="change_this_in_production",
        description="JWT signing key.",
    )

    JWT_ALGORITHM: str = Field(
        default="HS256",
        description="JWT algorithm.",
    )

    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=60,
        description="Access token expiry.",
    )

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------
    LOG_LEVEL: str = Field(
        default="INFO",
        description="Logging level.",
    )

    LOG_FILE: Path = Field(
        default=BASE_DIR / "logs" / "application.log",
        description="Application log file.",
    )

    # ------------------------------------------------------------------
    # Memory
    # ------------------------------------------------------------------
    MAX_CHAT_HISTORY: int = Field(
        default=20,
        description="Maximum conversation history.",
    )

    # ------------------------------------------------------------------
    # CORS
    # ------------------------------------------------------------------
    ALLOWED_ORIGINS: list[str] = Field(
        default=["*"],
        description="Allowed CORS origins.",
    )

    # ------------------------------------------------------------------
    # Helper Properties
    # ------------------------------------------------------------------
    @property
    def chroma_path(self) -> str:
        """
        Return the local ChromaDB storage path.
        """
        return self.CHROMA_DB_PATH


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Return a cached Settings instance.

    Returns:
        Singleton Settings object.
    """
    return Settings()


settings = get_settings()