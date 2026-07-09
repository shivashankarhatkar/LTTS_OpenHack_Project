"""
Plain text document parser.
"""

from __future__ import annotations

from pathlib import Path

from app.core.logging_config import get_logger
from app.ingestion.parsers.base_parser import BaseParser

logger = get_logger(__name__)


class TxtParser(BaseParser):
    """
    Parser for TXT files.
    """

    supported_extensions = (".txt",)

    def parse(self, file_path: Path) -> str:
        """
        Parse a TXT document.

        Args:
            file_path: Path to TXT file.

        Returns:
            Extracted text.
        """
        self.validate(file_path)

        logger.info("Parsing TXT document: %s", file_path.name)

        try:
            text = file_path.read_text(
                encoding="utf-8",
                errors="ignore",
            )

            return text.strip()

        except Exception as exc:
            logger.exception(
                "Failed to parse TXT document."
            )
            raise ValueError(
                f"Unable to parse {file_path.name}"
            ) from exc