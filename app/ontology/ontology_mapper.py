"""
Ontology mapper.

Maps extracted entities and relationships to the enterprise ontology.
"""

from __future__ import annotations

from app.core.logging_config import get_logger
from app.models.entity import Entity
from app.models.relationship import Relationship
from app.ontology.schema import (
    ENTITY_TYPE_MAP,
    RELATIONSHIP_TYPE_MAP,
)

logger = get_logger(__name__)


class OntologyMapper:
    """
    Maps entities and relationships to the supported ontology.
    """

    def map_entity(
        self,
        entity: Entity,
    ) -> Entity:
        """
        Normalize an entity type.

        Args:
            entity:
                Extracted entity.

        Returns:
            Normalized entity.
        """

        entity_type = entity.entity_type.strip()

        mapped = ENTITY_TYPE_MAP.get(
            entity_type.lower(),
        )

        if mapped is not None:

            entity.entity_type = mapped.name

        else:

            logger.warning(
                "Unknown entity type '%s'. Using 'Document'.",
                entity_type,
            )

            entity.entity_type = "Document"

        return entity

    def map_relationship(
        self,
        relationship: Relationship,
    ) -> Relationship:
        """
        Normalize a relationship type.

        Args:
            relationship:
                Extracted relationship.

        Returns:
            Normalized relationship.
        """

        relationship_type = (
            relationship.relationship_type.strip()
        )

        mapped = RELATIONSHIP_TYPE_MAP.get(
            relationship_type.lower(),
        )

        if mapped is not None:

            relationship.relationship_type = mapped.name

        else:

            logger.warning(
                "Unknown relationship '%s'. Using 'RELATED_TO'.",
                relationship_type,
            )

            relationship.relationship_type = (
                "RELATED_TO"
            )

        return relationship

    def map_entities(
        self,
        entities: list[Entity],
    ) -> list[Entity]:
        """
        Normalize multiple entities.
        """

        return [
            self.map_entity(entity)
            for entity in entities
        ]

    def map_relationships(
        self,
        relationships: list[Relationship],
    ) -> list[Relationship]:
        """
        Normalize multiple relationships.
        """

        return [
            self.map_relationship(
                relationship,
            )
            for relationship in relationships
        ]


ontology_mapper = OntologyMapper()