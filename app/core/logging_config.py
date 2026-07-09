"""
Application logging configuration.

This module configures structured logging for the Enterprise Knowledge
Assistant. All application modules should obtain loggers through
the standard logging.getLogger(__name__) interface.
"""

from __future__ import annotations

import logging
import logging.config
from pathlib import Path

from app.core.config import settings


def setup_logging() -> None:
    """
    Configure application-wide logging.

    Creates the log directory if it does not exist and applies
    a consistent logging configuration.
    """
    log_file = Path(settings.LOG_FILE)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": (
                    "%(asctime)s | %(levelname)-8s | "
                    "%(name)s | %(message)s"
                )
            },
            "detailed": {
                "format": (
                    "%(asctime)s | %(levelname)-8s | %(name)s | "
                    "%(filename)s:%(lineno)d | %(message)s"
                )
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "level": settings.LOG_LEVEL,
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": str(log_file),
                "formatter": "detailed",
                "level": settings.LOG_LEVEL,
                "encoding": "utf-8",
            },
        },
        "root": {
            "handlers": ["console", "file"],
            "level": settings.LOG_LEVEL,
        },
    }

    logging.config.dictConfig(logging_config)


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger.

    Args:
        name: Logger name.

    Returns:
        Configured logger instance.
    """
    return logging.getLogger(name)