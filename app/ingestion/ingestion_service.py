"""
Document ingestion service.

Coordinates the complete enterprise ingestion pipeline.

Pipeline

Upload
    ↓
Parser
    ↓
Cleaner
    ↓
Language Detection
    ↓
Metadata Extraction
    ↓
Semantic Chunking
    ↓
Embedding Generation
    ↓
BM25 Indexing
    ↓
ChromaDB Indexing
    ↓
Entity Extraction
    ↓
Relationship Extraction
    ↓
Entity Resolution
    ↓
Knowledge Graph Construction
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from app.core.logging_config import get_logger

from app.embeddings.sentence_transformer_embedder import (
    embedder,
)

from app.extraction.entities.entity_extractor import (
    entity_extractor,
)

from app.extraction.relationships.relationship_extractor import (
    relationship_extractor,
)

from app.ingestion.chunking.semantic_chunker import (
    SemanticChunker,
)

from app.ingestion.metadata.metadata_extractor import (
    DocumentMetadata,
    metadata_extractor,
)

from app.ingestion.parsers.parser_factory import (
    ParserFactory,
)

from app.ingestion.processing.cleaner import (
    text_cleaner,
)

from app.ingestion.processing.language_detector import (
    language_detector,
)

from app.knowledge_graph.graph_repository import (
    graph_repository,
)

from app.models.entity import (
    Entity,
)

from app.models.relationship import (
    Relationship,
)

from app.resolution.entity_resolver import (
    entity_resolver,
)

from app.retrieval.keyword.keyword_retriever import (
    keyword_retriever,
)

from app.vector_store.chromadb.chroma_repository import (
    chroma_repository,
)

logger = get_logger(__name__)


@dataclass(slots=True)
class IngestionResult:
    """
    Result returned after document ingestion.
    """

    file_name: str

    metadata: DocumentMetadata

    cleaned_text: str

    chunks: list[str]

    total_chunks: int

    entities: list[Entity]

    relationships: list[Relationship]


class IngestionService:
    """
    Enterprise document ingestion service.
    """

    def __init__(
        self,
    ) -> None:

        self.chunker = SemanticChunker()

    def ingest(
        self,
        file_path: Path,
    ) -> IngestionResult:
        """
        Execute the complete ingestion pipeline.
        """

        logger.info(
            "Starting ingestion for '%s'.",
            file_path.name,
        )

        # --------------------------------------------------
        # Select Parser
        # --------------------------------------------------

        parser = ParserFactory.get_parser(
            file_path,
        )

        # --------------------------------------------------
        # Parse Document
        # --------------------------------------------------

        raw_text = parser.parse(
            file_path,
        )

        logger.info(
            "Document parsed successfully."
        )

        # --------------------------------------------------
        # Clean Extracted Text
        # --------------------------------------------------

        cleaned_text = text_cleaner.clean(
            raw_text,
        )

        logger.info(
            "Document cleaned."
        )

            # --------------------------------------------------
        # Detect Language
        # --------------------------------------------------

        language = language_detector.detect(
            cleaned_text,
        )

        logger.info(
            "Detected language: %s",
            language,
        )

        # --------------------------------------------------
        # Extract Metadata
        # --------------------------------------------------

        metadata = metadata_extractor.extract(
            file_path=file_path,
            text=cleaned_text,
            language=language,
        )

        logger.info(
            "Metadata extracted."
        )

        # --------------------------------------------------
        # Semantic Chunking
        # --------------------------------------------------

        chunks = self.chunker.chunk(
            cleaned_text,
        )

        logger.info(
            "Generated %d chunks.",
            len(chunks),
        )

        # --------------------------------------------------
        # Generate Embeddings
        # --------------------------------------------------

        embeddings = embedder.embed_batch(
            chunks,
        )

        logger.info(
            "Generated %d embeddings.",
            len(embeddings),
        )

        # --------------------------------------------------
        # Build Chunk IDs & Metadata
        # --------------------------------------------------

        chunk_ids: list[str] = []

        chunk_metadata: list[dict] = []

        for index, _ in enumerate(
            chunks,
        ):

            chunk_ids.append(
                str(
                    uuid4(),
                )
            )

            chunk_metadata.append(
                {
                    "file_name": metadata.filename,
                    "extension": metadata.extension,
                    "language": metadata.language,
                    "chunk_index": index,
                    "total_chunks": len(chunks),
                }
            )
            # --------------------------------------------------
        # Build BM25 Index
        # --------------------------------------------------

        logger.info(
            "Building BM25 index."
        )

        keyword_retriever.index(
            ids=chunk_ids,
            documents=chunks,
            metadatas=chunk_metadata,
        )

        logger.info(
            "BM25 index created successfully."
        )

        # --------------------------------------------------
        # Store Embeddings in ChromaDB
        # --------------------------------------------------

        logger.info(
            "Indexing document into ChromaDB."
        )

        chroma_repository.add_documents(
            ids=chunk_ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=chunk_metadata,
        )

        logger.info(
            "Successfully indexed %d chunks into ChromaDB.",
            len(chunks),
        )

        # --------------------------------------------------
        # Extract Entities
        # --------------------------------------------------

        logger.info(
            "Extracting entities."
        )

        entities = entity_extractor.extract(
            cleaned_text,
        )

        logger.info(
            "Extracted %d entities.",
            len(entities),
        )


            # --------------------------------------------------
        # Extract Relationships
        # --------------------------------------------------

        logger.info(
            "Extracting relationships."
        )

        raw_relationships = relationship_extractor.extract(
            cleaned_text,
            entities,
        )

        logger.info(
            "Extracted %d raw relationships.",
            len(raw_relationships),
        )

        # --------------------------------------------------
        # Resolve Entity References
        # --------------------------------------------------

        logger.info(
            "Resolving entity references."
        )

        relationships = entity_resolver.resolve_relationships(
            entities,
            raw_relationships,
        )

        logger.info(
            "Resolved %d relationships.",
            len(relationships),
        )

        # --------------------------------------------------
        # Persist Knowledge Graph
        # --------------------------------------------------

        logger.info(
            "Persisting entities into Neo4j."
        )

        graph_repository.add_entities(
            entities,
        )

        logger.info(
            "Persisting relationships into Neo4j."
        )

        graph_repository.add_relationships(
            relationships,
        )

        logger.info(
            "Knowledge Graph updated successfully."
        )

            # --------------------------------------------------
        # Ingestion Completed
        # --------------------------------------------------

        logger.info(
            "Document '%s' successfully ingested.",
            file_path.name,
        )

        return IngestionResult(
            file_name=file_path.name,
            metadata=metadata,
            cleaned_text=cleaned_text,
            chunks=chunks,
            total_chunks=len(chunks),
            entities=entities,
            relationships=relationships,
        )


ingestion_service = IngestionService()                    

