"""
Summarization agent.

Performs lightweight post-processing on the generated answer.

This agent intentionally does NOT invoke the LLM again.
"""

from __future__ import annotations

import re

from app.core.logging_config import get_logger
from app.orchestration.agents.base_agent import BaseAgent
from app.orchestration.langgraph.graph_state import GraphState

logger = get_logger(__name__)


class SummarizationAgent(BaseAgent):
    """
    Cleans and formats the generated answer.
    """

    def __init__(self) -> None:

        super().__init__(
            name="SummarizationAgent",
        )

    def execute(
        self,
        state: GraphState,
    ) -> GraphState:
        """
        Clean the generated response.

        Args:
            state:
                Workflow state.

        Returns:
            Updated workflow state.
        """

        self.log_start()

        answer = state.get(
            "answer",
            "",
        )

        if not answer:

            self.log_finish()

            return state

        # --------------------------------------------
        # Normalize whitespace
        # --------------------------------------------

        answer = re.sub(
            r"\n{3,}",
            "\n\n",
            answer,
        )

        answer = re.sub(
            r"[ \t]+",
            " ",
            answer,
        )

        answer = answer.strip()

        # --------------------------------------------
        # Remove duplicate empty lines
        # --------------------------------------------

        lines = []

        previous_blank = False

        for line in answer.splitlines():

            blank = not line.strip()

            if blank and previous_blank:
                continue

            lines.append(line.rstrip())

            previous_blank = blank

        answer = "\n".join(lines).strip()

        # --------------------------------------------
        # Store formatted answer
        # --------------------------------------------

        state["answer"] = answer

        metadata = state.setdefault(
            "metadata",
            {},
        )

        metadata["formatted"] = True

        logger.info(
            "Answer formatting completed."
        )

        self.log_finish()

        return state


summarization_agent = SummarizationAgent()