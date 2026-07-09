"""
Base agent.

Defines the common interface for all LangGraph agents.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from app.core.logging_config import get_logger
from app.orchestration.langgraph.graph_state import (
    GraphState,
)

logger = get_logger(__name__)


class BaseAgent(ABC):
    """
    Abstract base class for every LangGraph agent.
    """

    def __init__(
        self,
        name: str,
    ) -> None:

        self._name = name

    @property
    def name(
        self,
    ) -> str:
        """
        Agent name.
        """

        return self._name

    @abstractmethod
    def execute(
        self,
        state: GraphState,
    ) -> GraphState:
        """
        Execute the agent.

        Args:
            state:
                Current workflow state.

        Returns:
            Updated workflow state.
        """
        raise NotImplementedError

    def log_start(
        self,
    ) -> None:
        """
        Log agent execution start.
        """

        logger.info(
            "[%s] Started.",
            self._name,
        )

    def log_finish(
        self,
    ) -> None:
        """
        Log agent execution completion.
        """

        logger.info(
            "[%s] Completed.",
            self._name,
        )