"""
Indexing pipeline.

Coordinates indexing of enterprise documents into the vector store and
knowledge graph.
"""

from __future__ import annotations

from app.core.logging_config import get_logger
from app.ingestion.ingestion_service import (
    ingestion_service,
)

logger = get_logger(__name__)


class IndexingPipeline:
    """
    Enterprise indexing pipeline.
    """

    def run(
        self,
        file_path: str,
    ) -> None:
        """
        Execute the indexing pipeline.

        The document is assumed to have already been validated.
        This pipeline delegates indexing to the ingestion service.

        Args:
            file_path:
                Path to the document.
        """

        logger.info(
            "Starting indexing pipeline for %s.",
            file_path,
        )

        ingestion_service.ingest(
            file_path=file_path,
        )

        logger.info(
            "Indexing pipeline completed successfully."
        )


indexing_pipeline = IndexingPipeline()