"""
Confidence scorer.

Calculates an overall confidence score for the generated answer based on
retrieval quality.
"""

from __future__ import annotations

from app.core.logging_config import get_logger
from app.retrieval.graph.graph_retriever import GraphResult
from app.retrieval.vector.vector_retriever import RetrievedChunk

logger = get_logger(__name__)


class ConfidenceScorer:
    """
    Calculates answer confidence.
    """

    def calculate(
        self,
        vector_results: list[RetrievedChunk],
        graph_results: list[GraphResult],
    ) -> float:
        """
        Calculate confidence score.

        Args:
            vector_results:
                Retrieved vector results.

            graph_results:
                Retrieved graph results.

        Returns:
            Confidence score between 0.0 and 1.0.
        """

        logger.info(
            "Calculating confidence score."
        )

        vector_score = 0.0

        if vector_results:

            vector_score = (
                sum(
                    chunk.score
                    for chunk in vector_results
                )
                / len(vector_results)
            )

        graph_score = 0.0

        if graph_results:
            graph_score = 1.0

        confidence = (
            (0.7 * vector_score)
            + (0.3 * graph_score)
        )

        confidence = max(
            0.0,
            min(
                confidence,
                1.0,
            ),
        )

        logger.info(
            "Confidence score: %.3f",
            confidence,
        )

        return confidence


confidence_scorer = ConfidenceScorer()