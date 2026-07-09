"""
Neo4j Repository.

Low-level Neo4j persistence layer.

Responsibilities
----------------
- Execute Cypher queries.
- Persist Entity nodes.
- Persist Relationship edges.
- Retrieve graph nodes.
- Clear the database.

Contains NO business logic.
"""

from __future__ import annotations

from typing import Any

from neo4j import GraphDatabase
from neo4j import Driver

from app.core.config.settings import settings
from app.core.logging_config import get_logger

logger = get_logger(__name__)


class Neo4jRepository:
    """
    Low-level Neo4j repository.
    """

    def __init__(self) -> None:

        self._driver: Driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(
                settings.NEO4J_USERNAME,
                settings.NEO4J_PASSWORD,
            ),
        )

        logger.info(
            "Connected to Neo4j."
        )

    @property
    def driver(
        self,
    ) -> Driver:
        """
        Return Neo4j driver.
        """

        return self._driver

    def execute_query(
        self,
        query: str,
        parameters: dict[str, Any] | None = None,
    ):
        """
        Execute a Cypher query.
        """

        with self.driver.session() as session:

            return session.run(
                query,
                parameters or {},
            )

    def create_node(
        self,
        label: str,
        properties: dict[str, Any],
    ) -> None:
        """
        Create or merge an entity node.
        """

        query = f"""
        MERGE (n:{label} {{entity_id: $entity_id}})
        SET n += $properties
        """

        self.execute_query(
            query=query,
            parameters={
                "entity_id": properties["entity_id"],
                "properties": properties,
            },
        )

        logger.info(
            "Node '%s' persisted.",
            properties["name"],
        )

    def create_relationship(
        self,
        source_id: str,
        target_id: str,
        relationship: str,
        properties: dict[str, Any] | None = None,
    ) -> None:
        """
        Create a relationship between two nodes.
        """

        query = f"""
        MATCH (source {{entity_id: $source_id}})
        MATCH (target {{entity_id: $target_id}})
        MERGE (source)-[r:{relationship}]->(target)
        SET r += $properties
        """

        self.execute_query(
            query=query,
            parameters={
                "source_id": source_id,
                "target_id": target_id,
                "properties": properties or {},
            },
        )

        logger.info(
            "Relationship '%s' persisted.",
            relationship,
        )

    def get_node(
        self,
        entity_id: str,
    ):
        """
        Retrieve an entity node.
        """

        query = """
        MATCH (n {entity_id:$entity_id})
        RETURN n
        """

        result = self.execute_query(
            query=query,
            parameters={
                "entity_id": entity_id,
            },
        )

        record = result.single()

        if record is None:

            return None

        return record["n"]

    def clear_database(
        self,
    ) -> None:
        """
        Remove every node and relationship.
        """

        self.execute_query(
            """
            MATCH (n)
            DETACH DELETE n
            """
        )

        logger.info(
            "Neo4j database cleared."
        )

    def close(
        self,
    ) -> None:
        """
        Close Neo4j driver.
        """

        self.driver.close()

        logger.info(
            "Neo4j connection closed."
        )


neo4j_repository = Neo4jRepository()