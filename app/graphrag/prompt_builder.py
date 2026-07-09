"""
Prompt builder.

Responsible for constructing prompts sent to Gemini.
"""

from __future__ import annotations


class PromptBuilder:
    """
    Builds prompts for the Enterprise Knowledge Assistant.
    """

    @staticmethod
    def build(
        query: str,
        context: str,
    ) -> str:
        """
        Build the final LLM prompt.

        Args:
            query: User question.
            context: Retrieved context.

        Returns:
            Prompt string.
        """
        return f"""
You are an Enterprise Knowledge Assistant.

Use ONLY the supplied context to answer.

If the answer cannot be found in the context, reply:

"I don't have enough information in the enterprise knowledge base to answer this question."

----------------------------
Enterprise Context
----------------------------

{context}

----------------------------
User Question
----------------------------

{query}

----------------------------
Answer
----------------------------
""".strip()


prompt_builder = PromptBuilder()