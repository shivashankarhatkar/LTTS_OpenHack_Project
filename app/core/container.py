"""
Simple dependency injection container.
"""

from __future__ import annotations

from typing import Any


class Container:
    """
    Lightweight dependency injection container.
    """

    def __init__(self) -> None:
        self._services: dict[str, Any] = {}

    def register(self, name: str, service: Any) -> None:
        """
        Register a service.

        Args:
            name: Service name.
            service: Service instance.
        """
        self._services[name] = service

    def resolve(self, name: str) -> Any:
        """
        Resolve a registered service.

        Args:
            name: Service name.

        Returns:
            Registered service.

        Raises:
            KeyError: If service is not registered.
        """
        if name not in self._services:
            raise KeyError(f"Service '{name}' is not registered.")

        return self._services[name]

    def exists(self, name: str) -> bool:
        """
        Check whether a service is registered.
        """
        return name in self._services

    def clear(self) -> None:
        """
        Remove all registered services.
        """
        self._services.clear()


container = Container()