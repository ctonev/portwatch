from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Position:
    ticker: str
    shares: float
    cost_basis: float          # price paid per share
    current_price: float = 0.0
    
    @property
    def total_cost(self) -> float:
        return self.shares * self.cost_basis

    @property
    def market_value(self) -> float:
        return self.shares * self.current_price

    @property
    def gain_loss(self) -> float:
        return self.market_value - self.total_cost

    @property
    def gain_loss_pct(self) -> float:
        if self.total_cost == 0:
            return 0.0
        return (self.gain_loss / self.total_cost) * 100


@dataclass
class Portfolio:
    positions: list[Position] = field(default_factory=list)

    @property
    def total_cost(self) -> float:
        return sum(p.total_cost for p in self.positions)

    @property
    def total_value(self) -> float:
        return sum(p.market_value for p in self.positions)

    @property
    def total_gain_loss(self) -> float:
        return self.total_value - self.total_cost

    @property
    def total_gain_loss_pct(self) -> float:
        if self.total_cost == 0:
            return 0.0
        return (self.total_gain_loss / self.total_cost) * 100

import csv
from pathlib import Path

def load_portfolio(filepath: str | Path) -> Portfolio:
    positions = []
    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(f"Portfolio file not found: {filepath}")

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            position = Position(
                ticker=row["ticker"].strip().upper(),
                shares=float(row["shares"]),
                cost_basis=float(row["cost_basis"]),
            )
            positions.append(position)

    if not positions:
        raise ValueError("Portfolio file is empty or has no valid positions")

    return Portfolio(positions=positions)