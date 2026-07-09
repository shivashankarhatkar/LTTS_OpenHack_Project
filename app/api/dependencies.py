"""
Common API dependencies.
"""

from app.core.config import settings


def get_settings():
    """
    Return application settings dependency.
    """
    return settings