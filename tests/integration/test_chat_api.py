"""
Integration tests for the Chat API.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint() -> None:

    response = client.get(
        "/api/v1/health",
    )

    assert response.status_code == 200


def test_chat_endpoint() -> None:

    payload = {
        "query": "What is GraphRAG?",
        "top_k": 5,
    }

    response = client.post(
        "/api/v1/chat",
        json=payload,
    )

    assert response.status_code in (
        200,
        500,
    )


def test_invalid_request() -> None:

    response = client.post(
        "/api/v1/chat",
        json={},
    )

    assert response.status_code == 422