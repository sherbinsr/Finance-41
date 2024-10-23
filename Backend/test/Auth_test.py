import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app,service,schemas
from unittest.mock import MagicMock


client = TestClient(app)

# Mock the database session and service functions
@pytest.fixture
def mock_db_session():
    db = MagicMock(spec=Session)
    return db

# Test to register a user
def test_register_success(mock_db_session):
    service.get_user_by_username = MagicMock(return_value=None)
    mock_user = schemas.ShowUser(id=1, username="testuser", email="test@example.com")
    service.create_user = MagicMock(return_value=mock_user)
    data = {
        "username": "testuser",
        "password": "password123",
        "email": "test@example.com"
    }
    response = client.post("/register", json=data)
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com"
    }

# Test to check if the user Already exists
def test_register_user_already_exists(mock_db_session):
    mock_user = schemas.ShowUser(id=1, username="existinguser", email="existing@example.com")
    service.get_user_by_username = MagicMock(return_value=mock_user)
    data = {
        "username": "existinguser",
        "password": "password123",
        "email": "existing@example.com"
    }
    response = client.post("/register", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already registered"}

# Test ti Invalid creds
def test_login_invalid_username(mock_db_session):
    service.get_user_by_username = MagicMock(return_value=None)
    data = {
        "username": "invaliduser",
        "password": "password123"
    }
    response = client.post("/login", json=data)

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid username or password"}
