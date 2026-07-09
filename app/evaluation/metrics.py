"""
Evaluation metrics.

Provides common evaluation metrics for retrieval and answer quality.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class EvaluationMetrics:
    """
    Evaluation metrics.
    """

    precision: float

    recall: float

    f1_score: float

    confidence: float


class Metrics:
    """
    Metric calculation utilities.
    """

    @staticmethod
    def precision(
        relevant_retrieved: int,
        total_retrieved: int,
    ) -> float:
        """
        Calculate precision.
        """

        if total_retrieved == 0:

            return 0.0

        return relevant_retrieved / total_retrieved

    @staticmethod
    def recall(
        relevant_retrieved: int,
        total_relevant: int,
    ) -> float:
        """
        Calculate recall.
        """

        if total_relevant == 0:

            return 0.0

        return relevant_retrieved / total_relevant

    @staticmethod
    def f1_score(
        precision: float,
        recall: float,
    ) -> float:
        """
        Calculate F1 score.
        """

        if precision + recall == 0:

            return 0.0

        return (
            2
            * precision
            * recall
            / (precision + recall)
        )

    @classmethod
    def evaluate(
        cls,
        relevant_retrieved: int,
        total_retrieved: int,
        total_relevant: int,
        confidence: float,
    ) -> EvaluationMetrics:
        """
        Calculate all evaluation metrics.
        """

        precision = cls.precision(
            relevant_retrieved,
            total_retrieved,
        )

        recall = cls.recall(
            relevant_retrieved,
            total_relevant,
        )

        f1 = cls.f1_score(
            precision,
            recall,
        )

        return EvaluationMetrics(
            precision=precision,
            recall=recall,
            f1_score=f1,
            confidence=confidence,
        )


metrics = Metrics()