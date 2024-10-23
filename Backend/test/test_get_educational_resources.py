import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app, get_db
from app.services import  resourceservice
client = TestClient(app)

# Mock the get_db dependency
@pytest.fixture
def mock_db():
    db = MagicMock()
    yield db

# Test for GET /educational_resources
def test_get_educational_resources(mock_db, monkeypatch):
    fake_resources = [
        {"id": 1, "title": "Resource 1", "description": "Description 1"},
        {"id": 2, "title": "Resource 2", "description": "Description 2"},
    ]

    def mock_get_all_resources(mock_db):
        return fake_resources
    monkeypatch.setattr("resourceservice.get_all_resources", mock_get_all_resources)
    monkeypatch.setattr("dependencies.get_db", mock_db)
    response = client.get("/educational_resources")
    assert response.status_code == 200
    assert response.json() == fake_resources
