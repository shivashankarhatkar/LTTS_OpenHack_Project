"""
Enterprise Relationship Extractor.

Extracts semantic relationships between previously
identified entities using Gemini.

This extractor DOES NOT resolve UUIDs.
It only returns name-based relationships.
"""

from __future__ import annotations

import json

from app.core.logging_config import get_logger
from app.llm.gemini_client import gemini_client
from app.models.entity import Entity
from app.models.relationship import RawRelationship

logger = get_logger(__name__)


class RelationshipExtractor:
    """
    Extract semantic relationships between entities.
    """

    def extract(
        self,
        text: str,
        entities: list[Entity],
    ) -> list[RawRelationship]:
        """
        Extract relationships between entities.

        Args:
            text:
                Original document text.

            entities:
                Previously extracted entities.

        Returns:
            List of RawRelationship objects.
        """

        if not text.strip():
            return []

        if not entities:

            logger.info(
                "No entities found. Skipping relationship extraction."
            )

            return []

        entity_list = "\n".join(
            f"- {entity.name} ({entity.entity_type})"
            for entity in entities
        )

        prompt = f"""
You are an Enterprise Knowledge Graph relationship extraction engine.

Below are the entities extracted from the document.

Entities

{entity_list}

Document

{text}

Extract ONLY meaningful relationships between the listed entities.

Rules:

1. Use ONLY entities present in the entity list.
2. Do NOT invent entities.
3. Return ONLY JSON.
4. No markdown.
5. No explanations.

Relationship Types (examples):

USES
MANAGES
BELONGS_TO
WORKS_IN
PART_OF
REPORTS_TO
DEPENDS_ON
CONNECTED_TO
OWNS
CREATED_BY
LOCATED_IN

Output Format:

[
    {{
        "source_name": "...",
        "target_name": "...",
        "relationship_type": "...",
        "confidence": 0.98,
        "description": "Optional description"
    }}
]
"""

        logger.info(
            "Extracting relationships using Gemini."
        )

        response = gemini_client.generate(
            prompt,
        )

        try:

            data = json.loads(
                response,
            )

        except Exception:

            logger.exception(
                "Unable to parse relationship extraction response."
            )

            logger.error(
                "Gemini Response:\n%s",
                response,
            )

            return []

        relationships: list[RawRelationship] = []

        for item in data:

            relationships.append(
                RawRelationship(
                    source_name=item.get(
                        "source_name",
                        "",
                    ).strip(),
                    target_name=item.get(
                        "target_name",
                        "",
                    ).strip(),
                    relationship_type=item.get(
                        "relationship_type",
                        "RELATED_TO",
                    ).strip(),
                    confidence=float(
                        item.get(
                            "confidence",
                            1.0,
                        )
                    ),
                    description=item.get(
                        "description",
                        "",
                    ).strip(),
                )
            )

        logger.info(
            "Extracted %d relationships.",
            len(relationships),
        )

        return relationships


relationship_extractor = RelationshipExtractor()