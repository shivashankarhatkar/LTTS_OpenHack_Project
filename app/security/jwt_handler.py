"""
JWT handler.

Provides JWT access token creation and verification.
"""

from __future__ import annotations

from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Any

import jwt

from app.core.config.settings import settings
from app.core.logging_config import get_logger

logger = get_logger(__name__)


class JWTHandler:
    """
    JWT token handler.
    """

    def create_access_token(
        self,
        payload: dict[str, Any],
        expires_delta: timedelta | None = None,
    ) -> str:
        """
        Create a signed JWT access token.

        Args:
            payload:
                Payload to encode.

            expires_delta:
                Optional expiration duration.

        Returns:
            JWT token.
        """

        expire = datetime.now(
            timezone.utc,
        ) + (
            expires_delta
            or timedelta(
                minutes=settings.jwt_expire_minutes,
            )
        )

        token_payload = payload.copy()

        token_payload.update(
            {
                "exp": expire,
                "iat": datetime.now(
                    timezone.utc,
                ),
            }
        )

        token = jwt.encode(
            token_payload,
            settings.jwt_secret_key,
            algorithm=settings.jwt_algorithm,
        )

        logger.info(
            "JWT access token created."
        )

        return token

    def verify_token(
        self,
        token: str,
    ) -> dict[str, Any]:
        """
        Verify a JWT token.

        Args:
            token:
                JWT token.

        Returns:
            Decoded payload.

        Raises:
            ValueError:
                If the token is invalid or expired.
        """

        try:

            payload = jwt.decode(
                token,
                settings.jwt_secret_key,
                algorithms=[
                    settings.jwt_algorithm,
                ],
            )

            logger.info(
                "JWT verified successfully."
            )

            return payload

        except jwt.ExpiredSignatureError as exc:

            logger.error(
                "JWT token has expired."
            )

            raise ValueError(
                "Token has expired."
            ) from exc

        except jwt.InvalidTokenError as exc:

            logger.error(
                "Invalid JWT token."
            )

            raise ValueError(
                "Invalid token."
            ) from exc


jwt_handler = JWTHandler()