from rich.console import Console
from rich.table import Table
from rich import box
from portwatch.portfolio import Portfolio

console = Console()


def display_report(portfolio: Portfolio) -> None:
    table = Table(
        title="Portfolio Summary",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column("Ticker", style="bold white", justify="left")
    table.add_column("Shares", justify="right")
    table.add_column("Cost Basis", justify="right")
    table.add_column("Current Price", justify="right")
    table.add_column("Market Value", justify="right")
    table.add_column("Gain/Loss", justify="right")
    table.add_column("Return %", justify="right")

    for position in portfolio.positions:
        gain_loss_color = "green" if position.gain_loss >= 0 else "red"
        table.add_row(
            position.ticker,
            f"{position.shares:.2f}",
            f"${position.cost_basis:.2f}",
            f"${position.current_price:.2f}",
            f"${position.market_value:.2f}",
            f"[{gain_loss_color}]${position.gain_loss:.2f}[/{gain_loss_color}]",
            f"[{gain_loss_color}]{position.gain_loss_pct:.2f}%[/{gain_loss_color}]",
        )

    console.print(table)
    console.print()

    total_color = "green" if portfolio.total_gain_loss >= 0 else "red"
    console.print(f"[bold]Total Cost:[/bold]        ${portfolio.total_cost:,.2f}")
    console.print(f"[bold]Total Value:[/bold]       ${portfolio.total_value:,.2f}")
    console.print(f"[bold]Total Gain/Loss:[/bold]   [{total_color}]${portfolio.total_gain_loss:,.2f} ({portfolio.total_gain_loss_pct:.2f}%)[/{total_color}]")
    