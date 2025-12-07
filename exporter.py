"""
Exporter module for sqtab.

Provides utilities for exporting SQLite tables to CSV or JSON files.
This is the initial skeleton; full implementation will be added in future commits.
"""

from typing import Optional
from db import get_conn


def export_csv(table: str, path: str) -> Optional[int]:
    """
    Export a SQLite table to a CSV file.

    Parameters
    ----------
    table : str
        Name of the SQLite table to export.
    path : str
        Destination path for the CSV output file.

    Returns
    -------
    Optional[int]
        The number of exported rows, or None if implementation is pending.

    Notes
    -----
    - CSV export logic will be implemented in a future commit.
    - The function should automatically fetch all rows and write them to disk.
    """
    # TODO: Implement CSV export logic.
    return None


def export_json(table: str, path: str) -> Optional[int]:
    """
    Export a SQLite table to a JSON file.

    Parameters
    ----------
    table : str
        Name of the SQLite table to export.
    path : str
        Destination path for the JSON output file.

    Returns
    -------
    Optional[int]
        The number of exported rows, or None if implementation is pending.

    Notes
    -----
    - JSON export logic will be implemented in a future commit.
    - Rows should be converted to dictionaries keyed by column names.
    """
    # TODO: Implement JSON export logic.
    return None
