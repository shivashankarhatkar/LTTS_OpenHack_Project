"""
Chat API schemas.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ChatRequest(BaseModel):
    """
    User chat request.
    """

    query: str = Field(
        ...,
        min_length=1,
        description="User question.",
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Maximum number of retrieval results.",
    )


class CitationSchema(BaseModel):
    """
    Citation returned with the answer.
    """

    model_config = ConfigDict(from_attributes=True)

    source_type: str
    title: str
    reference: str
    confidence: float


class ChatResponse(BaseModel):
    """
    Chat response returned by the Enterprise Knowledge Assistant.
    """

    model_config = ConfigDict(from_attributes=True)

    answer: str

    citations: list[CitationSchema]

    confidence: float

    validation_message: str

    is_valid: bool