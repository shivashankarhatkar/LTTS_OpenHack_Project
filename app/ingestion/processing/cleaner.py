"""
Document text cleaning utilities.

This module normalizes extracted text before chunking and indexing.
"""

from __future__ import annotations

import re

from app.core.logging_config import get_logger

logger = get_logger(__name__)


class TextCleaner:
    """
    Cleans extracted document text.
    """

    MULTIPLE_SPACES = re.compile(r"[ \t]+")
    MULTIPLE_NEWLINES = re.compile(r"\n{3,}")
    NON_PRINTABLE = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]")

    def clean(self, text: str) -> str:
        """
        Clean extracted text.

        Steps:
        - Remove non-printable characters
        - Normalize spaces
        - Normalize newlines
        - Trim whitespace

        Args:
            text: Raw extracted text.

        Returns:
            Cleaned text.
        """
        logger.info("Cleaning extracted text.")

        if not text:
            return ""

        text = self.NON_PRINTABLE.sub("", text)
        text = self.MULTIPLE_SPACES.sub(" ", text)
        text = self.MULTIPLE_NEWLINES.sub("\n\n", text)

        cleaned_lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        cleaned_text = "\n".join(cleaned_lines).strip()

        logger.info(
            "Text cleaned successfully (%d characters).",
            len(cleaned_text),
        )

        return cleaned_text


text_cleaner = TextCleaner()