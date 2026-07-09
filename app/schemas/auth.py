"""
Authentication API schemas.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class LoginRequest(BaseModel):
    """
    Login request.
    """

    username: str = Field(
        ...,
        min_length=3,
        max_length=100,
    )

    password: str = Field(
        ...,
        min_length=6,
    )


class RegisterRequest(BaseModel):
    """
    User registration request.
    """

    username: str = Field(
        ...,
        min_length=3,
        max_length=100,
    )

    email: EmailStr

    full_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    password: str = Field(
        ...,
        min_length=6,
    )


class TokenResponse(BaseModel):
    """
    JWT token response.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    access_token: str

    token_type: str = "bearer"


class UserResponse(BaseModel):
    """
    Authenticated user information.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    username: str

    email: str

    full_name: str

    role: str

    is_active: bool