"""Application exception hierarchy.

Defines a single base error, :class:`AppError`, from which every domain-
specific exception derives. Each error carries an HTTP status code and a stable
machine-readable ``error_code`` so the API layer can translate exceptions into
consistent responses without leaking internals.
"""

from __future__ import annotations


class AppError(Exception):
    """Base class for all application errors.

    Attributes:
        message: Human-readable description of the failure.
        error_code: Stable, machine-readable identifier for the error type.
        status_code: HTTP status code the API layer should return.
    """

    error_code: str = "app_error"
    status_code: int = 500

    def __init__(
        self,
        message: str,
        *,
        error_code: str | None = None,
        status_code: int | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        if error_code is not None:
            self.error_code = error_code
        if status_code is not None:
            self.status_code = status_code

    def __str__(self) -> str:
        return f"[{self.error_code}] {self.message}"


class ConfigurationError(AppError):
    """Raised when the application is misconfigured (missing/invalid settings)."""

    error_code = "configuration_error"
    status_code = 500


class NotFoundError(AppError):
    """Raised when a requested resource does not exist."""

    error_code = "not_found"
    status_code = 404


class ValidationError(AppError):
    """Raised when input fails domain validation."""

    error_code = "validation_error"
    status_code = 422


class IngestionError(AppError):
    """Raised when document ingestion or parsing fails."""

    error_code = "ingestion_error"
    status_code = 500


class RetrievalError(AppError):
    """Raised when hybrid/graph/vector/keyword retrieval fails."""

    error_code = "retrieval_error"
    status_code = 500


class LLMError(AppError):
    """Raised when the Gemini LLM call fails or returns an invalid result."""

    error_code = "llm_error"
    status_code = 502


class GraphError(AppError):
    """Raised for Neo4j knowledge-graph operation failures."""

    error_code = "graph_error"
    status_code = 502


class VectorStoreError(AppError):
    """Raised for ChromaDB vector-store operation failures."""

    error_code = "vector_store_error"
    status_code = 502


class AuthenticationError(AppError):
    """Raised when a request cannot be authenticated."""

    error_code = "authentication_error"
    status_code = 401


class AuthorizationError(AppError):
    """Raised when an authenticated principal lacks required permissions."""

    error_code = "authorization_error"
    status_code = 403