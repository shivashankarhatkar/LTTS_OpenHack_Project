"""
Validation agent.

Final LangGraph node.

Performs deterministic validation of the generated answer using the
retrieval evidence already stored in the workflow state.

This agent never performs retrieval or invokes the LLM.
"""

from __future__ import annotations

from app.core.logging_config import get_logger
from app.graphrag.hallucination_guard import (
    hallucination_guard,
)
from app.orchestration.agents.base_agent import BaseAgent
from app.orchestration.langgraph.graph_state import GraphState

logger = get_logger(__name__)


class ValidationAgent(BaseAgent):
    """
    Final validation step of the workflow.
    """

    def __init__(self) -> None:

        super().__init__(
            name="ValidationAgent",
        )

    def execute(
        self,
        state: GraphState,
    ) -> GraphState:
        """
        Validate the generated answer.

        Args:
            state:
                Current workflow state.

        Returns:
            Updated workflow state.
        """

        self.log_start()

        validation = hallucination_guard.validate(
            answer=state.get(
                "answer",
                "",
            ),
        vector_results=state.get(
            "vector_results",
            [],
            ),
            graph_results=state.get(
                "graph_results",
                [],
            ),
            confidence=state.get(
                "confidence",
                0.0,
            ),
        )

        state["is_valid"] = validation.is_valid

        state["validation_message"] = validation.message

        if not validation.is_valid:

            logger.warning(
                "Validation failed. Returning guarded response."
            )

        state["answer"] = (
            "I couldn't confidently answer your question "
            "using the available enterprise knowledge.\n\n"
            f"Reason: {validation.message}"
        )

        metadata = state.setdefault(
            "metadata",
            {},
        )

        metadata["validated"] = True

        logger.info(
            "Validation completed. Status: %s",
            validation.is_valid,
        )

        self.log_finish()

        return state


validation_agent = ValidationAgent()