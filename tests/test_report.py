from portwatch.portfolio import Position, Portfolio
from portwatch.report import display_report
from rich.console import Console
from io import StringIO


def make_portfolio_with_prices():
    positions = [
        Position(ticker="AAPL", shares=10, cost_basis=150.0, current_price=200.0),
        Position(ticker="MSFT", shares=5, cost_basis=300.0, current_price=250.0),
    ]
    return Portfolio(positions=positions)


def test_display_report_runs_without_error():
    portfolio = make_portfolio_with_prices()
    console = Console(file=StringIO(), highlight=False)
    display_report(portfolio)


def test_display_report_captures_output():
    portfolio = make_portfolio_with_prices()
    buffer = StringIO()
    console = Console(file=buffer, highlight=False, no_color=True)

    from unittest.mock import patch
    with patch("portwatch.report.console", console):
        display_report(portfolio)

    output = buffer.getvalue()
    assert "AAPL" in output
    assert "MSFT" in output
    assert "Portfolio Summary" in output
