"""
Importer module for sqtab.

Provides utilities for importing tabular data (CSV or JSON) into the default
SQLite database. This is the initial skeleton; full implementation will follow.
"""

from typing import Optional
from db import get_conn


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
        The number of rows imported, or None if the implementation is pending.

    Notes
    -----
    - CSV support will be added in a future commit.
    - JSON support will be added in a future commit.
    - The table will be created automatically if it does not exist.
    """
    # TODO: Implement CSV and JSON import logic.
    return None
