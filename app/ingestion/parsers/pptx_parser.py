"""
PowerPoint document parser.

Uses python-pptx to extract text from Microsoft PowerPoint
presentations.
"""

from __future__ import annotations

from pathlib import Path

from pptx import Presentation

from app.core.logging_config import get_logger
from app.ingestion.parsers.base_parser import BaseParser

logger = get_logger(__name__)


class PptxParser(BaseParser):
    """
    Parser for Microsoft PowerPoint presentations.
    """

    supported_extensions = (
        ".pptx",
        ".ppt",
    )

    def parse(self, file_path: Path) -> str:
        """
        Parse a PowerPoint presentation.

        Args:
            file_path: Path to the presentation.

        Returns:
            Extracted presentation text.

        Raises:
            ValueError:
                If the presentation cannot be parsed.
        """
        self.validate(file_path)

        logger.info(
            "Parsing PowerPoint presentation: %s",
            file_path.name,
        )

        try:
            presentation = Presentation(file_path)

            slide_contents: list[str] = []

            for slide_number, slide in enumerate(
                presentation.slides,
                start=1,
            ):
                slide_text: list[str] = []

                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        text = shape.text.strip()

                        if text:
                            slide_text.append(text)

                if slide_text:
                    slide_contents.append(
                        f"Slide {slide_number}\n"
                        + "\n".join(slide_text)
                    )

            extracted_text = "\n\n".join(
                slide_contents
            ).strip()

            logger.info(
                "Successfully extracted %d characters from '%s'.",
                len(extracted_text),
                file_path.name,
            )

            return extracted_text

        except Exception as exc:
            logger.exception(
                "Failed to parse PowerPoint '%s'.",
                file_path.name,
            )
            raise ValueError(
                f"Unable to parse PowerPoint '{file_path.name}'."
            ) from exc