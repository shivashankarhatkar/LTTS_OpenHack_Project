"""
Keyword retriever.

Maintains an in-memory BM25 index for enterprise documents.
New documents are added incrementally during ingestion.
"""

from __future__ import annotations

from threading import Lock

from rank_bm25 import BM25Okapi

from app.core.logging_config import get_logger

logger = get_logger(__name__)


class KeywordRetriever:
    """
    BM25 keyword retriever.

    The retriever maintains an in-memory BM25 index that is updated
    whenever new document chunks are ingested.
    """

    def __init__(self) -> None:

        self._documents: list[str] = []
        self._metadatas: list[dict] = []
        self._document_ids: set[str] = set()

        self._bm25: BM25Okapi | None = None

        self._lock = Lock()

    def index(
        self,
        ids: list[str],
        documents: list[str],
        metadatas: list[dict],
    ) -> None:
        """
        Add new chunks to the BM25 index.

        Existing chunks are skipped.

        Args:
            ids:
                Chunk ids.

            documents:
                Chunk texts.

            metadatas:
                Chunk metadata.
        """

        with self._lock:

            added = 0

            for chunk_id, document, metadata in zip(
                ids,
                documents,
                metadatas,
            ):

                if chunk_id in self._document_ids:
                    continue

                self._document_ids.add(
                    chunk_id,
                )

                self._documents.append(
                    document,
                )

                self._metadatas.append(
                    metadata,
                )

                added += 1

            if added == 0:
                logger.info(
                    "No new chunks added to BM25."
                )
                return

            corpus = [
                document.lower().split()
                for document in self._documents
            ]

            self._bm25 = BM25Okapi(
                corpus,
            )

            logger.info(
                "BM25 index updated. "
                "Total indexed chunks: %d",
                len(self._documents),
            )

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:
        """
        Perform keyword search.

        Args:
            query:
                User query.

            top_k:
                Maximum number of results.

        Returns:
            Ranked keyword search results.
        """

        if (
            self._bm25 is None
            or not self._documents
        ):
            return []

        scores = self._bm25.get_scores(
            query.lower().split(),
        )

        ranked = sorted(
            enumerate(scores),
            key=lambda item: item[1],
            reverse=True,
        )[:top_k]

        results: list[dict] = []

        for index, score in ranked:

            results.append(
                {
                    "document": self._documents[index],
                    "metadata": self._metadatas[index],
                    "score": float(score),
                }
            )

        logger.info(
            "Keyword retrieval returned %d results.",
            len(results),
        )

        return results

    def count(self) -> int:
        """
        Return indexed chunk count.
        """

        return len(self._documents)

    def clear(self) -> None:
        """
        Clear the BM25 index.
        """

        with self._lock:

            self._documents.clear()
            self._metadatas.clear()
            self._document_ids.clear()

            self._bm25 = None

            logger.info(
                "BM25 index cleared."
            )


keyword_retriever = KeywordRetriever()