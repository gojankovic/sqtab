"""
CSV and JSON importer for sqtab.

This module provides basic CSV import functionality. JSON support will be
added in a future commit.
"""

import csv
from typing import Optional
from sqtab.db import get_conn


def import_file(path: str, table: str) -> Optional[int]:
    """
    Import a CSV or JSON file into the specified SQLite table.

    Parameters
    ----------
    path : str
        Path to the input CSV or JSON file.
    table : str
        Name of the SQLite table to import data into.

    Returns
    -------
    Optional[int]
        Number of rows imported, or None if no rows were processed.
    """
    if path.lower().endswith(".csv"):
        return _import_csv(path, table)

    # JSON support coming in future commits.
    raise ValueError("Only CSV import is supported at the moment.")


def _import_csv(path: str, table: str) -> int:
    """
    Import data from a CSV file into a SQLite table.

    The table will be created automatically if it does not exist.

    Returns
    -------
    int
        Number of imported rows.
    """
    conn = get_conn()
    cur = conn.cursor()

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        return 0

    columns = rows[0].keys()
    col_list = ", ".join([f'"{col}"' for col in columns])
    placeholders = ", ".join(["?"] * len(columns))

    # Create table if needed.
    cur.execute(f'CREATE TABLE IF NOT EXISTS "{table}" ({col_list})')

    # Insert rows.
    for row in rows:
        values = list(row.values())
        cur.execute(
            f'INSERT INTO "{table}" VALUES ({placeholders})',
            values
        )

    conn.commit()
    conn.close()
    return len(rows)
