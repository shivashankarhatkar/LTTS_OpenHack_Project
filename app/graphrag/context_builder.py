"""
Context builder.

Builds the retrieval context from retrieved document chunks.
"""

from __future__ import annotations

from app.retrieval.vector.vector_retriever import RetrievedChunk


class ContextBuilder:
    """
    Builds LLM context from retrieved chunks.
    """

    @staticmethod
    def build(
        chunks: list[RetrievedChunk],
    ) -> str:
        """
        Build formatted context.

        Args:
            chunks: Retrieved chunks.

        Returns:
            Formatted context.
        """
        if not chunks:
            return "No relevant context was found."

        context: list[str] = []

        for index, chunk in enumerate(chunks, start=1):
            context.append(
                f"[Document {index}]\n"
                f"{chunk.document}"
            )

        return "\n\n".join(context)


context_builder = ContextBuilder()