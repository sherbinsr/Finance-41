import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app

client = TestClient(app)

@pytest.fixture
def mock_fetch_market_trends():
    with patch("app.services.service.market_trends", new_callable=AsyncMock) as mock:
        yield mock
@pytest.fixture
def mock_get_users():
    with patch("app.services.service.get_users", new_callable=AsyncMock) as mock:
        yield mock
@pytest.fixture
def mock_send_email():
    with patch("app.services.service.send_email", new_callable=AsyncMock) as mock:
        yield mock

@pytest.fixture
def mock_schedule_task():
    with patch("app.services.service.schedule_task") as mock:
        yield mock

def test_send_market_trends_endpoint(
        mock_fetch_market_trends,
        mock_get_users,
        mock_send_email,
        mock_schedule_task
):
    mock_fetch_market_trends.return_value = ["stock 1", "stock 2", "stock 3"]
    mock_get_users.return_value = ["mailtosherbin@gmail", "bj@gmail.com"]
    response = client.get("/send_market_trends")
    assert response.status_code == 200
    assert response.json() == {"message": "Market trends are being sent to users."}
    mock_fetch_market_trends.assert_called_once()
    mock_get_users.assert_called_once()
