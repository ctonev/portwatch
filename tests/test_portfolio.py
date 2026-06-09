import pytest
from portwatch.portfolio import Position, Portfolio, load_portfolio


def test_position_market_value():
    pos = Position(ticker="AAPL", shares=10, cost_basis=150.0, current_price=200.0)
    assert pos.market_value == 2000.0


def test_position_gain_loss():
    pos = Position(ticker="AAPL", shares=10, cost_basis=150.0, current_price=200.0)
    assert pos.gain_loss == 500.0


def test_position_gain_loss_pct():
    pos = Position(ticker="AAPL", shares=10, cost_basis=150.0, current_price=200.0)
    assert pos.gain_loss_pct == pytest.approx(33.33, rel=1e-2)


def test_portfolio_totals():
    positions = [
        Position(ticker="AAPL", shares=10, cost_basis=150.0, current_price=200.0),
        Position(ticker="MSFT", shares=5, cost_basis=300.0, current_price=400.0),
    ]
    portfolio = Portfolio(positions=positions)
    assert portfolio.total_cost == 3000.0
    assert portfolio.total_value == 4000.0

def test_load_portfolio(tmp_path):
    csv_content = "ticker,shares,cost_basis\nAAPL,10,150.00\nMSFT,5,300.00\n"
    csv_file = tmp_path / "portfolio.csv"
    csv_file.write_text(csv_content)

    portfolio = load_portfolio(csv_file)

    assert len(portfolio.positions) == 2
    assert portfolio.positions[0].ticker == "AAPL"
    assert portfolio.positions[0].shares == 10.0
    assert portfolio.positions[1].ticker == "MSFT"


def test_load_portfolio_file_not_found():
    import pytest
    with pytest.raises(FileNotFoundError):
        load_portfolio("nonexistent.csv")


def test_load_portfolio_uppercases_ticker(tmp_path):
    csv_content = "ticker,shares,cost_basis\naapl,10,150.00\n"
    csv_file = tmp_path / "portfolio.csv"
    csv_file.write_text(csv_content)

    portfolio = load_portfolio(csv_file)
    assert portfolio.positions[0].ticker == "AAPL"