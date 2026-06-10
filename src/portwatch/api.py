from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from portwatch.portfolio import load_portfolio, Portfolio
from portwatch.prices import fetch_prices


app = FastAPI(
    title="Portwatch API",
    description="REST API for tracking and reporting on a personal stock portfolio",
    version="0.1.1",
)

PORTFOLIO_FILE = "portfolio.csv"


class PositionResponse(BaseModel):
    ticker: str
    shares: float
    cost_basis: float
    current_price: float
    market_value: float
    gain_loss: float
    gain_loss_pct: float


class PortfolioResponse(BaseModel):
    positions: list[PositionResponse]
    total_cost: float
    total_value: float
    total_gain_loss: float
    total_gain_loss_pct: float


def portfolio_to_response(portfolio: Portfolio) -> PortfolioResponse:
    positions = [
        PositionResponse(
            ticker=p.ticker,
            shares=p.shares,
            cost_basis=p.cost_basis,
            current_price=p.current_price,
            market_value=p.market_value,
            gain_loss=p.gain_loss,
            gain_loss_pct=p.gain_loss_pct,
        )
        for p in portfolio.positions
    ]
    return PortfolioResponse(
        positions=positions,
        total_cost=portfolio.total_cost,
        total_value=portfolio.total_value,
        total_gain_loss=portfolio.total_gain_loss,
        total_gain_loss_pct=portfolio.total_gain_loss_pct,
    )


@app.get("/portfolio", response_model=PortfolioResponse)
async def get_portfolio():
    """Load and return portfolio without live prices."""
    try:
        portfolio = load_portfolio(PORTFOLIO_FILE)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Portfolio file not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return portfolio_to_response(portfolio)


@app.get("/portfolio/prices", response_model=PortfolioResponse)
async def get_portfolio_with_prices():
    """Load portfolio and fetch live prices."""
    try:
        portfolio = load_portfolio(PORTFOLIO_FILE)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Portfolio file not found")
    fetch_prices(portfolio)
    return portfolio_to_response(portfolio)


@app.get("/portfolio/{ticker}", response_model=PositionResponse)
async def get_position(ticker: str):
    """Get a single position by ticker."""
    try:
        portfolio = load_portfolio(PORTFOLIO_FILE)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Portfolio file not found")
    ticker = ticker.upper()
    for position in portfolio.positions:
        if position.ticker == ticker:
            return PositionResponse(
                ticker=position.ticker,
                shares=position.shares,
                cost_basis=position.cost_basis,
                current_price=position.current_price,
                market_value=position.market_value,
                gain_loss=position.gain_loss,
                gain_loss_pct=position.gain_loss_pct,
            )
    raise HTTPException(status_code=404, detail=f"Ticker {ticker} not found")