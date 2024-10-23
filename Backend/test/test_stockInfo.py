from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app  # Assuming your FastAPI app is defined in app.main
from requests.exceptions import HTTPError

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

    # Send a GET request to the /stock endpoint
    response = client.get("/stock", params={"name": "AAPL"})

    # Assert the status code is 200 OK
    assert response.status_code == 200

    # Assert the returned data matches the mock
    assert response.json() == {
        "name": "AAPL",
        "price": 150.00,
        "change": "+1.25"
    }

    # Check that the service method was called with the correct argument
    mock_get_stock_info.assert_called_once_with("AAPL")

# Test case for generic Exception
@patch("app.services.service.get_stock_info")
def test_get_stock_generic_error(mock_get_stock_info):
    # Mock a generic Exception
    mock_get_stock_info.side_effect = Exception("Something went wrong")

    # Send a GET request to the /stock endpoint
    response = client.get("/stock", params={"name": "AAPL"})

    # Assert the status code is 500
    assert response.status_code == 500

    # Assert the error detail matches
    assert response.json() == {"detail": "Something went wrong"}
