"""
Language detection.

Currently supports lightweight English detection.
Designed so additional language detection libraries can
be plugged in later without changing the architecture.
"""

from __future__ import annotations

import re

from app.core.logging_config import get_logger

logger = get_logger(__name__)


class LanguageDetector:
    """
    Detect document language.
    """

    ENGLISH_WORDS = (
        "the",
        "and",
        "is",
        "are",
        "of",
        "to",
        "in",
        "for",
        "with",
        "on",
        "that",
    )

    def detect(self, text: str) -> str:
        """
        Detect language.

        Args:
            text: Document text.

        Returns:
            ISO language code.
        """
        logger.info("Detecting language.")

        if not text.strip():
            return "unknown"

        words = re.findall(r"[a-zA-Z]+", text.lower())

        if not words:
            return "unknown"

        matches = sum(
            1
            for word in words
            if word in self.ENGLISH_WORDS
        )

        score = matches / max(len(words), 1)

        language = "en" if score >= 0.01 else "unknown"

        logger.info(
            "Detected language: %s",
            language,
        )

        return language


language_detector = LanguageDetector()