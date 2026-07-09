"""
Evaluator.

Evaluates retrieval and answer quality for the Enterprise Knowledge
Assistant.
"""

from __future__ import annotations

from app.core.logging_config import get_logger
from app.evaluation.metrics import (
    EvaluationMetrics,
    metrics,
)

logger = get_logger(__name__)


class Evaluator:
    """
    Enterprise evaluation service.
    """

    def evaluate(
        self,
        retrieved_results: int,
        relevant_results: int,
        relevant_retrieved: int,
        confidence: float,
    ) -> EvaluationMetrics:
        """
        Evaluate retrieval quality.

        Args:
            retrieved_results:
                Number of retrieved documents.

            relevant_results:
                Total relevant documents.

            relevant_retrieved:
                Relevant retrieved documents.

            confidence:
                Confidence score.

        Returns:
            EvaluationMetrics.
        """

        evaluation = metrics.evaluate(
            relevant_retrieved=relevant_retrieved,
            total_retrieved=retrieved_results,
            total_relevant=relevant_results,
            confidence=confidence,
        )

        logger.info(
            (
                "Evaluation completed "
                "(Precision=%.3f, Recall=%.3f, F1=%.3f)"
            ),
            evaluation.precision,
            evaluation.recall,
            evaluation.f1_score,
        )

        return evaluation

    def evaluate_answer(
        self,
        answer: str,
        citations: list,
        confidence: float,
    ) -> EvaluationMetrics:
        """
        Perform a lightweight evaluation of the generated answer.

        Args:
            answer:
                Generated answer.

            citations:
                Supporting citations.

            confidence:
                Confidence score.

        Returns:
            EvaluationMetrics.
        """

        retrieved = max(
            len(citations),
            1,
        )

        relevant = retrieved

        relevant_retrieved = (
            retrieved
            if answer.strip()
            else 0
        )

        return self.evaluate(
            retrieved_results=retrieved,
            relevant_results=relevant,
            relevant_retrieved=relevant_retrieved,
            confidence=confidence,
        )


evaluator = Evaluator()