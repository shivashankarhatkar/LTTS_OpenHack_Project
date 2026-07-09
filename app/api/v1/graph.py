"""
Knowledge Graph API endpoints.
"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Query
from fastapi import status

from app.core.logging_config import get_logger
from app.knowledge_graph.graph_repository import (
    graph_repository,
)

logger = get_logger(__name__)

router = APIRouter(
    prefix="/graph",
    tags=["Knowledge Graph"],
)


@router.get(
    "/entity/{entity_name}",
    status_code=status.HTTP_200_OK,
)
async def get_entity(
    entity_name: str,
) -> dict:
    """
    Retrieve an entity from the knowledge graph.
    """

    try:

        logger.info(
            "Fetching entity '%s'.",
            entity_name,
        )

        entity = graph_repository.get_entity(
            entity_name,
        )

        if entity is None:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Entity not found.",
            )

        return entity

    except HTTPException:

        raise

    except Exception as exc:

        logger.exception(
            "Failed to fetch entity."
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve entity.",
        ) from exc


@router.get(
    "/relationships/{entity_name}",
    status_code=status.HTTP_200_OK,
)
async def get_relationships(
    entity_name: str,
) -> dict:
    """
    Retrieve relationships for an entity.
    """

    try:

        relationships = (
            graph_repository.get_relationships(
                entity_name,
            )
        )

        return {
            "entity": entity_name,
            "relationships": relationships,
        }

    except Exception as exc:

        logger.exception(
            "Failed to retrieve relationships."
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve relationships.",
        ) from exc


@router.get(
    "/search",
    status_code=status.HTTP_200_OK,
)
async def search_graph(
    query: str = Query(
        ...,
        min_length=1,
    ),
) -> dict:
    """
    Search the knowledge graph.
    """

    try:

        results = graph_repository.search(
            query=query,
        )

        return {
            "query": query,
            "results": results,
        }

    except Exception as exc:

        logger.exception(
            "Graph search failed."
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to search the graph.",
        ) from exc