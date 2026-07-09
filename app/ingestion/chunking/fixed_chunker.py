"""
Fixed-size document chunker.
"""

from __future__ import annotations

from app.core.config import settings
from app.core.logging_config import get_logger
from app.ingestion.chunking.base_chunker import BaseChunker

logger = get_logger(__name__)


class FixedChunker(BaseChunker):
    """
    Character-based chunking with overlap.
    """

    def __init__(
        self,
        chunk_size: int | None = None,
        chunk_overlap: int | None = None,
    ) -> None:
        self.chunk_size = chunk_size or settings.CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or settings.CHUNK_OVERLAP

    def chunk(self, text: str) -> list[str]:
        """
        Split text into overlapping chunks.

        Args:
            text: Clean document text.

        Returns:
            List of chunks.
        """
        logger.info("Creating fixed-size chunks.")

        if not text.strip():
            return []

        chunks: list[str] = []

        start = 0
        length = len(text)

        while start < length:
            end = start + self.chunk_size

            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            start += self.chunk_size - self.chunk_overlap

        logger.info(
            "Generated %d chunks.",
            len(chunks),
        )

        return chunks