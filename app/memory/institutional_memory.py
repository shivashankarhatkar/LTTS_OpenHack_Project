"""
Institutional memory.

Provides long-term enterprise memory backed by the vector store.
This memory stores and retrieves organizational knowledge that
persists across user sessions.
"""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from app.memory.base_memory import (
    BaseMemory,
    MemoryRecord,
)
from app.vector_store.chromadb.chroma_repository import (
    chroma_repository,
)


class InstitutionalMemory(BaseMemory):
    """
    Long-term enterprise memory.
    """

    COLLECTION_NAME = "institutional_memory"

    def add(
        self,
        content: str,
        metadata: dict | None = None,
    ) -> MemoryRecord:
        """
        Store institutional knowledge.
        """

        record = MemoryRecord(
            memory_id=str(uuid4()),
            content=content,
            metadata=metadata or {},
            created_at=datetime.utcnow(),
        )

        chroma_repository.add_documents(
            collection_name=self.COLLECTION_NAME,
            documents=[record.content],
            metadatas=[
                {
                    **record.metadata,
                    "memory_id": record.memory_id,
                    "created_at": record.created_at.isoformat(),
                }
            ],
            ids=[record.memory_id],
        )

        return record

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[MemoryRecord]:
        """
        Search institutional memory.
        """

        results = chroma_repository.query(
            collection_name=self.COLLECTION_NAME,
            query=query,
            top_k=top_k,
        )

        memories: list[MemoryRecord] = []

        for document, metadata in zip(
            results.documents,
            results.metadatas,
        ):

            memories.append(
                MemoryRecord(
                    memory_id=metadata.get(
                        "memory_id",
                        str(uuid4()),
                    ),
                    content=document,
                    metadata=metadata,
                    created_at=datetime.fromisoformat(
                        metadata.get(
                            "created_at",
                            datetime.utcnow().isoformat(),
                        )
                    ),
                )
            )

        return memories

    def get(
        self,
        memory_id: str,
    ) -> MemoryRecord | None:
        """
        Retrieve a memory by ID.
        """

        results = chroma_repository.get(
            collection_name=self.COLLECTION_NAME,
            ids=[memory_id],
        )

        if not results.documents:
            return None

        metadata = results.metadatas[0]

        return MemoryRecord(
            memory_id=memory_id,
            content=results.documents[0],
            metadata=metadata,
            created_at=datetime.fromisoformat(
                metadata.get(
                    "created_at",
                    datetime.utcnow().isoformat(),
                )
            ),
        )

    def delete(
        self,
        memory_id: str,
    ) -> bool:
        """
        Delete a memory.
        """

        chroma_repository.delete(
            collection_name=self.COLLECTION_NAME,
            ids=[memory_id],
        )

        return True

    def clear(
        self,
    ) -> None:
        """
        Remove all institutional memories.
        """

        chroma_repository.delete_collection(
            self.COLLECTION_NAME,
        )

    def count(
        self,
    ) -> int:
        """
        Return the total number of institutional memories.
        """

        return chroma_repository.count(
            self.COLLECTION_NAME,
        )


institutional_memory = InstitutionalMemory()