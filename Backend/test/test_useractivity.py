from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch


client = TestClient(app)

# Mock service.get_user_count_from_db
@patch("app.services.service.get_user_count_from_db")
def test_get_user_count(mock_get_user_count):
    mock_get_user_count.return_value = 100
    response = client.get("/user-count")
    assert response.status_code == 200
    assert response.json() == {"user_count": 100}
    mock_get_user_count.assert_called_once()
