from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app


client = TestClient(app)

# Test case for successful stock information retrieval
@patch("app.services.service.get_stock_info")
def test_get_stock_success(mock_get_stock_info):
    # Mock a successful stock response
    mock_get_stock_info.return_value = {
        "name": "AAPL",
        "price": 150.00,
        "change": "+1.25"
    }

    response = client.get("/stock", params={"name": "AAPL"})
    assert response.status_code == 200
    assert response.json() == {
        "name": "AAPL",
        "price": 150.00,
        "change": "+1.25"
    }
    mock_get_stock_info.assert_called_once_with("AAPL")

# Test case for generic Exception
@patch("app.services.service.get_stock_info")
def test_get_stock_generic_error(mock_get_stock_info):
    mock_get_stock_info.side_effect = Exception("Something went wrong")
    response = client.get("/stock", params={"name": "AAPL"})
    assert response.status_code == 500
    assert response.json() == {"detail": "Something went wrong"}
