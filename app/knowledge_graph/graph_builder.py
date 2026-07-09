"""
Knowledge Graph builder.

Creates the enterprise Knowledge Graph from ingested documents.
"""

from __future__ import annotations

from app.core.logging_config import get_logger
from app.extraction.entities.entity_extractor import (
    entity_extractor,
)
from app.extraction.relationships.relationship_extractor import (
    relationship_extractor,
)
from app.knowledge_graph.graph_repository import (
    graph_repository,
)

logger = get_logger(__name__)


class GraphBuilder:
    """
    Builds the Knowledge Graph.
    """

    def build(
        self,
        document_text: str,
    ) -> tuple[list[dict], list[dict]]:
        """
        Build the graph.

        Args:
            document_text: Document text.

        Returns:
            Tuple of entities and relationships.
        """

        logger.info(
            "Starting Knowledge Graph construction."
        )

        # --------------------------------------------
        # Extract entities
        # --------------------------------------------
        entities = entity_extractor.extract(
            document_text,
        )

        logger.info(
            "Extracted %d entities.",
            len(entities),
        )

        for entity in entities:
            graph_repository.add_entity(entity)

        # --------------------------------------------
        # Extract relationships
        # --------------------------------------------
        relationships = relationship_extractor.extract(
            document_text,
            entities,
        )

        logger.info(
            "Extracted %d relationships.",
            len(relationships),
        )

        for relationship in relationships:
            graph_repository.add_relationship(
                relationship,
            )

        logger.info(
            "Knowledge Graph successfully built."
        )

        return entities, relationships


graph_builder = GraphBuilder()