"""
Hybrid retriever.

Combines:

- Vector Retrieval
- Knowledge Graph Retrieval
- BM25 Keyword Retrieval
"""

from __future__ import annotations

from app.core.logging_config import get_logger
from app.retrieval.fusion.context_fusion import (
    context_fusion,
)
from app.retrieval.graph.graph_retriever import (
    graph_retriever,
)
from app.retrieval.keyword.keyword_retriever import (
    keyword_retriever,
)
from app.retrieval.rerank.reranker import (
    reranker,
)
from app.retrieval.vector.vector_retriever import (
    vector_retriever,
)

logger = get_logger(__name__)


class HybridRetriever:
    """
    Enterprise Hybrid Retrieval Engine.
    """

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> dict:
        """
        Perform hybrid retrieval.
        """

        logger.info(
            "Running hybrid retrieval."
        )

        graph_results = graph_retriever.retrieve(
            query,
            top_k,
        )

        vector_results = vector_retriever.retrieve(
            query,
            top_k,
        )

        keyword_results = keyword_retriever.retrieve(
            query,
            top_k,
        )

        vector_results = reranker.rerank(
            vector_results,
        )

        return context_fusion.fuse(
            graph_results=graph_results,
            vector_results=vector_results,
            keyword_results=keyword_results,
        )


hybrid_retriever = HybridRetriever()