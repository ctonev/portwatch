from click.testing import CliRunner
from portwatch.cli import main
from unittest.mock import patch


def make_csv(tmp_path):
    csv_content = "ticker,shares,cost_basis\nAAPL,10,150.00\nMSFT,5,300.00\n"
    csv_file = tmp_path / "portfolio.csv"
    csv_file.write_text(csv_content)
    return str(csv_file)


def test_cli_runs_with_no_fetch(tmp_path):
    runner = CliRunner()
    csv_file = make_csv(tmp_path)

    result = runner.invoke(main, [csv_file, "--no-fetch"])

    assert result.exit_code == 0
    assert "AAPL" in result.output
    assert "MSFT" in result.output


def test_cli_missing_file():
    runner = CliRunner()

    result = runner.invoke(main, ["nonexistent.csv", "--no-fetch"])

    assert result.exit_code == 1


def test_cli_export_json(tmp_path):
    runner = CliRunner()
    csv_file = make_csv(tmp_path)
    export_file = str(tmp_path / "output.json")

    result = runner.invoke(main, [csv_file, "--no-fetch", "--export", export_file])

    assert result.exit_code == 0
    assert "Exported" in result.output

    import json
    with open(export_file) as f:
        data = json.load(f)

    assert len(data["positions"]) == 2
    assert data["summary"]["total_cost"] == 3000.0
