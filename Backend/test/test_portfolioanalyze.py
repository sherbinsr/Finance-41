from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app ,schemas


client = TestClient(app)

# portfolio data for testing
sample_portfolio = {
    "items": [
        {"symbol": "AAPL", "quantity": 10, "price": 150.0},
        {"symbol": "GOOGL", "quantity": 5, "price": 2800.0},
    ]
}

# Test case for successful portfolio analysis
@patch("app.services.service.analyze_portfolio")
def test_analyze_portfolio_success(mock_analyze_portfolio):
    mock_analyze_portfolio.return_value = {"risk_score": 0.25, "recommendation": "Low risk"}
    response = client.post("/analyze", json=sample_portfolio)
    expected_total_value = (10 * 150.0) + (5 * 2800.0)
    assert response.status_code == 200
    assert response.json() == {
        "total_value": expected_total_value,
        "total_items": 2,
        "risk_analysis": {
            "risk_score": 0.25,
            "recommendation": "Low risk"
        }
    }
    expected_portfolio_data = {
        "portfolio": [
            {"symbol": "AAPL", "quantity": 10, "price": 150.0},
            {"symbol": "GOOGL", "quantity": 5, "price": 2800.0}
        ]
    }
    mock_analyze_portfolio.assert_called_once_with(expected_portfolio_data)

# Test case for exception during portfolio analysis
@patch("app.services.service.analyze_portfolio")
def test_analyze_portfolio_error(mock_analyze_portfolio):
    mock_analyze_portfolio.side_effect = Exception("Service error")
    response = client.post("/analyze", json=sample_portfolio)
    assert response.status_code == 200
    assert response.json() == {"error": "Error analyzing portfolio: Service error"}
    expected_portfolio_data = {
        "portfolio": [
            {"symbol": "AAPL", "quantity": 10, "price": 150.0},
            {"symbol": "GOOGL", "quantity": 5, "price": 2800.0}
        ]
    }
    mock_analyze_portfolio.assert_called_once_with(expected_portfolio_data)
