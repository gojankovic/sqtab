"""
CLI interface for sqtab.

Defines the public command-line interface using Typer.
Commands are currently skeletons and will be implemented in future commits.
"""

import os
import sqlite3
import typer

from rich.console import Console
from rich.table import Table
from pathlib import Path
from sqtab.importer import import_file
from sqtab.exporter import export_csv, export_json
from sqtab.analyzer import analyze_table
from sqtab.logger import log
from sqtab.db import DB_PATH, get_conn

app = typer.Typer(help="sqtab - Minimal CLI for tabular data (CSV/JSON + SQLite).")

console = Console()

EXPORT_DIR = Path("exports")
EXPORT_DIR.mkdir(exist_ok=True)

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
def export_cmd(table: str, path: str = None):
    """
    Export a SQLite table to CSV or JSON. (CSV implemented)
    """
    # If no output path is provided, generate one automatically.
    if path is None:
        path = EXPORT_DIR / f"{table}.csv"
    else:
        path = Path(path)

    lower = str(path).lower()

    if lower.endswith(".csv"):
        rows = export_csv(table, path)
        print(f"Exported {rows} rows to {path}.")
        return

    if lower.endswith(".json"):
        rows = export_json(table, path)
        print(f"Exported {rows} rows to {path}.")
        return

    print("Unsupported export format. Use .csv or .json.")


@app.command("sql")
def sql_command(query: str):
    """
    Execute a raw SQL query on the SQLite database.

    - For SELECT-like statements, prints a formatted table of results.
    - For modification statements (INSERT/UPDATE/DELETE/etc.), prints affected row count.
    """
    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute(query)
        stripped = query.strip().lower()

        if stripped.startswith("select"):
            rows = cur.fetchall()

            if not rows:
                typer.echo("No rows returned.")
            else:
                headers = [col[0] for col in cur.description]

                table = Table(show_header=True, header_style="bold")
                for h in headers:
                    table.add_column(h)

                for row in rows:
                    table.add_row(*[str(value) for value in row])

                console.print(table)
        else:
            conn.commit()
            affected = cur.rowcount
            typer.echo(f"Query executed. Rows affected: {affected}")

        log(f"SQL executed successfully: {query}")

    except sqlite3.Error as exc:
        log(f"SQL error for query={query!r}: {exc}")
        typer.echo(f"Error executing SQL: {exc}")
        raise typer.Exit(code=1)
    finally:
        conn.close()


@app.command("tables")
def tables_command():
    """
    List all tables in the SQLite database.
    """
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        typer.echo("No tables found.")
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("Table Name")

    for (name,) in rows:
        table.add_row(name)

    console.print(table)

    log("Listed all tables.")


@app.command("analyze")
def analyze_cmd(table: str):
    """
    Analyze a SQLite table and output structural information.
    (AI integration will be added later.)
    """
    try:
        summary = analyze_table(table)
    except ValueError as exc:
        typer.echo(f"Error: {exc}")
        raise typer.Exit(code=1)

    console.print(f"[bold]Table:[/bold] {summary['table']}")
    console.print(f"[bold]Rows:[/bold] {summary['rows']}")
    console.print(f"[bold]Columns:[/bold] {summary['column_count']}")

    # Pretty print column structure
    from rich.table import Table as RichTable
    col_table = RichTable(show_header=True, header_style="bold")
    col_table.add_column("Name")
    col_table.add_column("Type")
    col_table.add_column("Not Null")
    col_table.add_column("Primary Key")

    for col in summary["columns"]:
        col_table.add_row(
            col["name"],
            col["type"],
            str(col["not_null"]),
            str(col["primary_key"]),
        )

    console.print(col_table)

    log(f"Analyzed table {table}.")

    # AI placeholder
    console.print(
        "[green]\nAI analysis not implemented yet — summary prepared.[/green]"
    )


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
