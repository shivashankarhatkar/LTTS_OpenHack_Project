"""
OCR image parser.

Extracts text from images using Tesseract OCR.
"""

from __future__ import annotations

from pathlib import Path

import pytesseract
from PIL import Image

from app.core.logging_config import get_logger
from app.ingestion.parsers.base_parser import BaseParser

logger = get_logger(__name__)


class OCRParser(BaseParser):
    """
    OCR parser for image documents.
    """

    supported_extensions = (
        ".png",
        ".jpg",
        ".jpeg",
        ".bmp",
        ".tiff",
    )

    def parse(self, file_path: Path) -> str:
        """
        Extract text from an image.

        Args:
            file_path: Image path.

        Returns:
            Extracted OCR text.
        """
        self.validate(file_path)

        logger.info(
            "Running OCR on image: %s",
            file_path.name,
        )

        try:
            image = Image.open(file_path)

            text = pytesseract.image_to_string(
                image,
                lang="eng",
            ).strip()

            logger.info(
                "Successfully extracted %d characters from '%s'.",
                len(text),
                file_path.name,
            )

            return text

        except Exception as exc:
            logger.exception(
                "OCR failed for '%s'.",
                file_path.name,
            )
            raise ValueError(
                f"Unable to perform OCR on '{file_path.name}'."
            ) from exc