"""
Vector retriever.

Performs semantic retrieval using ChromaDB.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.connectors.chroma_connector import chroma_connector
from app.core.logging_config import get_logger
from app.embeddings.sentence_transformer_embedder import embedder
from app.vector_store.chromadb.chroma_repository import (
    chroma_repository,
)

logger = get_logger(__name__)


@dataclass(slots=True)
class RetrievedChunk:
    """
    Represents a retrieved document chunk.
    """

    document: str
    metadata: dict
    score: float


class VectorRetriever:
    """
    Performs semantic similarity search.
    """

    def __init__(self) -> None:
        self._repository = chroma_repository
        self._embedder = embedder

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[RetrievedChunk]:
        """
        Retrieve the most relevant document chunks.

        Args:
            query: User query.
            top_k: Maximum number of results.

        Returns:
            Ranked retrieved chunks.
        """
        logger.info(
            "Performing semantic retrieval for query: %s",
            query,
        )

        query_embedding = self._embedder.embed(query)

        results = self._repository.similarity_search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        retrieved_chunks: list[RetrievedChunk] = []

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances,
        ):
            score = max(0.0, 1.0 - float(distance))

            retrieved_chunks.append(
                RetrievedChunk(
                    document=document,
                    metadata=metadata,
                    score=score,
                )
            )

        logger.info(
            "Retrieved %d document chunks.",
            len(retrieved_chunks),
        )

        return retrieved_chunks


vector_retriever = VectorRetriever()