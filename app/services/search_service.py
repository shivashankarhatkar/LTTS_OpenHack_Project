"""
Search service.

Provides enterprise search functionality using the configured
Hybrid Retriever.
"""

from __future__ import annotations

from app.core.logging_config import get_logger
from app.retrieval.hybrid_retriever import hybrid_retriever
from app.schemas.search import (
    SearchResponse,
    SearchResult,
)

logger = get_logger(__name__)


class SearchService:
    """
    Enterprise search service.
    """

    def search(
        self,
        query: str,
        top_k: int = 10,
    ) -> SearchResponse:
        """
        Execute enterprise search.

        Args:
            query:
                Search query.

            top_k:
                Maximum number of results.

        Returns:
            SearchResponse.
        """

        logger.info(
            "Executing search for query: %s",
            query,
        )

        retrieval_results = hybrid_retriever.retrieve(
            query=query,
            top_k=top_k,
        )

        results: list[SearchResult] = []

        for result in retrieval_results:

            results.append(
                SearchResult(
                    document_id=result.document_id,
                    file_name=result.metadata.get(
                        "file_name",
                        "",
                    ),
                    chunk_id=result.chunk_id,
                    content=result.content,
                    score=result.score,
                    metadata=result.metadata,
                )
            )

        logger.info(
            "Search completed with %d results.",
            len(results),
        )

        return SearchResponse(
            query=query,
            total_results=len(results),
            results=results,
        )


search_service = SearchService()