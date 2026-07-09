"""
Authentication service.

Provides authentication and user verification for the Enterprise
Knowledge Assistant.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.core.logging_config import get_logger
from app.security.password_hasher import password_hasher
from app.security.jwt_handler import jwt_handler

logger = get_logger(__name__)


@dataclass(slots=True)
class AuthUser:
    """
    Authenticated user.
    """

    username: str

    role: str


class AuthService:
    """
    Authentication service.
    """

    def authenticate(
        self,
        username: str,
        password: str,
        stored_password_hash: str,
        role: str = "user",
    ) -> str:
        """
        Authenticate a user and return a JWT.

        Args:
            username:
                Username.

            password:
                Plain-text password.

            stored_password_hash:
                Password hash from the user store.

            role:
                User role.

        Returns:
            JWT access token.
        """

        logger.info(
            "Authenticating user '%s'.",
            username,
        )

        if not password_hasher.verify_password(
            password=password,
            hashed_password=stored_password_hash,
        ):
            logger.warning(
                "Authentication failed for '%s'.",
                username,
            )
            raise ValueError(
                "Invalid username or password."
            )

        token = jwt_handler.create_access_token(
            {
                "sub": username,
                "role": role,
            }
        )

        logger.info(
            "Authentication successful for '%s'.",
            username,
        )

        return token

    def verify_token(
        self,
        token: str,
    ) -> AuthUser:
        """
        Verify a JWT token.

        Args:
            token:
                JWT token.

        Returns:
            Authenticated user.
        """

        payload = jwt_handler.verify_token(
            token,
        )

        return AuthUser(
            username=payload["sub"],
            role=payload.get(
                "role",
                "user",
            ),
        )


auth_service = AuthService()