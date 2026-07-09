"""
Graph retriever.

Retrieves relevant entities and relationships from the Knowledge Graph
using Neo4j.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.core.logging_config import get_logger
from app.knowledge_graph.neo4j.neo4j_repository import (
    neo4j_repository,
)

logger = get_logger(__name__)


@dataclass(slots=True)
class GraphResult:
    """
    Represents a graph retrieval result.
    """

    entity_id: str
    entity_name: str
    entity_type: str
    relationship: str
    related_entity: str


class GraphRetriever:
    """
    Retrieve information from the Knowledge Graph.
    """

    def retrieve(
        self,
        query: str,
        limit: int = 10,
    ) -> list[GraphResult]:
        """
        Retrieve graph information relevant to a query.

        Args:
            query: User query.
            limit: Maximum number of graph results.

        Returns:
            List of GraphResult objects.
        """

        logger.info(
            "Searching Knowledge Graph for '%s'.",
            query,
        )

        cypher = """
        MATCH (a)-[r]->(b)

        WHERE
            toLower(a.name) CONTAINS toLower($query)
            OR
            toLower(b.name) CONTAINS toLower($query)

        RETURN
            a.id AS entity_id,
            a.name AS entity_name,
            labels(a)[0] AS entity_type,
            type(r) AS relationship,
            b.name AS related_entity

        LIMIT $limit
        """

        records = neo4j_repository.execute_query(
            query=cypher,
            parameters={
                "query": query,
                "limit": limit,
            },
        )

        results: list[GraphResult] = []

        for record in records:
            results.append(
                GraphResult(
                    entity_id=record["entity_id"],
                    entity_name=record["entity_name"],
                    entity_type=record["entity_type"],
                    relationship=record["relationship"],
                    related_entity=record["related_entity"],
                )
            )

        logger.info(
            "Retrieved %d graph results.",
            len(results),
        )

        return results


graph_retriever = GraphRetriever()