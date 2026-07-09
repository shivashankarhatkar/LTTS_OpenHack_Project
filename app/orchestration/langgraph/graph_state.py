"""
Graph state.

Defines the shared state passed between LangGraph nodes.
"""

from __future__ import annotations

from typing import TypedDict

from app.graphrag.citation_builder import Citation


class GraphState(TypedDict):
    """
    Shared LangGraph workflow state.
    """

    question: str

    top_k: int

    answer: str

    citations: list[Citation]

    confidence: float

    validation_message: str

    is_valid: bool

    workflow_type: str

    metadata: dict
    vector_results: list
    graph_results: list
    keyword_results: list