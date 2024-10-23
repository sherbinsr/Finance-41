import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

@pytest.fixture
def mock_fetch_market_trends():
    with patch("app.services.service.market_trends") as mock:
        yield mock

def test_get_market_trends_success(mock_fetch_market_trends):
    mock_fetch_market_trends.return_value = {
        "trending_stocks": {
            "top_gainers": [
                {
                    "ticker_id": "S0003015",
                    "company_name": "Bajaj Finance",
                    "price": "6995.8",
                    "percent_change": "4.76",
                    "net_change": "317.9",
                    "bid": "6995.8",
                    "ask": "0",
                    "high": "7098.85",
                    "low": "6601",
                    "open": "6605.75",
                    "low_circuit_limit": "6010.15",
                    "up_circuit_limit": "7345.65",
                    "volume": "2637180",
                    "date": "2024-10-23",
                    "time": "10:14:54",
                    "close": "6677.9",
                    "bid_size": "414",
                    "ask_size": "0",
                    "exchange_type": "NSI",
                    "lot_size": "1",
                    "year_low": "6187.8",
                    "year_high": "7884.9",
                    "ric": "BJFN.NS"
                },
                {
                    "ticker_id": "S0003115",
                    "company_name": "Tech Mahindra",
                    "price": "1735.95",
                    "percent_change": "2.32",
                    "net_change": "39.4",
                    "bid": "0",
                    "ask": "1735.95",
                    "high": "1749",
                    "low": "1685.6",
                    "open": "1696.55",
                    "low_circuit_limit": "1526.9",
                    "up_circuit_limit": "1866.2",
                    "volume": "4198484",
                    "date": "2024-10-23",
                    "time": "10:14:55",
                    "close": "1696.55",
                    "bid_size": "0",
                    "ask_size": "522",
                    "exchange_type": "NSI",
                    "lot_size": "1",
                    "year_low": "1098.15",
                    "year_high": "1761.85",
                    "ric": "TEML.NS"
                },
                {
                    "ticker_id": "S0003120",
                    "company_name": "Bajaj Auto",
                    "price": "10586.75",
                    "percent_change": "2.11",
                    "net_change": "218.4",
                    "bid": "0",
                    "ask": "10586.75",
                    "high": "10735.1",
                    "low": "10342.45",
                    "open": "10368",
                    "low_circuit_limit": "9331.55",
                    "up_circuit_limit": "11405.15",
                    "volume": "1323845",
                    "date": "2024-10-23",
                    "time": "10:11:32",
                    "close": "10368.35",
                    "bid_size": "0",
                    "ask_size": "425",
                    "exchange_type": "NSI",
                    "lot_size": "1",
                    "year_low": "5236",
                    "year_high": "12774",
                    "ric": "BAJA.NS"
                }
            ],
            "top_losers": [
                {
                    "ticker_id": "S0003059",
                    "company_name": "Mahindra & Mahindra",
                    "price": "2793.5",
                    "percent_change": "-3.25",
                    "net_change": "-93.7",
                    "bid": "2793.5",
                    "ask": "0",
                    "high": "2924.9",
                    "low": "2781.25",
                    "open": "2876.15",
                    "low_circuit_limit": "2598.5",
                    "up_circuit_limit": "3175.9",
                    "volume": "7913765",
                    "date": "2024-10-23",
                    "time": "10:12:04",
                    "close": "2887.2",
                    "bid_size": "29633",
                    "ask_size": "0",
                    "exchange_type": "NSI",
                    "lot_size": "1",
                    "year_low": "1450",
                    "year_high": "3222.1",
                    "ric": "MAHM.NS"
                },
                {
                    "ticker_id": "S0003089",
                    "company_name": "Sun Pharmaceutical Industries",
                    "price": "1839.35",
                    "percent_change": "-2.55",
                    "net_change": "-48.2",
                    "bid": "0",
                    "ask": "1839.35",
                    "high": "1889.55",
                    "low": "1832",
                    "open": "1880.05",
                    "low_circuit_limit": "1698.8",
                    "up_circuit_limit": "2076.3",
                    "volume": "1673338",
                    "date": "2024-10-23",
                    "time": "10:14:22",
                    "close": "1887.55",
                    "bid_size": "0",
                    "ask_size": "220",
                    "exchange_type": "NSI",
                    "lot_size": "1",
                    "year_low": "1068.35",
                    "year_high": "1960.35",
                    "ric": "SUN.NS"
                },
                {
                    "ticker_id": "S0003068",
                    "company_name": "Power Grid Corporation Of India",
                    "price": "316.9",
                    "percent_change": "-1.81",
                    "net_change": "-5.85",
                    "bid": "0",
                    "ask": "316.9",
                    "high": "321.9",
                    "low": "313.85",
                    "open": "319.2",
                    "low_circuit_limit": "290.5",
                    "up_circuit_limit": "355",
                    "volume": "12541366",
                    "date": "2024-10-23",
                    "time": "10:14:36",
                    "close": "322.75",
                    "bid_size": "0",
                    "ask_size": "963",
                    "exchange_type": "NSI",
                    "lot_size": "1",
                    "year_low": "196.3",
                    "year_high": "366.25",
                    "ric": "PGRD.NS"
                }
            ]
        }
    }



