"""
CLI interface for sqtab.

Defines the public command-line interface using Typer.
Commands are currently skeletons and will be implemented in future commits.
"""

import os
import typer
import sqlite3
from sqtab.importer import import_file
from sqtab.exporter import export_csv, export_json
from sqtab.analyzer import analyze_table
from sqtab.logger import log
from sqtab.db import DB_PATH

app = typer.Typer(help="sqtab - Minimal CLI for tabular data (CSV/JSON + SQLite).")


@app.command()
def version():
    """
    Show the current sqtab version.
    """
    typer.echo("sqtab version 0.0.1")


@app.command("import")
def import_command(path: str, table: str):
    """
    Import a CSV or JSON file into a SQLite table.
    (Skeleton implementation.)
    """
    result = import_file(path, table)
    log(f"Import called for path={path}, table={table}")
    typer.echo(f"Import command executed (rows imported: {result}).")


@app.command("export")
def export_command(table: str, csv: str = None, json: str = None):
    """
    Export a SQLite table to CSV or JSON.
    (Skeleton implementation.)
    """
    if csv:
        result = export_csv(table, csv)
        typer.echo(f"Exported to CSV (rows: {result}).")

    if json:
        result = export_json(table, json)
        typer.echo(f"Exported to JSON (rows: {result}).")

    log(f"Export called for table={table}, csv={csv}, json={json}")


@app.command("sql")
def sql_command(query: str):
    """
    Execute a raw SQL query on the SQLite database.
    (Skeleton implementation.)
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    rows = cur.execute(query).fetchall()
    conn.close()

    typer.echo(rows)
    log(f"SQL executed: {query}")


@app.command("analyze")
def analyze_command(table: str):
    """
    Analyze a SQLite table using AI.
    (Skeleton implementation.)
    """
    output = analyze_table(table)
    typer.echo(output)
    log(f"Analyze called for table={table}")


@app.command("reset")
def reset_command():
    """
    Reset (delete) the SQLite database file.
    """
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        log("Database reset.")
        typer.echo("database.db removed.")
    else:
        typer.echo("database.db does not exist.")
