from unittest.mock import patch, MagicMock
import pandas as pd
import pytest
from portwatch.portfolio import Position, Portfolio
from portwatch.prices import fetch_prices


def make_portfolio(*tickers):
    positions = [Position(ticker=t, shares=10, cost_basis=100.0) for t in tickers]
    return Portfolio(positions=positions)


def test_fetch_prices_single_ticker():
    portfolio = make_portfolio("AAPL")

    mock_data = {
        "Close": pd.Series([195.50])
    }

    with patch("portwatch.prices.yf.download", return_value=mock_data):
        fetch_prices(portfolio)

    assert portfolio.positions[0].current_price == 195.50


def test_fetch_prices_multiple_tickers():
    portfolio = make_portfolio("AAPL", "MSFT")

    mock_close = pd.DataFrame({"AAPL": [195.50], "MSFT": [415.00]})
    mock_data = {"Close": mock_close}

    with patch("portwatch.prices.yf.download", return_value=mock_data):
        fetch_prices(portfolio)

    assert portfolio.positions[0].current_price == 195.50
    assert portfolio.positions[1].current_price == 415.00


def test_fetch_prices_missing_ticker():
    portfolio = make_portfolio("AAPL", "INVALID")

    mock_close = pd.DataFrame({"AAPL": [195.50]})
    mock_data = {"Close": mock_close}

    with patch("portwatch.prices.yf.download", return_value=mock_data):
        fetch_prices(portfolio)

    assert portfolio.positions[0].current_price == 195.50
    assert portfolio.positions[1].current_price == 0.0