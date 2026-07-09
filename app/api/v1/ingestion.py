"""
Document ingestion API.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.core.config import settings
from app.core.logging_config import get_logger
from app.ingestion.ingestion_service import ingestion_service
from app.schemas.ingestion import IngestionResponse

logger = get_logger(__name__)

router = APIRouter(
    prefix="/ingestion",
    tags=["Document Ingestion"],
)


@router.post(
    "/upload",
    response_model=IngestionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    file: UploadFile = File(...),
) -> IngestionResponse:
    """
    Upload and ingest a document.
    """

    try:
        upload_dir = Path(settings.UPLOAD_DIRECTORY)
        upload_dir.mkdir(parents=True, exist_ok=True)

        file_path = upload_dir / file.filename

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = ingestion_service.ingest(file_path)

        return IngestionResponse(
            file_name=result.file_name,
            file_type=result.metadata.extension,
            language=result.metadata.language,
            total_chunks=result.total_chunks,
            character_count=result.metadata.character_count,
            word_count=result.metadata.word_count,
            message="Document ingested successfully.",
        )

    except Exception as exc:
        logger.exception("Document ingestion failed.")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc