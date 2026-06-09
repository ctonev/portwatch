import yfinance as yf
from portwatch.portfolio import Portfolio


def fetch_prices(portfolio: Portfolio) -> None:
    tickers = [p.ticker for p in portfolio.positions]
    data = yf.download(tickers, period="1d", auto_adjust=True, progress=False)

    for position in portfolio.positions:
        try:
            if len(tickers) == 1:
                price = float(data["Close"].iloc[-1])
            else:
                price = float(data["Close"][position.ticker].iloc[-1])
            position.current_price = price
        except (KeyError, IndexError):
            print(f"Warning: could not fetch price for {position.ticker}")
