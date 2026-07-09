"""
Neo4j connector.

Provides a singleton Neo4j driver for the application.
"""

from __future__ import annotations

from neo4j import Driver
from neo4j import GraphDatabase

from app.core.config import settings
from app.core.logging_config import get_logger

logger = get_logger(__name__)


class Neo4jConnector:
    """
    Singleton connector for Neo4j.
    """

    def __init__(self) -> None:
        self._driver: Driver | None = None

    @property
    def driver(self) -> Driver:
        """
        Return the Neo4j driver.
        """
        if self._driver is None:
            logger.info(
                "Connecting to Neo4j: %s",
                settings.NEO4J_URI,
            )

            self._driver = GraphDatabase.driver(
                settings.NEO4J_URI,
                auth=(
                    settings.NEO4J_USERNAME,
                    settings.NEO4J_PASSWORD,
                ),
            )

            logger.info(
                "Neo4j connection established."
            )

        return self._driver

    def verify_connection(self) -> bool:
        """
        Verify database connectivity.
        """
        try:
            self.driver.verify_connectivity()
            return True

        except Exception:
            logger.exception(
                "Neo4j connection failed."
            )
            return False

    def close(self) -> None:
        """
        Close the Neo4j driver.
        """
        if self._driver is not None:
            self._driver.close()
            logger.info("Neo4j connection closed.")


neo4j_connector = Neo4jConnector()