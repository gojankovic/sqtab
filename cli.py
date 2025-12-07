import typer

app = typer.Typer(help="sqtab - Minimal CLI for tabular data (CSV/JSON + SQLite).")

@app.command()
def version():
    """
    Show the current sqtab version.
    """
    typer.echo("sqtab version 0.0.1")

if __name__ == "__main__":
    app()
