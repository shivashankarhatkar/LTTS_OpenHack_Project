"""
Enterprise Entity Extractor.

Uses Gemini to extract Knowledge Graph entities from
enterprise documents.
"""

from __future__ import annotations

import json

from app.core.logging_config import get_logger
from app.llm.gemini_client import gemini_client
from app.models.entity import Entity
from app.utils.id_utils import generate_uuid

logger = get_logger(__name__)


class EntityExtractor:
    """
    Extract canonical Knowledge Graph entities from text.
    """

    def extract(
        self,
        text: str,
    ) -> list[Entity]:
        """
        Extract entities from a document.

        Args:
            text:
                Document text.

        Returns:
            List of Entity objects.
        """

        if not text.strip():

            return []

        prompt = f"""
You are an Enterprise Knowledge Graph extraction engine.

Extract ALL important entities from the document.

Entity Types:

- Person
- Organization
- Department
- Team
- Project
- Product
- Technology
- Tool
- Application
- Database
- Policy
- Process
- Location

Rules:

1. Return ONLY JSON.
2. No markdown.
3. No explanation.
4. Confidence must be between 0 and 1.

Output format:

[
    {{
        "name": "...",
        "entity_type": "...",
        "description": "...",
        "confidence": 0.98
    }}
]

Document:

{text}
"""

        logger.info(
            "Extracting entities using Gemini."
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
                "Unable to parse entity extraction response."
            )

            logger.error(
                "Gemini Response:\n%s",
                response,
            )

            return []

        entities: list[Entity] = []

        for item in data:

            entity = Entity(
                entity_id=generate_uuid(),
                name=item.get(
                    "name",
                    "",
                ).strip(),
                entity_type=item.get(
                    "entity_type",
                    "Unknown",
                ).strip(),
                description=item.get(
                    "description",
                    "",
                ).strip(),
                confidence=float(
                    item.get(
                        "confidence",
                        1.0,
                    )
                ),
                aliases=[],
                metadata={},
            )

            entities.append(
                entity,
            )

        logger.info(
            "Extracted %d entities.",
            len(entities),
        )

        return entities


entity_extractor = EntityExtractor()