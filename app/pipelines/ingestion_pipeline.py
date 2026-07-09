"""
Ingestion pipeline.

Coordinates the complete enterprise document ingestion workflow.
"""

from __future__ import annotations

from app.core.logging_config import get_logger
from app.ingestion.ingestion_service import (
    ingestion_service,
)

logger = get_logger(__name__)


class IngestionPipeline:
    """
    Enterprise ingestion pipeline.
    """

    def run(
        self,
        file_path: str,
    ) -> None:
        """
        Execute the complete ingestion pipeline.

        Steps

        1. Read document
        2. Parse content
        3. Chunk document
        4. Extract entities
        5. Extract relationships
        6. Build knowledge graph
        7. Generate embeddings
        8. Store in ChromaDB
        9. Store in Neo4j

        Args:
            file_path:
                Path to the document.
        """

        logger.info(
            "Starting ingestion pipeline for %s.",
            file_path,
        )

        ingestion_service.ingest(
            file_path=file_path,
        )

        logger.info(
            "Ingestion pipeline completed successfully."
        )


ingestion_pipeline = IngestionPipeline()