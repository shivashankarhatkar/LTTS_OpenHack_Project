"""
File utility functions.
"""

from __future__ import annotations

from pathlib import Path


def ensure_directory(
    directory: str | Path,
) -> Path:
    """
    Create a directory if it does not exist.

    Args:
        directory:
            Directory path.

    Returns:
        Path object.
    """

    path = Path(directory)

    path.mkdir(
        parents=True,
        exist_ok=True,
    )

    return path


def file_exists(
    file_path: str | Path,
) -> bool:
    """
    Check whether a file exists.

    Args:
        file_path:
            File path.

    Returns:
        True if the file exists.
    """

    return Path(file_path).is_file()


def directory_exists(
    directory: str | Path,
) -> bool:
    """
    Check whether a directory exists.

    Args:
        directory:
            Directory path.

    Returns:
        True if the directory exists.
    """

    return Path(directory).is_dir()


def get_file_extension(
    file_path: str | Path,
) -> str:
    """
    Return the lowercase file extension.

    Args:
        file_path:
            File path.

    Returns:
        File extension without '.'.
    """

    return Path(file_path).suffix.lower().lstrip(".")


def get_file_name(
    file_path: str | Path,
) -> str:
    """
    Return the file name.

    Args:
        file_path:
            File path.

    Returns:
        File name.
    """

    return Path(file_path).name


def get_stem(
    file_path: str | Path,
) -> str:
    """
    Return the file name without extension.

    Args:
        file_path:
            File path.

    Returns:
        File stem.
    """

    return Path(file_path).stem


def list_files(
    directory: str | Path,
    recursive: bool = False,
) -> list[Path]:
    """
    List all files in a directory.

    Args:
        directory:
            Directory path.

        recursive:
            Whether to search recursively.

    Returns:
        List of file paths.
    """

    path = Path(directory)

    if not path.exists():

        return []

    if recursive:

        return sorted(
            file
            for file in path.rglob("*")
            if file.is_file()
        )

    return sorted(
        file
        for file in path.iterdir()
        if file.is_file()
    )


def get_file_size(
    file_path: str | Path,
) -> int:
    """
    Return the file size in bytes.

    Args:
        file_path:
            File path.

    Returns:
        File size.
    """

    return Path(file_path).stat().st_size