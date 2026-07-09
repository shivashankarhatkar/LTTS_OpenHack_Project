"""
Health service.
"""

from app.core.config import settings
from app.schemas.health import HealthResponse


class HealthService:
    """
    Service responsible for health status.
    """

    def get_health(self) -> HealthResponse:
        """
        Return application health.

        Returns:
            HealthResponse object.
        """
        return HealthResponse(
            status="healthy",
            application=settings.APP_NAME,
            version=settings.APP_VERSION,
            environment=settings.ENVIRONMENT,
            message="Enterprise Knowledge Assistant is running successfully.",
        )


health_service = HealthService()