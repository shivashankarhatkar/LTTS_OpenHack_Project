"""
Entity Resolver.

Resolves name-based relationships produced by the LLM into
UUID-based relationships suitable for storage in Neo4j.
"""

from __future__ import annotations

from app.core.logging_config import get_logger
from app.models.entity import Entity
from app.models.relationship import (
    RawRelationship,
    Relationship,
)
from app.utils.id_utils import generate_uuid

logger = get_logger(__name__)


class EntityResolver:
    """
    Resolves entity names into Knowledge Graph UUIDs.
    """

    def resolve_relationships(
        self,
        entities: list[Entity],
        raw_relationships: list[RawRelationship],
    ) -> list[Relationship]:
        """
        Resolve raw relationships into graph relationships.

        Args:
            entities:
                Canonical extracted entities.

            raw_relationships:
                Relationships containing entity names.

        Returns:
            UUID-based relationships.
        """

        logger.info(
            "Resolving relationship entity references."
        )

        entity_lookup = {
            entity.name.strip().lower(): entity
            for entity in entities
        }

        resolved: list[Relationship] = []

        for raw in raw_relationships:

            source = entity_lookup.get(
                raw.source_name.strip().lower(),
            )

            target = entity_lookup.get(
                raw.target_name.strip().lower(),
            )

            if source is None:

                logger.warning(
                    "Unable to resolve source entity '%s'.",
                    raw.source_name,
                )

                continue

            if target is None:

                logger.warning(
                    "Unable to resolve target entity '%s'.",
                    raw.target_name,
                )

                continue

            resolved.append(
                Relationship(
                    relationship_id=generate_uuid(),
                    source_entity_id=source.entity_id,
                    target_entity_id=target.entity_id,
                    relationship_type=raw.relationship_type,
                    confidence=raw.confidence,
                    metadata={
                        "description": raw.description,
                    },
                )
            )

        logger.info(
            "Resolved %d relationships.",
            len(resolved),
        )

        return resolved


entity_resolver = EntityResolver()