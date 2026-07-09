"""
ChromaDB connector.

Provides a singleton connection to the ChromaDB server.
"""

from __future__ import annotations

import chromadb
from chromadb import ClientAPI
from chromadb.config import Settings

from app.core.config import settings
from app.core.logging_config import get_logger

logger = get_logger(__name__)


class ChromaConnector:
    """
    Singleton connector for ChromaDB.
    """

    def __init__(self) -> None:
        self._client: ClientAPI | None = None

    @property
    def client(self) -> ClientAPI:
        """
        Return a connected ChromaDB client.
        """
        if self._client is None:
            logger.info(
                "Connecting to local ChromaDB at %s",
                settings.chroma_path,
            )

            self._client = chromadb.PersistentClient(
                path=settings.CHROMA_DB_PATH,
                settings=Settings(
                anonymized_telemetry=False,
                ),
            )

            logger.info("Connected to ChromaDB.")

        return self._client

    def get_collection(self):
        """
        Get or create the configured collection.

        Returns:
            Chroma collection instance.
        """
        return self.client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION,
            metadata={
                "description": (
                    "Enterprise Knowledge Assistant "
                    "document collection"
                )
            },
        )

    def heartbeat(self) -> bool:
        """
        Check whether ChromaDB is reachable.

        Returns:
            True if the server responds.
        """
        try:
            self.client.heartbeat()
            return True
        except Exception:
            logger.exception(
                "Unable to connect to ChromaDB."
            )
            return False


chroma_connector = ChromaConnector()