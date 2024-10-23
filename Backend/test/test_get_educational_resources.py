import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app, get_db

client = TestClient(app)

# Mock the get_db dependency
@pytest.fixture
def mock_db():
    db = MagicMock()
    yield db

# Test for GET /educational_resources
def test_get_educational_resources(mock_db, monkeypatch):
    # Mock the resourceservice.get_all_resources to return a fake list
    fake_resources = [
        {"id": 1, "title": "Resource 1", "description": "Description 1"},
        {"id": 2, "title": "Resource 2", "description": "Description 2"},
    ]

    def mock_get_all_resources(db):
        return fake_resources

    # Use monkeypatch to replace the function in the resourceservice
    monkeypatch.setattr("resourceservice.get_all_resources", mock_get_all_resources)

    # Mock the get_db dependency
    monkeypatch.setattr("dependencies.get_db", mock_db)

    # Make the GET request to the endpoint
    response = client.get("/educational_resources")

    # Assert that the status code is 200
    assert response.status_code == 200
    # Assert that the response JSON matches the mocked resources
    assert response.json() == fake_resources
