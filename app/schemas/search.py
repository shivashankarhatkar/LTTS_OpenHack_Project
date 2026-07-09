"""
Search API schemas.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class SearchRequest(BaseModel):
    """
    Enterprise search request.
    """

    query: str = Field(
        ...,
        min_length=1,
        description="Search query.",
    )

    top_k: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Maximum number of results.",
    )


class SearchResult(BaseModel):
    """
    Single search result.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    document_id: str

    file_name: str

    chunk_id: str

    content: str

    score: float

    metadata: dict


class SearchResponse(BaseModel):
    """
    Enterprise search response.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    query: str

    total_results: int

    results: list[SearchResult]