"""
Password hasher.

Provides password hashing and verification using bcrypt via Passlib.
"""

from __future__ import annotations

from passlib.context import CryptContext

from app.core.logging_config import get_logger

logger = get_logger(__name__)


class PasswordHasher:
    """
    Password hashing utility.
    """

    def __init__(self) -> None:
        self._pwd_context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto",
        )

    def hash_password(
        self,
        password: str,
    ) -> str:
        """
        Hash a plain-text password.

        Args:
            password:
                Plain-text password.

        Returns:
            BCrypt password hash.
        """

        logger.info(
            "Hashing password."
        )

        return self._pwd_context.hash(
            password,
        )

    def verify_password(
        self,
        password: str,
        hashed_password: str,
    ) -> bool:
        """
        Verify a plain-text password.

        Args:
            password:
                Plain-text password.

            hashed_password:
                Stored password hash.

        Returns:
            True if password is valid.
        """

        logger.info(
            "Verifying password."
        )

        return self._pwd_context.verify(
            password,
            hashed_password,
        )


password_hasher = PasswordHasher()