import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
client = TestClient(app)

class Query:
    def __init__(self, message):
        self.message = message

@pytest.fixture
def mock_generate_advice():
    with patch("app.services.service.generate_advice") as mock:
        yield mock

def test_chat(mock_generate_advice):
    mock_generate_advice.return_value = "This is a test response"
    query = {"message": "What is the best investment plan?"}
    response = client.post("/chat", json=query)
    assert response.status_code == 200
    assert response.json() == {"response": "This is a test response"}


