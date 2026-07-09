"""
Authentication API endpoints.
"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status

from app.core.logging_config import get_logger
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
)
from app.security.auth_service import (
    auth_service,
)
from app.security.password_hasher import (
    password_hasher,
)

logger = get_logger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# ------------------------------------------------------------------
# Demo In-Memory User Store
#
# Replace with a database repository when integrating persistence.
# ------------------------------------------------------------------

_USERS: dict[str, dict] = {}


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
async def register(
    request: RegisterRequest,
) -> dict:
    """
    Register a new user.
    """

    if request.username in _USERS:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists.",
        )

    _USERS[request.username] = {
        "username": request.username,
        "email": request.email,
        "full_name": request.full_name,
        "password_hash": password_hasher.hash_password(
            request.password,
        ),
        "role": "user",
    }

    logger.info(
        "User '%s' registered.",
        request.username,
    )

    return {
        "message": "User registered successfully.",
    }


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    request: LoginRequest,
) -> TokenResponse:
    """
    Authenticate a user.
    """

    user = _USERS.get(
        request.username,
    )

    if user is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )

    try:

        token = auth_service.authenticate(
            username=request.username,
            password=request.password,
            stored_password_hash=user["password_hash"],
            role=user["role"],
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc

    logger.info(
        "User '%s' logged in.",
        request.username,
    )

    return TokenResponse(
        access_token=token,
    )


@router.get(
    "/verify",
)
async def verify(
    token: str,
) -> dict:
    """
    Verify a JWT token.
    """

    try:

        user = auth_service.verify_token(
            token,
        )

        return {
            "username": user.username,
            "role": user.role,
            "authenticated": True,
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc