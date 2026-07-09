"""
PDF document parser.

Uses PyMuPDF (fitz) for high-performance text extraction from PDF files.
"""

from __future__ import annotations

from pathlib import Path

import fitz

from app.core.logging_config import get_logger
from app.ingestion.parsers.base_parser import BaseParser

logger = get_logger(__name__)


class PdfParser(BaseParser):
    """
    Parser for PDF documents.
    """

    supported_extensions = (".pdf",)

    def parse(self, file_path: Path) -> str:
        """
        Parse a PDF document.

        Args:
            file_path: Path to the PDF document.

        Returns:
            Extracted text from all pages.

        Raises:
            ValueError:
                If the PDF cannot be parsed.
        """
        self.validate(file_path)

        logger.info("Parsing PDF document: %s", file_path.name)

        try:
            extracted_pages: list[str] = []

            with fitz.open(file_path) as document:
                logger.info(
                    "PDF contains %d pages.",
                    document.page_count,
                )

                for page in document:
                    page_text = page.get_text("text").strip()

                    if page_text:
                        extracted_pages.append(page_text)

            extracted_text = "\n\n".join(extracted_pages).strip()

            logger.info(
                "Successfully extracted %d characters from '%s'.",
                len(extracted_text),
                file_path.name,
            )

            return extracted_text

        except Exception as exc:
            logger.exception(
                "Failed to parse PDF '%s'.",
                file_path.name,
            )
            raise ValueError(
                f"Unable to parse PDF '{file_path.name}'."
            ) from exc