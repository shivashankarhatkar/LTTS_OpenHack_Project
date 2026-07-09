"""
Base memory.

Defines the abstract interface for all memory implementations used by
the Enterprise Knowledge Assistant.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class MemoryRecord:
    """
    Represents a single memory entry.
    """

    memory_id: str

    content: str

    metadata: dict[str, Any]

    created_at: datetime


class BaseMemory(ABC):
    """
    Abstract base class for all memory implementations.
    """

    @abstractmethod
    def add(
        self,
        content: str,
        metadata: dict[str, Any] | None = None,
    ) -> MemoryRecord:
        """
        Store a memory record.

        Args:
            content:
                Memory content.

            metadata:
                Optional metadata.

        Returns:
            Created MemoryRecord.
        """
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[MemoryRecord]:
        """
        Search memory.

        Args:
            query:
                Search query.

            top_k:
                Maximum records.

        Returns:
            Matching memory records.
        """
        raise NotImplementedError

    @abstractmethod
    def get(
        self,
        memory_id: str,
    ) -> MemoryRecord | None:
        """
        Retrieve a memory by ID.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        memory_id: str,
    ) -> bool:
        """
        Delete a memory.

        Returns:
            True if deleted.
        """
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        """
        Remove all memories.
        """
        raise NotImplementedError

    @abstractmethod
    def count(self) -> int:
        """
        Return the total number of memory records.
        """
        raise NotImplementedError