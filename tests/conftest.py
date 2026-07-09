"""
Pytest fixtures.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    """
    Create a reusable FastAPI test client.
    """
    return TestClient(app)