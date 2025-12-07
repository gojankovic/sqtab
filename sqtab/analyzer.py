"""
Analyzer module for sqtab.

Provides AI-assisted analysis of SQLite tables. This module will later use
OpenAI models to examine table structure, sample rows, and generate insights
about the dataset.

This is the initial skeleton; full implementation will follow.
"""
import json
import os

from sqtab.db import get_conn
from textwrap import dedent
from openai import OpenAI


def analyze_table(table: str) -> dict:
    """
    Analyze a SQLite table and return structure + sample rows.
    """

    conn = get_conn()
    cur = conn.cursor()

    # table existence check
    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
        (table,)
    )
    if not cur.fetchone():
        raise ValueError(f"Table '{table}' does not exist.")

    # --- 1) Schema ---
    cur.execute(f'PRAGMA table_info("{table}")')
    columns_info = cur.fetchall()

    schema = []
    for cid, name, col_type, notnull, dflt, pk in columns_info:
        schema.append({
            "name": name,
            "type": col_type or "UNKNOWN",
            "not_null": bool(notnull),
            "primary_key": bool(pk)
        })

    # --- 2) Row count ---
    cur.execute(f'SELECT COUNT(*) FROM "{table}"')
    row_count = cur.fetchone()[0]

    # --- 3) Sample rows (first 5) ---
    cur.execute(f'SELECT * FROM "{table}" LIMIT 5')
    rows = cur.fetchall()

    samples = [
        {col["name"]: row[i] for i, col in enumerate(schema)}
        for row in rows
    ]

    conn.close()

    return {
        "table": table,
        "row_count": row_count,
        "column_count": len(schema),
        "schema": schema,
        "samples": samples,
    }


def run_ai_analysis(table: str, info: dict) -> str:
    """
    Generate an AI interpretation of table structure and sample data.
    Requires OPENAI_API_KEY to be set (via .env or OS env).
    """

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "AI analysis unavailable: please set OPENAI_API_KEY in .env"

    client = OpenAI(api_key=api_key)

    prompt = dedent(f"""
    You are a senior data analyst. Analyze the following SQLite table.

    TABLE NAME:
    {table}

    SCHEMA:
    {json.dumps(info["schema"], indent=2)}

    SAMPLE ROWS:
    {json.dumps(info["samples"], indent=2)}

    TASKS:
    - Describe the purpose of this table.
    - Interpret column meanings.
    - Identify potential data issues (nulls, outliers, inconsistencies).
    - Suggest 3–5 useful SQL queries for exploring this data.
    """)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()

