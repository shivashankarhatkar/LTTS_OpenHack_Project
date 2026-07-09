"""
Graph QA agent.

Handles graph-oriented questions using the Enterprise GraphRAG
pipeline.

Unlike DocumentQAAgent, this agent stores the retrieval evidence
inside the workflow state so downstream agents can reuse it without
performing retrieval again.
"""

from __future__ import annotations

from app.core.logging_config import get_logger
from app.graphrag.graphrag_service import graphrag_service
from app.orchestration.agents.base_agent import BaseAgent
from app.orchestration.langgraph.graph_state import GraphState

logger = get_logger(__name__)


class GraphQAAgent(BaseAgent):
    """
    Handles Knowledge Graph based question answering.
    """

    def __init__(self) -> None:

        super().__init__(
            name="GraphQAAgent",
        )

    def execute(
        self,
        state: GraphState,
    ) -> GraphState:
        """
        Execute Graph QA.

        Args:
            state:
                Current workflow state.

        Returns:
            Updated workflow state.
        """

        self.log_start()

        response = graphrag_service.query(
            question=state["question"],
            top_k=state.get(
                "top_k",
                5,
            ),
        )

        # --------------------------------------------------
        # Final Answer
        # --------------------------------------------------

        state["answer"]

        state["vector_results"]

        state["graph_results"]

        state["keyword_results"]
        # --------------------------------------------------
        # Metadata
        # --------------------------------------------------

        metadata = state.setdefault(
            "metadata",
            {},
        )

        metadata["workflow"] = "graph"

        metadata["retrieval"] = "hybrid"

        self.log_finish()

        return state


graph_qa_agent = GraphQAAgent()