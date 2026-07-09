"""
Health check response schema.
"""

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """
    Health check response.
    """

    status: str = Field(
        ...,
        description="Current application status.",
        examples=["healthy"],
    )

    application: str = Field(
        ...,
        description="Application name.",
    )

    version: str = Field(
        ...,
        description="Application version.",
    )

    environment: str = Field(
        ...,
        description="Current environment.",
    )

    message: str = Field(
        ...,
        description="Health message.",
    )