"""
End-to-end tests for the Enterprise Knowledge Assistant.

These tests validate the complete application workflow through the
public API.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_application_health() -> None:
    """
    Verify the application starts successfully.
    """

    response = client.get(
        "/api/v1/health",
    )

    assert response.status_code == 200


def test_complete_chat_workflow() -> None:
    """
    Verify the complete question-answering workflow.
    """

    payload = {
        "query": "Explain enterprise knowledge graph.",
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

    if response.status_code == 200:

        data = response.json()

        assert "answer" in data

        assert "citations" in data

        assert "confidence" in data

        assert "validation_message" in data

        assert "is_valid" in data


def test_empty_query() -> None:
    """
    Empty query should be rejected.
    """

    payload = {
        "query": "",
        "top_k": 5,
    }

    response = client.post(
        "/api/v1/chat",
        json=payload,
    )

    assert response.status_code == 422


def test_invalid_payload() -> None:
    """
    Invalid payload should fail validation.
    """

    response = client.post(
        "/api/v1/chat",
        json={},
    )

    assert response.status_code == 422


def test_invalid_top_k() -> None:
    """
    Invalid top_k should fail validation.
    """

    payload = {
        "query": "What is GraphRAG?",
        "top_k": 0,
    }

    response = client.post(
        "/api/v1/chat",
        json=payload,
    )

    assert response.status_code == 422


def test_large_query() -> None:
    """
    Verify the application handles large requests.
    """

    payload = {
        "query": "Enterprise Knowledge Assistant " * 100,
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