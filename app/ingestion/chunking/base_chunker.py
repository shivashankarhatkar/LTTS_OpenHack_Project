"""
Base chunker interface.

All chunking strategies must inherit from this class.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class BaseChunker(ABC):
    """
    Abstract base class for document chunking.
    """

    @abstractmethod
    def chunk(self, text: str) -> list[str]:
        """
        Split text into chunks.

        Args:
            text: Clean document text.

        Returns:
            List of document chunks.
        """
        raise NotImplementedError