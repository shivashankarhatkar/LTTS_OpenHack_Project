"""
Base parser interface.

All document parsers must inherit from this class.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class BaseParser(ABC):
    """
    Abstract base class for all document parsers.
    """

    supported_extensions: tuple[str, ...] = ()

    @abstractmethod
    def parse(self, file_path: Path) -> str:
        """
        Parse a document and return extracted text.

        Args:
            file_path: Path to the document.

        Returns:
            Extracted document text.

        Raises:
            FileNotFoundError:
                If file does not exist.

            ValueError:
                If document cannot be parsed.
        """
        raise NotImplementedError

    def validate(self, file_path: Path) -> None:
        """
        Validate the input file.

        Args:
            file_path: Document path.
        """
        if not file_path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        if not file_path.is_file():
            raise ValueError(
                f"{file_path} is not a valid file."
            )

        if (
            self.supported_extensions
            and file_path.suffix.lower()
            not in self.supported_extensions
        ):
            raise ValueError(
                f"Unsupported file type: {file_path.suffix}"
            )