import click
from portwatch.portfolio import load_portfolio
from portwatch.prices import fetch_prices
from portwatch.report import display_report


@click.command()
@click.argument("portfolio_file", default="portfolio.csv")
@click.option("--no-fetch", is_flag=True, default=False, help="Skip live price fetch")
@click.option("--export", type=click.Path(), default=None, help="Export results to a JSON file")
def main(portfolio_file: str, no_fetch: bool, export: str) -> None:
    """Portfolio tracker — display live P&L for your stock positions."""

    click.echo(f"Loading portfolio from {portfolio_file}...")

    try:
        portfolio = load_portfolio(portfolio_file)
    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)

    if not no_fetch:
        click.echo("Fetching live prices...")
        fetch_prices(portfolio)

    display_report(portfolio)

    if export:
        _export_json(portfolio, export)
        click.echo(f"Exported to {export}")


def _export_json(portfolio, filepath: str) -> None:
    import json
    from dataclasses import asdict

    data = {
        "positions": [asdict(p) for p in portfolio.positions],
        "summary": {
            "total_cost": portfolio.total_cost,
            "total_value": portfolio.total_value,
            "total_gain_loss": portfolio.total_gain_loss,
            "total_gain_loss_pct": portfolio.total_gain_loss_pct,
        }
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
