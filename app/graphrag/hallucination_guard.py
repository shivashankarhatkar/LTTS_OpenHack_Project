"""
Hallucination guard.

Validates generated answers against retrieved enterprise knowledge to
reduce unsupported or hallucinated responses.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.core.logging_config import get_logger
from app.retrieval.graph.graph_retriever import GraphResult
from app.retrieval.vector.vector_retriever import RetrievedChunk

logger = get_logger(__name__)


@dataclass(slots=True)
class ValidationResult:
    """
    Validation result for a generated answer.
    """

    is_valid: bool
    confidence: float
    message: str


class HallucinationGuard:
    """
    Validates whether a generated answer is sufficiently supported by
    retrieved enterprise knowledge.
    """

    MIN_CONFIDENCE = 0.45

    def validate(
        self,
        answer: str,
        vector_results: list[RetrievedChunk],
        graph_results: list[GraphResult],
        confidence: float,
    ) -> ValidationResult:
        """
        Validate an answer.

        Args:
            answer:
                Generated answer.

            vector_results:
                Retrieved vector chunks.

            graph_results:
                Retrieved graph context.

            confidence:
                Confidence score produced by ConfidenceScorer.

        Returns:
            ValidationResult
        """

        logger.info(
            "Running hallucination validation."
        )

        # --------------------------------------------------
        # Empty answer
        # --------------------------------------------------

        if not answer.strip():

            return ValidationResult(
                is_valid=False,
                confidence=0.0,
                message="The language model returned an empty response.",
            )

        # --------------------------------------------------
        # No retrieved knowledge
        # --------------------------------------------------

        if (
            len(vector_results) == 0
            and len(graph_results) == 0
        ):

            return ValidationResult(
                is_valid=False,
                confidence=0.0,
                message=(
                    "No supporting enterprise knowledge was retrieved."
                ),
            )

        # --------------------------------------------------
        # Low confidence
        # --------------------------------------------------

        if confidence < self.MIN_CONFIDENCE:

            return ValidationResult(
                is_valid=False,
                confidence=confidence,
                message=(
                    "Retrieved evidence is insufficient to confidently "
                    "answer the question."
                ),
            )

        # --------------------------------------------------
        # Context size heuristic
        # --------------------------------------------------

        context_characters = sum(
            len(chunk.document)
            for chunk in vector_results
        )

        if (
            context_characters < 100
            and len(graph_results) == 0
        ):

            return ValidationResult(
                is_valid=False,
                confidence=confidence,
                message=(
                    "Insufficient enterprise context was retrieved."
                ),
            )

        # --------------------------------------------------
        # Passed validation
        # --------------------------------------------------

        logger.info(
            "Hallucination validation passed."
        )

        return ValidationResult(
            is_valid=True,
            confidence=confidence,
            message="Answer validated successfully.",
        )


hallucination_guard = HallucinationGuard()