"""
Health endpoint tests.
"""

from fastapi.testclient import TestClient


def test_health_endpoint(client: TestClient) -> None:
    """
    Test the health endpoint.
    """
    response = client.get("/api/v1/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["application"] == "Enterprise Knowledge Assistant"
    assert data["version"] == "1.0.0"