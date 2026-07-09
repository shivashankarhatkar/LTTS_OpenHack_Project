"""
Base retriever.

Defines the common interface for all retrieval implementations used by
the Enterprise Knowledge Assistant.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class RetrievalResult:
    """
    Represents a single retrieval result.
    """

    document_id: str

    chunk_id: str

    content: str

    score: float

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )


class BaseRetriever(ABC):
    """
    Abstract base class for all retrievers.
    """

    @abstractmethod
    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[RetrievalResult]:
        """
        Retrieve relevant results.

        Args:
            query:
                User query.

            top_k:
                Maximum number of results.

        Returns:
            Ranked retrieval results.
        """
        raise NotImplementedError