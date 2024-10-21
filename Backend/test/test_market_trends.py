import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app  # Ensure this points to your FastAPI app

client = TestClient(app)

@pytest.fixture
def mock_fetch_market_trends():
    with patch("app.services.service.fetch_market_trends") as mock:
        yield mock

def test_get_market_trends_success(mock_fetch_market_trends):
    mock_fetch_market_trends.return_value = {"market": "up", "trends": "bullish"}
    response = client.get("/market-trends")
    assert response.status_code == 200
    assert response.json() == {"market": "up", "trends": "bullish"}

def test_get_market_trends_failure(mock_fetch_market_trends):
    mock_fetch_market_trends.side_effect = Exception("Service error")
    response = client.get("/market-trends")
    assert response.status_code == 500
    assert response.json() == {"detail": "Error fetching market trends"}
