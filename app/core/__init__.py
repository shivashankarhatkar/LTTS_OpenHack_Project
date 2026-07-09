"""
Core package containing configuration, logging,
dependency injection, and exception handling.
"""

from app.core.container import container
from app.core.logging_config import get_logger, setup_logging

__all__ = [
    "container",
    "get_logger",
    "setup_logging",
]