"""
Chat API endpoints.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.core.logging_config import get_logger
from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    CitationSchema,
)
from app.services.chat_service import chat_service

logger = get_logger(__name__)

router = APIRouter(
    prefix="/chat",
    tags=["Enterprise Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
)
async def chat(
    request: ChatRequest,
) -> ChatResponse:
    """
    Ask a question to the Enterprise Knowledge Assistant.
    """

    try:

        result = chat_service.chat(
            query=request.query,
            top_k=request.top_k,
        )

        return ChatResponse(
            answer=result.answer,
            citations=[
                CitationSchema.model_validate(citation)
                for citation in result.citations
            ],
            confidence=result.confidence,
            validation_message=result.validation_message,
            is_valid=result.is_valid,
        )

    except Exception as exc:

        logger.exception(
            "Failed to process chat request."
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to process the chat request.",
        ) from exc