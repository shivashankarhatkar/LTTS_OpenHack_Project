"""
Gemini client.

Concrete implementation of the BaseLLM interface using the Google
Generative AI SDK.
"""

from __future__ import annotations

from google import genai
from google.genai.types import GenerateContentConfig

from app.core.config.settings import settings
from app.core.logging_config import get_logger
from app.llm.base_llm import BaseLLM

logger = get_logger(__name__)


class GeminiClient(BaseLLM):
    """
    Gemini LLM client.
    """

    def __init__(self) -> None:

        self._client = genai.Client(
            api_key=settings.gemini_api_key,
        )

        self._model = settings.gemini_model

        logger.info(
            "Gemini client initialized."
        )

    def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.2,
    ) -> str:
        """
        Generate text using Gemini.

        Args:
            prompt:
                Input prompt.

            temperature:
                Sampling temperature.

        Returns:
            Generated response.
        """

        logger.info(
            "Sending request to Gemini."
        )

        response = self._client.models.generate_content(
            model=self._model,
            contents=prompt,
            config=GenerateContentConfig(
                temperature=temperature,
            ),
        )

        if (
            response is None
            or response.text is None
        ):

            logger.error(
                "Gemini returned an empty response."
            )

            raise RuntimeError(
                "Gemini returned an empty response."
            )

        logger.info(
            "Gemini response received successfully."
        )

        logger.info(
            "Gemini response received successfully."
        )

        text = response.text.strip()

        # Remove Markdown code fences if present.
        if text.startswith("```json"):
            text = text[7:]

        elif text.startswith("```"):
            text = text[3:]

        if text.endswith("```"):
            text = text[:-3]

        text = text.strip()
        logger.info(
            "Gemini raw response:\n%s",
            text,
        )

        return text


gemini_client = GeminiClient()