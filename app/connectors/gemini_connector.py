"""
Gemini connector.

Provides a singleton Gemini client for the application.
"""

from __future__ import annotations

from google import genai
from google.genai import Client

from app.core.config import settings
from app.core.logging_config import get_logger

logger = get_logger(__name__)


class GeminiConnector:
    """
    Singleton connector for Google Gemini.
    """

    def __init__(self) -> None:
        self._client: Client | None = None

    @property
    def client(self) -> Client:
        """
        Return the Gemini client.
        """
        if self._client is None:
            logger.info("Initializing Gemini client...")

            self._client = genai.Client(
                api_key=settings.GEMINI_API_KEY,
            )

            logger.info("Gemini client initialized.")

        return self._client

    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate a response using Gemini.

        Args:
            prompt: Input prompt.

        Returns:
            Generated response text.
        """
        logger.info("Generating Gemini response.")

        response = self.client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
        )

        if (
            response is None
            or response.text is None
        ):
            logger.warning("Gemini returned an empty response.")
            return ""

        return response.text.strip()


gemini_connector = GeminiConnector()