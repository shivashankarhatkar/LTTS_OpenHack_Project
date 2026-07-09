"""
Answer generator.

Generates the final answer using Gemini based on the
constructed GraphRAG prompt.
"""

from __future__ import annotations

from app.connectors.gemini_connector import gemini_connector
from app.core.logging_config import get_logger

logger = get_logger(__name__)


class AnswerGenerator:
    """
    Generates answers using Gemini.
    """

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate the final answer.

        Args:
            prompt:
                GraphRAG prompt.

        Returns:
            Generated answer.
        """

        logger.info(
            "Generating answer using Gemini."
        )

        answer = gemini_connector.generate(
            prompt=prompt,
        )

        if not answer:
            logger.warning(
                "Gemini returned an empty response."
            )

            return (
                "I couldn't generate an answer from the "
                "available enterprise knowledge."
            )

        logger.info(
            "Answer generated successfully."
        )

        return answer.strip()


answer_generator = AnswerGenerator()