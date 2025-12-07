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


def run_ai_analysis(
    table: str,
    info: dict,
    tasks: list[str] | None = None,
    rules: list[str] | None = None,
) -> str:
    """
    Generate an AI interpretation of table structure and sample data.
    Users can optionally override TASKS and RULES for fully custom analysis.
    Requires OPENAI_API_KEY to be set.
    """

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "AI analysis unavailable: please set OPENAI_API_KEY in .env"

    client = OpenAI(api_key=api_key)

    # -----------------------
    # DEFAULT TASKS & RULES
    # -----------------------
    default_tasks = [
        "Describe the purpose of this table.",
        "Interpret column meanings.",
        "Identify potential data issues (nulls, outliers, inconsistencies).",
        "Suggest 3–5 useful SQL queries for exploring this data.",
    ]

    default_rules = [
        "Respond using clean and properly structured Markdown.",
        "SQL queries must be valid SQLite syntax.",
        "Do not invent columns or data that do not exist.",
        "Be analytical, factual, and concise.",
    ]

    tasks = tasks or default_tasks
    rules = rules or default_rules

    # Format TASKS and RULES as Markdown lists
    tasks_md = "\n".join(f"- {t}" for t in tasks)
    rules_md = "\n".join(f"- {r}" for r in rules)

    # Helper converts first 5 rows to Markdown table
    schema_md = render_schema_md(info["schema"])
    samples_md = render_samples_md(info["samples"])

    # -----------------------
    # BUILD PROMPT
    # -----------------------
    prompt = dedent(f"""
    You are a senior data analyst helping a user understand SQLite data.

    ## TABLE NAME
    {table}

    ## SCHEMA
    {schema_md}

    ## SAMPLE ROWS
    {samples_md}

    ## TASKS
    {tasks_md}

    ## RULES
    {rules_md}
    """)

    # -----------------------
    # OPENAI CALL
    # -----------------------
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
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

def render_schema_md(schema: list[dict]) -> str:
    """Render schema into a clean Markdown table."""
    lines = ["| Name | Type | Not Null | Primary Key |", "|---|---|---|---|"]
    for col in schema:
        lines.append(
            f"| {col['name']} | {col['type']} | {col['not_null']} | {col['primary_key']} |"
        )
    return "\n".join(lines)


def render_samples_md(samples: list[dict]) -> str:
    """Render sample rows into a Markdown table."""
    if not samples:
        return "_No sample rows available_"

    columns = samples[0].keys()
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"

    rows = []
    for row in samples[:5]:  # limit 5 rows for clarity
        rows.append("| " + " | ".join(str(row[col]) for col in columns) + " |")

    return "\n".join([header, separator] + rows)

