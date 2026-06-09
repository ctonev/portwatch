# portwatch

A CLI tool to track and report live P&L for your personal stock portfolio.

## Installation

```bash
pip install portwatch
```

## Usage

Create a CSV file with your holdings:


```bash
ticker,shares,cost_basis
AAPL,10,150.00
MSFT,5,300.00
```

Then run:

```bash
# Display live portfolio report
portwatch portfolio.csv

# Skip live price fetch
portwatch portfolio.csv --no-fetch

# Export results to JSON
portwatch portfolio.csv --export results.json
```

## License

MIT
