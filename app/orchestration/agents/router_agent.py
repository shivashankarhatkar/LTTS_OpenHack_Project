"""
Router agent.

Determines which workflow path should process the user's request.
"""

from __future__ import annotations

from app.core.logging_config import get_logger
from app.orchestration.agents.base_agent import BaseAgent
from app.orchestration.langgraph.graph_state import GraphState

logger = get_logger(__name__)


class RouterAgent(BaseAgent):
    """
    Routes user requests to the appropriate workflow.

    Current routes:

    - graph
    - document

    This implementation is intentionally simple and deterministic.
    New routes can be added later without changing the workflow.
    """

    GRAPH_KEYWORDS = {
        "relationship",
        "related",
        "connected",
        "connection",
        "owner",
        "owns",
        "belongs",
        "dependency",
        "dependencies",
        "manager",
        "reports",
        "reporting",
        "hierarchy",
        "organization",
        "network",
        "graph",
        "link",
        "links",
    }

    def __init__(self) -> None:

        super().__init__(
            name="RouterAgent",
        )

    def execute(
        self,
        state: GraphState,
    ) -> GraphState:
        """
        Determine the workflow type.
        """

        self.log_start()

        workflow_type = self.route(
            state,
        )

        state["workflow_type"] = workflow_type

        logger.info(
            "Workflow selected: %s",
            workflow_type,
        )

        self.log_finish()

        return state

    def route(
        self,
        state: GraphState,
    ) -> str:
        """
        Decide which workflow should answer the question.

        Returns

        graph
        document
        """

        question = (
            state.get(
                "question",
                "",
            )
            .lower()
            .strip()
        )

        for keyword in self.GRAPH_KEYWORDS:

            if keyword in question:

                return "graph"

        return "document"


router_agent = RouterAgent()