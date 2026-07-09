"""
Citation agent.

Builds citations using the retrieval evidence already present in the
workflow state.

This agent never performs retrieval again.
"""

from __future__ import annotations

from app.core.logging_config import get_logger
from app.graphrag.citation_builder import (
    citation_builder,
)
from app.orchestration.agents.base_agent import BaseAgent
from app.orchestration.langgraph.graph_state import GraphState

logger = get_logger(__name__)


class CitationAgent(BaseAgent):
    """
    Builds citations for the final response.
    """

    def __init__(self) -> None:

        super().__init__(
            name="CitationAgent",
        )

    def execute(
        self,
        state: GraphState,
    ) -> GraphState:
        """
        Build citations.

        Args:
            state:
                Current workflow state.

        Returns:
            Updated workflow state.
        """

        self.log_start()

        vector_results = state.get(
            "vector_results",
            [],
        )

        graph_results = state.get(
            "graph_results",
            [],
        )

        citations = citation_builder.build(
            vector_results=vector_results,
            graph_results=graph_results,
        )

        state["citations"] = citations

        metadata = state.setdefault(
            "metadata",
            {},
        )

        metadata["citations_generated"] = True

        logger.info(
            "Generated %d citations.",
            len(citations),
        )

        self.log_finish()

        return state


citation_agent = CitationAgent()