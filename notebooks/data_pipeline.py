import marimo

__generated_with = "0.14.12"
app = marimo.App(width="medium")


@app.cell
def _():
    import json
    from pathlib import Path
    import sys
    from src.data_models import InputTransactions
    import pandas as pd
    import duckdb
    from dotenv import load_dotenv
    _ = load_dotenv(override=True)
    sys.path.append("..")
    return InputTransactions, Path, duckdb, pd


@app.cell
def _(InputTransactions, Path, pd):
    def load_data(filepath: Path):
        with filepath.open("+r", encoding="utf-8") as f:
            data = pd.read_json(f)
        try:
            InputTransactions.validate(data)
        except Exception as e:
            print(f"Error raised during dataframe validation {e}")
        return data
    return (load_data,)


@app.cell
def _(Path):
    data_path = Path(__file__).parents[1]/"data/financial_transactions.json"
    return (data_path,)


@app.cell
def _(data_path, load_data):
    data = load_data(data_path)
    return (data,)


@app.cell
def _(data):
    data
    return


@app.cell
def _(data):
    data.groupby("year").sum("amount")
    return


@app.cell
def _(duckdb):
    table_name = "transactions"
    duckdb.sql(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM data")

    return


@app.cell
def _():
    from src.agent import triage_agent
    from agents.extensions.visualization import draw_graph
    return draw_graph, triage_agent


@app.cell
def _(draw_graph, triage_agent):
    draw_graph(triage_agent,filename="data/triage")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
