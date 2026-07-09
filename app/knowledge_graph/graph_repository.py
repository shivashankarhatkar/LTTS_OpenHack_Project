"""
Knowledge Graph Repository.

Responsible for persisting canonical Knowledge Graph
entities and relationships into Neo4j.

This layer contains NO business logic.
"""

from __future__ import annotations

from app.core.logging_config import get_logger
from app.knowledge_graph.neo4j.neo4j_repository import (
    neo4j_repository,
)
from app.models.entity import Entity
from app.models.relationship import Relationship

logger = get_logger(__name__)


class GraphRepository:
    """
    Repository responsible for persisting the
    Enterprise Knowledge Graph.
    """

    def add_entity(
        self,
        entity: Entity,
    ) -> None:
        """
        Persist an entity node.

        Args:
            entity:
                Canonical entity.
        """

        logger.info(
            "Persisting entity '%s'.",
            entity.name,
        )

        neo4j_repository.create_node(
            label=entity.entity_type,
            properties=entity.to_dict(),
        )

    def add_entities(
        self,
        entities: list[Entity],
    ) -> None:
        """
        Persist multiple entities.

        Args:
            entities:
                List of entities.
        """

        for entity in entities:

            self.add_entity(
                entity,
            )

    def add_relationship(
        self,
        relationship: Relationship,
    ) -> None:
        """
        Persist a relationship.

        Args:
            relationship:
                Canonical relationship.
        """

        logger.info(
            "Persisting relationship '%s'.",
            relationship.relationship_type,
        )

        neo4j_repository.create_relationship(
            source_id=relationship.source_entity_id,
            target_id=relationship.target_entity_id,
            relationship=relationship.relationship_type,
            properties=relationship.to_dict(),
        )

    def add_relationships(
        self,
        relationships: list[Relationship],
    ) -> None:
        """
        Persist multiple relationships.

        Args:
            relationships:
                List of graph relationships.
        """

        for relationship in relationships:

            self.add_relationship(
                relationship,
            )

    def get_node(
        self,
        entity_id: str,
    ):
        """
        Retrieve a node by entity ID.
        """

        return neo4j_repository.get_node(
            entity_id,
        )

    def clear(
        self,
    ) -> None:
        """
        Remove all graph data.
        """

        neo4j_repository.clear_database()


graph_repository = GraphRepository()