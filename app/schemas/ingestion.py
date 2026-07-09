"""
Schemas for document ingestion.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class IngestionResponse(BaseModel):
    """
    Response returned after successful document ingestion.
    """

    model_config = ConfigDict(from_attributes=True)

    file_name: str
    file_type: str
    language: str
    total_chunks: int
    character_count: int
    word_count: int
    message: str