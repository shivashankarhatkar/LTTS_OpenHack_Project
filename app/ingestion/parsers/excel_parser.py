"""
Excel document parser.

Supports both .xlsx and .xls files using openpyxl.
"""

from __future__ import annotations

from pathlib import Path

from openpyxl import load_workbook

from app.core.logging_config import get_logger
from app.ingestion.parsers.base_parser import BaseParser

logger = get_logger(__name__)


class ExcelParser(BaseParser):
    """
    Parser for Microsoft Excel documents.
    """

    supported_extensions = (
        ".xlsx",
        ".xls",
    )

    def parse(self, file_path: Path) -> str:
        """
        Parse an Excel workbook.

        Args:
            file_path: Path to the workbook.

        Returns:
            Extracted workbook text.

        Raises:
            ValueError:
                If workbook cannot be parsed.
        """
        self.validate(file_path)

        logger.info("Parsing Excel document: %s", file_path.name)

        try:
            workbook = load_workbook(
                filename=file_path,
                data_only=True,
            )

            extracted_text: list[str] = []

            for sheet in workbook.worksheets:
                extracted_text.append(
                    f"Worksheet: {sheet.title}"
                )

                for row in sheet.iter_rows(values_only=True):
                    values = [
                        str(cell).strip()
                        for cell in row
                        if cell is not None
                        and str(cell).strip()
                    ]

                    if values:
                        extracted_text.append(
                            " | ".join(values)
                        )

                extracted_text.append("")

            result = "\n".join(extracted_text).strip()

            logger.info(
                "Successfully extracted %d characters from '%s'.",
                len(result),
                file_path.name,
            )

            return result

        except Exception as exc:
            logger.exception(
                "Failed to parse Excel '%s'.",
                file_path.name,
            )
            raise ValueError(
                f"Unable to parse Excel '{file_path.name}'."
            ) from exc