"""
Result reranker.
"""

from __future__ import annotations


class Reranker:
    """
    Confidence-based reranking.
    """

    def rerank(
        self,
        vector_results: list,
    ) -> list:
        """
        Sort retrieved chunks by confidence.
        """

        return sorted(
            vector_results,
            key=lambda result: result.score,
            reverse=True,
        )


reranker = Reranker()