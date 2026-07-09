"""
HTML document parser.
"""

from __future__ import annotations

from pathlib import Path

from bs4 import BeautifulSoup

from app.core.logging_config import get_logger
from app.ingestion.parsers.base_parser import BaseParser

logger = get_logger(__name__)


class HtmlParser(BaseParser):
    """
    Parser for HTML documents.
    """

    supported_extensions = (
        ".html",
        ".htm",
    )

    def parse(self, file_path: Path) -> str:
        """
        Parse an HTML document.

        Args:
            file_path: HTML file path.

        Returns:
            Clean extracted text.
        """
        self.validate(file_path)

        logger.info("Parsing HTML document: %s", file_path.name)

        try:
            html = file_path.read_text(
                encoding="utf-8",
                errors="ignore",
            )

            soup = BeautifulSoup(
                html,
                "lxml",
            )

            for tag in soup(
                [
                    "script",
                    "style",
                    "noscript",
                    "header",
                    "footer",
                ]
            ):
                tag.decompose()

            text = soup.get_text(
                separator="\n",
                strip=True,
            )

            logger.info(
                "Successfully extracted %d characters from '%s'.",
                len(text),
                file_path.name,
            )

            return text

        except Exception as exc:
            logger.exception(
                "Failed to parse HTML '%s'.",
                file_path.name,
            )
            raise ValueError(
                f"Unable to parse HTML '{file_path.name}'."
            ) from exc