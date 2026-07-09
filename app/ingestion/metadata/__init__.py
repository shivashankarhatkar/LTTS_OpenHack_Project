"""
Metadata extraction package.
"""

from app.ingestion.metadata.metadata_extractor import (
    DocumentMetadata,
    MetadataExtractor,
    metadata_extractor,
)

__all__ = [
    "DocumentMetadata",
    "MetadataExtractor",
    "metadata_extractor",
]