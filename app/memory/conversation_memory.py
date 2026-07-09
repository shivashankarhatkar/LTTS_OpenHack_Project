"""
Conversation memory.

Stores short-term conversation history for the current user session.
"""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from app.memory.base_memory import (
    BaseMemory,
    MemoryRecord,
)


class ConversationMemory(BaseMemory):
    """
    In-memory implementation of short-term conversation memory.
    """

    def __init__(self) -> None:
        self._records: dict[str, MemoryRecord] = {}

    def add(
        self,
        content: str,
        metadata: dict | None = None,
    ) -> MemoryRecord:
        """
        Store a conversation message.
        """

        record = MemoryRecord(
            memory_id=str(uuid4()),
            content=content,
            metadata=metadata or {},
            created_at=datetime.utcnow(),
        )

        self._records[record.memory_id] = record

        return record

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[MemoryRecord]:
        """
        Search conversation history.
        """

        query = query.lower()

        results = [
            record
            for record in self._records.values()
            if query in record.content.lower()
        ]

        results.sort(
            key=lambda record: record.created_at,
            reverse=True,
        )

        return results[:top_k]

    def get(
        self,
        memory_id: str,
    ) -> MemoryRecord | None:
        """
        Retrieve a conversation memory.
        """

        return self._records.get(memory_id)

    def delete(
        self,
        memory_id: str,
    ) -> bool:
        """
        Delete a conversation memory.
        """

        return self._records.pop(memory_id, None) is not None

    def clear(self) -> None:
        """
        Clear the conversation history.
        """

        self._records.clear()

    def count(self) -> int:
        """
        Number of conversation memories.
        """

        return len(self._records)


conversation_memory = ConversationMemory()