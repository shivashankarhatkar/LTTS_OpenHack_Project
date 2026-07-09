"""
Parser factory.

Creates the appropriate parser based on the uploaded document type.
"""

from __future__ import annotations

from pathlib import Path

from app.ingestion.parsers.base_parser import BaseParser
from app.ingestion.parsers.docx_parser import DocxParser
from app.ingestion.parsers.excel_parser import ExcelParser
from app.ingestion.parsers.html_parser import HtmlParser
from app.ingestion.parsers.ocr_parser import OCRParser
from app.ingestion.parsers.pdf_parser import PdfParser
from app.ingestion.parsers.pptx_parser import PptxParser
from app.ingestion.parsers.txt_parser import TxtParser


class ParserFactory:
    """
    Factory responsible for returning the correct parser.
    """

    _PARSERS: dict[str, type[BaseParser]] = {
        ".txt": TxtParser,
        ".pdf": PdfParser,
        ".docx": DocxParser,
        ".pptx": PptxParser,
        ".ppt": PptxParser,
        ".xlsx": ExcelParser,
        ".xls": ExcelParser,
        ".html": HtmlParser,
        ".htm": HtmlParser,
        ".png": OCRParser,
        ".jpg": OCRParser,
        ".jpeg": OCRParser,
        ".tiff": OCRParser,
        ".bmp": OCRParser,
    }

    @classmethod
    def get_parser(cls, file_path: Path) -> BaseParser:
        """
        Return the appropriate parser for the given file.

        Args:
            file_path: Document path.

        Returns:
            Parser instance.

        Raises:
            ValueError:
                If the file extension is unsupported.
        """
        extension = file_path.suffix.lower()

        parser_class = cls._PARSERS.get(extension)

        if parser_class is None:
            supported = ", ".join(sorted(cls._PARSERS.keys()))
            raise ValueError(
                f"Unsupported file type '{extension}'. "
                f"Supported types: {supported}"
            )

        return parser_class()