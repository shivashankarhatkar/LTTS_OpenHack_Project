"""
ID utility functions.
"""

from __future__ import annotations

import hashlib
from uuid import uuid4


def generate_uuid() -> str:
    """
    Generate a UUID4 string.

    Returns:
        UUID string.
    """

    return str(
        uuid4(),
    )


def generate_document_id(
    file_name: str,
) -> str:
    """
    Generate a deterministic document ID.

    Args:
        file_name:
            Document file name.

    Returns:
        SHA-256 document ID.
    """

    return hashlib.sha256(
        file_name.encode(
            "utf-8",
        )
    ).hexdigest()


def generate_chunk_id(
    document_id: str,
    chunk_index: int,
) -> str:
    """
    Generate a deterministic chunk ID.

    Args:
        document_id:
            Parent document ID.

        chunk_index:
            Chunk number.

    Returns:
        SHA-256 chunk ID.
    """

    value = (
        f"{document_id}:{chunk_index}"
    )

    return hashlib.sha256(
        value.encode(
            "utf-8",
        )
    ).hexdigest()


def generate_entity_id(
    entity_name: str,
    entity_type: str,
) -> str:
    """
    Generate a deterministic entity ID.

    Args:
        entity_name:
            Entity name.

        entity_type:
            Entity type.

    Returns:
        SHA-256 entity ID.
    """

    value = (
        f"{entity_type}:{entity_name.lower().strip()}"
    )

    return hashlib.sha256(
        value.encode(
            "utf-8",
        )
    ).hexdigest()


def generate_relationship_id(
    source_entity_id: str,
    target_entity_id: str,
    relationship_type: str,
) -> str:
    """
    Generate a deterministic relationship ID.

    Args:
        source_entity_id:
            Source entity.

        target_entity_id:
            Target entity.

        relationship_type:
            Relationship type.

    Returns:
        SHA-256 relationship ID.
    """

    value = (
        f"{source_entity_id}:{relationship_type}:{target_entity_id}"
    )

    return hashlib.sha256(
        value.encode(
            "utf-8",
        )
    ).hexdigest()


def generate_conversation_id() -> str:
    """
    Generate a conversation ID.

    Returns:
        UUID string.
    """

    return generate_uuid()


def generate_user_id(
    username: str,
) -> str:
    """
    Generate a deterministic user ID.

    Args:
        username:
            Username.

    Returns:
        SHA-256 user ID.
    """

    return hashlib.sha256(
        username.lower().strip().encode(
            "utf-8",
        )
    ).hexdigest()