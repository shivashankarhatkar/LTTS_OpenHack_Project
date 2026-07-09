"""
Search API endpoints.
"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status

from app.core.logging_config import get_logger
from app.schemas.search import (
    SearchRequest,
    SearchResponse,
)
from app.services.search_service import (
    search_service,
)

logger = get_logger(__name__)

router = APIRouter(
    prefix="/search",
    tags=["Search"],
)


@router.post(
    "",
    response_model=SearchResponse,
    status_code=status.HTTP_200_OK,
)
async def search(
    request: SearchRequest,
) -> SearchResponse:
    """
    Enterprise search endpoint.
    """

    try:

        logger.info(
            "Received search request."
        )

        return search_service.search(
            query=request.query,
            top_k=request.top_k,
        )

    except Exception as exc:

        logger.exception(
            "Search request failed."
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to execute search.",
        ) from exc