import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from portwatch.api import app
from portwatch.portfolio import Position, Portfolio


client = TestClient(app)


def make_portfolio():
    positions = [
        Position(ticker="AAPL", shares=10, cost_basis=150.0, current_price=0.0),
        Position(ticker="MSFT", shares=5, cost_basis=300.0, current_price=0.0),
    ]
    return Portfolio(positions=positions)


def test_get_portfolio():
    portfolio = make_portfolio()
    with patch("portwatch.api.load_portfolio", return_value=portfolio):
        response = client.get("/portfolio")

    assert response.status_code == 200
    data = response.json()
    assert len(data["positions"]) == 2
    assert data["positions"][0]["ticker"] == "AAPL"
    assert data["total_cost"] == 3000.0


def test_get_portfolio_file_not_found():
    with patch("portwatch.api.load_portfolio", side_effect=FileNotFoundError):
        response = client.get("/portfolio")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_get_portfolio_with_prices():
    portfolio = make_portfolio()

    def mock_fetch(p):
        for position in p.positions:
            position.current_price = 200.0

    with patch("portwatch.api.load_portfolio", return_value=portfolio):
        with patch("portwatch.api.fetch_prices", side_effect=mock_fetch):
            response = client.get("/portfolio/prices")

    assert response.status_code == 200
    data = response.json()
    assert data["positions"][0]["current_price"] == 200.0
    assert data["total_value"] == 3000.0


def test_get_position():
    portfolio = make_portfolio()
    with patch("portwatch.api.load_portfolio", return_value=portfolio):
        response = client.get("/portfolio/AAPL")

    assert response.status_code == 200
    data = response.json()
    assert data["ticker"] == "AAPL"
    assert data["shares"] == 10.0


def test_get_position_case_insensitive():
    portfolio = make_portfolio()
    with patch("portwatch.api.load_portfolio", return_value=portfolio):
        response = client.get("/portfolio/aapl")

    assert response.status_code == 200
    assert response.json()["ticker"] == "AAPL"


def test_get_position_not_found():
    portfolio = make_portfolio()
    with patch("portwatch.api.load_portfolio", return_value=portfolio):
        response = client.get("/portfolio/TSLA")

    assert response.status_code == 404