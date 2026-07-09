"""
Claim extractor.

Extracts factual claims from enterprise documents using the configured
LLM.
"""

from __future__ import annotations

import json
from dataclasses import dataclass

from app.core.logging_config import get_logger
from app.llm.gemini_client import gemini_client

logger = get_logger(__name__)


@dataclass(slots=True)
class Claim:
    """
    Represents an extracted claim.
    """

    claim: str

    category: str

    confidence: float = 1.0


class ClaimExtractor:
    """
    Enterprise claim extractor.
    """

    def extract(
        self,
        text: str,
    ) -> list[Claim]:
        """
        Extract factual claims from text.

        Args:
            text:
                Input document text.

        Returns:
            List of extracted claims.
        """

        if not text.strip():

            return []

        prompt = f"""
Extract all factual claims from the following enterprise document.

Examples of claims:

- Policies
- Procedures
- Responsibilities
- Rules
- Business facts
- Compliance statements
- Technical facts

Return ONLY valid JSON.

Example:

[
    {{
        "claim": "...",
        "category": "...",
        "confidence": 0.95
    }}
]

Text:

{text}
"""

        logger.info(
            "Extracting claims."
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
                "Unable to parse claim extraction response."
            )

            return []

        claims: list[Claim] = []

        for item in data:

            claims.append(
                Claim(
                    claim=item.get(
                        "claim",
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
            "Extracted %d claims.",
            len(claims),
        )

        return claims


claim_extractor = ClaimExtractor()