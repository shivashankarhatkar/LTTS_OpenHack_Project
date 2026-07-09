"""
Chat service.

Acts as the application service for the Enterprise Knowledge Assistant.

The service delegates all orchestration to the LangGraph workflow.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.core.logging_config import get_logger

from app.graphrag.citation_builder import Citation

from app.orchestration.langgraph.workflow import (
    workflow,
)

logger = get_logger(__name__)


@dataclass(slots=True)
class ChatResponse:
    """
    Final response returned to the API layer.
    """

    answer: str

    citations: list[Citation]

    confidence: float

    validation_message: str

    is_valid: bool


class ChatService:
    """
    Enterprise Chat Service.

    This service is intentionally thin.

    It delegates the complete execution to the LangGraph workflow
    and converts the resulting workflow state into a response model.
    """

    def chat(
        self,
        query: str,
        top_k: int = 5,
    ) -> ChatResponse:
        """
        Process a user query.

        Args:
            query:
                User question.

            top_k:
                Number of retrieval results.

        Returns:
            ChatResponse
        """

        logger.info(
            "Received chat request."
        )

        state = workflow.run(
            question=query,
            top_k=top_k,
        )

        logger.info(
            "Workflow completed successfully."
        )

        return ChatResponse(
            answer=state["answer"],
            citations=state["citations"],
            confidence=state["confidence"],
            validation_message=state["validation_message"],
            is_valid=state["is_valid"],
        )


chat_service = ChatService()