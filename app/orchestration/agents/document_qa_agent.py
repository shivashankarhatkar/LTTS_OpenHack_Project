"""
Document QA agent.

Handles document-based question answering by delegating the complete
GraphRAG pipeline to GraphRAGService.
"""

from __future__ import annotations

from app.core.logging_config import get_logger
from app.graphrag.graphrag_service import (
    graphrag_service,
)
from app.orchestration.agents.base_agent import (
    BaseAgent,
)
from app.orchestration.langgraph.graph_state import (
    GraphState,
)

logger = get_logger(__name__)


class DocumentQAAgent(BaseAgent):
    """
    Executes document-based question answering.
    """

    def __init__(self) -> None:

        super().__init__(
            name="DocumentQAAgent",
        )

    def execute(
        self,
        state: GraphState,
    ) -> GraphState:
        """
        Execute document QA workflow.

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

        state["answer"]

        state["vector_results"]

        state["graph_results"]

        state["keyword_results"]

        metadata = state.setdefault(
            "metadata",
            {},
        )

        metadata["workflow"] = "document"

        metadata["retrieval"] = "hybrid"

        self.log_finish()

        return state


document_qa_agent = DocumentQAAgent()