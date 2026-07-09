"""
Policy extractor.

Extracts enterprise policies, rules, and compliance statements from
documents using the configured LLM.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from app.core.logging_config import get_logger
from app.llm.gemini_client import gemini_client

logger = get_logger(__name__)


@dataclass(slots=True)
class Policy:
    """
    Represents an extracted policy.
    """

    title: str

    description: str

    category: str

    confidence: float = 1.0


class PolicyExtractor:
    """
    Enterprise policy extractor.
    """

    def extract(
        self,
        text: str,
    ) -> list[Policy]:
        """
        Extract enterprise policies from text.

        Args:
            text:
                Document text.

        Returns:
            List of extracted policies.
        """

        if not text.strip():

            return []

        prompt = f"""
Extract all enterprise policies, business rules, compliance statements,
guidelines, and standard operating procedures from the following text.

Return ONLY valid JSON.

Example:

[
    {{
        "title": "...",
        "description": "...",
        "category": "...",
        "confidence": 0.98
    }}
]

Text:

{text}
"""

        logger.info(
            "Extracting enterprise policies."
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
                "Unable to parse policy extraction response."
            )

            return []

        policies: list[Policy] = []

        for item in data:

            policies.append(
                Policy(
                    title=item.get(
                        "title",
                        "",
                    ),
                    description=item.get(
                        "description",
                        "",
                    ),
                    category=item.get(
                        "category",
                        "General",
                    ),
                    confidence=float(
                        item.get(
                            "confidence",
                            1.0,
                        )
                    ),
                )
            )

        logger.info(
            "Extracted %d policies.",
            len(policies),
        )

        return policies


policy_extractor = PolicyExtractor()