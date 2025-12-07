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
    Requires OPENAI_API_KEY to be set.
    """

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "AI analysis unavailable: please set OPENAI_API_KEY in .env"

    client = OpenAI(api_key=api_key)

    # Convert schema into clean Markdown text
    schema_md = "\n".join(
        f"- **{col['name']}** ({col['type']})"
        for col in info["schema"]
    )

    # Format samples as Markdown table
    samples_md = format_samples_md(info["samples"])

    prompt = dedent(f"""
    You are a senior data analyst. Analyze the following SQLite table.

    ## TABLE NAME
    {table}

    ## SCHEMA
    {schema_md}

    ## SAMPLE ROWS
    {samples_md}

    ### TASKS
    - Describe the likely purpose of this table.
    - Explain what each column represents.
    - Identify potential data quality issues (nulls, outliers, duplicates, inconsistencies).
    - Suggest 3–5 practical SQL queries for exploring this data.
    """)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=600,
    )

    return response.choices[0].message.content.strip()


def format_samples_md(samples: list) -> str:
    """
    Convert sample rows into a compact Markdown table.
    """
    if not samples:
        return "_No sample rows available._"

    headers = samples[0].keys()
    header_row = " | ".join(headers)
    separator = " | ".join(["---"] * len(headers))

    data_rows = []
    for row in samples:
        data_rows.append(" | ".join(str(row[h]) for h in headers))

    return "\n".join([header_row, separator] + data_rows)
