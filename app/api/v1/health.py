"""
Health API endpoints.
"""

from fastapi import APIRouter, status

from app.schemas.health import HealthResponse
from app.services.health_service import health_service

router = APIRouter(prefix="/health")


@router.get(
    "",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Application Health Check",
)
async def health_check() -> HealthResponse:
    """
    Returns the current application health.
    """
    return health_service.get_health()