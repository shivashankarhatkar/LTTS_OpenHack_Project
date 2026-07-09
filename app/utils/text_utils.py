"""
Text utility functions.
"""

from __future__ import annotations

import re
from typing import Iterable


def normalize_text(
    text: str,
) -> str:
    """
    Normalize whitespace in text.

    Args:
        text:
            Input text.

    Returns:
        Normalized text.
    """

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def clean_text(
    text: str,
) -> str:
    """
    Clean extracted document text.

    Args:
        text:
            Raw extracted text.

    Returns:
        Cleaned text.
    """

    text = text.replace(
        "\u00a0",
        " ",
    )

    text = text.replace(
        "\ufeff",
        "",
    )

    return normalize_text(
        text,
    )


def split_into_sentences(
    text: str,
) -> list[str]:
    """
    Split text into sentences.

    Args:
        text:
            Input text.

    Returns:
        List of sentences.
    """

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text.strip(),
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def truncate_text(
    text: str,
    max_length: int,
) -> str:
    """
    Truncate text to the specified length.

    Args:
        text:
            Input text.

        max_length:
            Maximum length.

    Returns:
        Truncated text.
    """

    if len(text) <= max_length:

        return text

    return text[: max_length - 3] + "..."


def remove_duplicate_lines(
    text: str,
) -> str:
    """
    Remove duplicate lines while preserving order.

    Args:
        text:
            Input text.

    Returns:
        Text with duplicate lines removed.
    """

    seen: set[str] = set()

    lines: list[str] = []

    for line in text.splitlines():

        normalized = line.strip()

        if not normalized:

            continue

        if normalized in seen:

            continue

        seen.add(
            normalized,
        )

        lines.append(
            normalized,
        )

    return "\n".join(
        lines,
    )


def join_paragraphs(
    paragraphs: Iterable[str],
) -> str:
    """
    Join multiple paragraphs.

    Args:
        paragraphs:
            Paragraph collection.

    Returns:
        Combined text.
    """

    return "\n\n".join(
        paragraph.strip()
        for paragraph in paragraphs
        if paragraph.strip()
    )