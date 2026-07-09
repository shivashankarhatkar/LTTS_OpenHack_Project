"""
Document metadata extractor.

Extracts useful metadata from uploaded documents before indexing.
"""

from __future__ import annotations
from datetime import datetime
import mimetypes
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel, ConfigDict

from app.core.logging_config import get_logger

logger = get_logger(__name__)


class DocumentMetadata(BaseModel):
    """
    Represents document metadata.
    """

    model_config = ConfigDict(from_attributes=True)

    filename: str
    extension: str
    mime_type: str
    file_size: int
    created_at: datetime
    modified_at: datetime
    language: str
    character_count: int
    word_count: int
    line_count: int


class MetadataExtractor:
    """
    Extract metadata from a document.
    """

    def extract(
        self,
        file_path: Path,
        text: str,
        language: str,
    ) -> DocumentMetadata:
        """
        Extract document metadata.

        Args:
            file_path: Document path.
            text: Extracted text.
            language: Detected language.

        Returns:
            DocumentMetadata instance.
        """
        logger.info(
            "Extracting metadata from '%s'.",
            file_path.name,
        )

        stat = file_path.stat()

        mime_type, _ = mimetypes.guess_type(file_path.name)

        metadata = DocumentMetadata(
            filename=file_path.name,
            extension=file_path.suffix.lower(),
            mime_type=mime_type or "application/octet-stream",
            file_size=stat.st_size,
            created_at=datetime.fromtimestamp(stat.st_ctime),
            modified_at=datetime.fromtimestamp(stat.st_mtime),
            language=language,
            character_count=len(text),
            word_count=len(text.split()),
            line_count=len(text.splitlines()),
        )

        logger.info(
            "Metadata extracted successfully."
        )

        return metadata


metadata_extractor = MetadataExtractor()