"""
Semantic document chunker.

Currently performs paragraph-aware chunking while maintaining
the same interface as future semantic implementations.
"""

from __future__ import annotations

from app.core.config import settings
from app.core.logging_config import get_logger
from app.ingestion.chunking.base_chunker import BaseChunker

logger = get_logger(__name__)


class SemanticChunker(BaseChunker):
    """
    Paragraph-aware semantic chunker.
    """

    def __init__(
        self,
        max_chunk_size: int | None = None,
    ) -> None:
        self.max_chunk_size = (
            max_chunk_size or settings.CHUNK_SIZE
        )

    def chunk(self, text: str) -> list[str]:
        """
        Split text using paragraph boundaries.

        Args:
            text: Clean document text.

        Returns:
            List of semantic chunks.
        """
        logger.info("Creating semantic chunks.")

        if not text.strip():
            return []

        paragraphs = [
            paragraph.strip()
            for paragraph in text.split("\n\n")
            if paragraph.strip()
        ]

        chunks: list[str] = []
        current_chunk = ""

        for paragraph in paragraphs:

            if (
                len(current_chunk)
                + len(paragraph)
                + 2
                <= self.max_chunk_size
            ):
                if current_chunk:
                    current_chunk += "\n\n"

                current_chunk += paragraph

            else:
                if current_chunk:
                    chunks.append(current_chunk)

                current_chunk = paragraph

        if current_chunk:
            chunks.append(current_chunk)

        logger.info(
            "Generated %d semantic chunks.",
            len(chunks),
        )

        return chunks