"""
Citation builder.

Builds citations for the final GraphRAG response.

This module collects citations from vector retrieval results and
knowledge graph retrieval results into a unified structure that can
be returned to the frontend.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.core.logging_config import get_logger
from app.retrieval.graph.graph_retriever import GraphResult
from app.retrieval.vector.vector_retriever import RetrievedChunk

logger = get_logger(__name__)


@dataclass(slots=True)
class Citation:
    """
    Represents a citation returned to the user.
    """

    source_type: str
    title: str
    reference: str
    confidence: float


class CitationBuilder:
    """
    Builds citations from retrieval results.
    """

    def build(
        self,
        vector_results: list[RetrievedChunk],
        graph_results: list[GraphResult],
    ) -> list[Citation]:
        """
        Build citations.

        Args:
            vector_results:
                Retrieved vector chunks.

            graph_results:
                Retrieved graph results.

        Returns:
            List of citations.
        """

        logger.info(
            "Building citations."
        )

        citations: list[Citation] = []

        # --------------------------------------------------
        # Vector citations
        # --------------------------------------------------

        for chunk in vector_results:

            metadata = chunk.metadata or {}

            citations.append(
                Citation(
                    source_type="vector",
                    title=metadata.get(
                        "file_name",
                        "Unknown Document",
                    ),
                    reference=(
                        f"Chunk "
                        f"{metadata.get('chunk_index', 0) + 1}"
                    ),
                    confidence=round(
                        chunk.score,
                        3,
                    ),
                )
            )

        # --------------------------------------------------
        # Graph citations
        # --------------------------------------------------

        for graph in graph_results:

            citations.append(
                Citation(
                    source_type="graph",
                    title=graph.entity_name,
                    reference=(
                        f"{graph.relationship} "
                        f"{graph.related_entity}"
                    ),
                    confidence=1.0,
                )
            )

        logger.info(
            "Generated %d citations.",
            len(citations),
        )

        return citations


citation_builder = CitationBuilder()