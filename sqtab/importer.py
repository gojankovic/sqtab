"""
CSV and JSON importer for sqtab.

This module provides basic CSV import functionality. JSON support will be
added in a future commit.
"""

import csv
import json
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
    path = str(path)
    path_lower = path.lower()

    if path_lower.endswith(".csv"):
        return _import_csv(path, table)

    if path_lower.endswith(".json"):
        return _import_json(path, table)

    raise ValueError("Only CSV and JSON import are supported at the moment.")


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


def _import_json(path: str, table: str) -> int:
    """
    Import data from a JSON file into a SQLite table.

    The JSON file must contain either:
    - a list of objects (recommended), or
    - a single object (will be wrapped into a list)

    Returns
    -------
    int
        Number of rows imported.
    """
    conn = get_conn()
    cur = conn.cursor()

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        # Single object → wrap into a list
        rows = [data]
    elif isinstance(data, list):
        rows = data
    else:
        raise ValueError("Invalid JSON format. Expected object or list of objects.")

    if not rows:
        return 0

    columns = rows[0].keys()
    col_list = ", ".join([f'"{col}"' for col in columns])
    placeholders = ", ".join(["?"] * len(columns))

    # Create table if needed
    cur.execute(f'CREATE TABLE IF NOT EXISTS "{table}" ({col_list})')

    # Insert rows
    for row in rows:
        values = list(row.values())
        cur.execute(
            f'INSERT INTO "{table}" VALUES ({placeholders})',
            values
        )

    conn.commit()
    conn.close()
    return len(rows)

