"""
LangGraph workflow.

This module defines the central orchestration workflow for the
Enterprise Knowledge Assistant.

Workflow

START
    │
    ▼
RouterAgent
    │
    ├───────────────┐
    ▼               ▼
DocumentQA     GraphQA
    │               │
    └──────┬────────┘
           ▼
Summarization
           ▼
Citation
           ▼
Validation
           ▼
END
"""

from __future__ import annotations

from langgraph.graph import END
from langgraph.graph import START
from langgraph.graph import StateGraph

from app.core.logging_config import get_logger

from app.orchestration.agents.router_agent import (
    router_agent,
)

from app.orchestration.agents.document_qa_agent import (
    document_qa_agent,
)

from app.orchestration.agents.graph_qa_agent import (
    graph_qa_agent,
)

from app.orchestration.agents.summarization_agent import (
    summarization_agent,
)

from app.orchestration.agents.citation_agent import (
    citation_agent,
)

from app.orchestration.agents.validation_agent import (
    validation_agent,
)

from app.orchestration.langgraph.graph_state import (
    GraphState,
)

logger = get_logger(__name__)


class Workflow:
    """
    Enterprise LangGraph workflow.
    """

    def __init__(
        self,
    ) -> None:

        self._workflow = self._create_workflow()

    def _create_workflow(
        self,
    ):

        logger.info(
            "Building LangGraph workflow."
        )

        builder = StateGraph(
            GraphState,
        )

        # --------------------------------------------------
        # Register Nodes
        # --------------------------------------------------

        builder.add_node(
            "router",
            router_agent.execute,
        )

        builder.add_node(
            "document_qa",
            document_qa_agent.execute,
        )

        builder.add_node(
            "graph_qa",
            graph_qa_agent.execute,
        )

        builder.add_node(
            "summarization",
            summarization_agent.execute,
        )

        builder.add_node(
            "citation",
            citation_agent.execute,
        )

        builder.add_node(
            "validation",
            validation_agent.execute,
        )

        # --------------------------------------------------
        # Entry Point
        # --------------------------------------------------

        builder.add_edge(
            START,
            "router",
        )

        # --------------------------------------------------
        # Router
        # --------------------------------------------------

        builder.add_conditional_edges(
            "router",
            router_agent.route,
            {
                "document": "document_qa",
                "graph": "graph_qa",
            },
        )

        # --------------------------------------------------
        # Merge Branches
        # --------------------------------------------------

        builder.add_edge(
            "document_qa",
            "summarization",
        )

        builder.add_edge(
            "graph_qa",
            "summarization",
        )

        builder.add_edge(
            "summarization",
            "citation",
        )

        builder.add_edge(
            "citation",
            "validation",
        )

        builder.add_edge(
            "validation",
            END,
        )

        logger.info(
            "Compiling LangGraph workflow."
        )

        return builder.compile()
    
    def invoke(
        self,
        state: GraphState,
        ) -> GraphState:
        """
            Execute an existing workflow state.

            Args:
                state:
                Initialized GraphState.

            Returns:
                Updated GraphState.
            """

        logger.info(
            "Executing LangGraph workflow."
        )

        return self._workflow.invoke(
            state,
        )

    def run(
        self,
        question: str,
        top_k: int = 5,
    ) -> GraphState:
        """
        Execute the complete Enterprise Knowledge Assistant workflow.

        Args:
            question:
                User question.

            top_k:
                Number of retrieval results.

        Returns:
            Final workflow state.
        """

        logger.info(
            "Starting Enterprise Knowledge Assistant workflow."
        )

        initial_state: GraphState = {
            "question": question,
            "top_k": top_k,

            "answer": "",

            "citations": [],

            "confidence": 0.0,

            "validation_message": "",

            "is_valid": False,

            "workflow_type": "",

            "vector_results": [],

            "graph_results": [],

            "keyword_results": [],

            "metadata": {},
        }

        try:

            result = self.invoke(
                initial_state,
            )

            logger.info(
                "Workflow executed successfully."
            )

            return result

        except Exception:

            logger.exception(
                "Workflow execution failed."
            )

            raise


workflow = Workflow()
