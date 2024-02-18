import sqlite3

from actuate.core import action

from actuate.util import shorten_text


@action(name=lambda: f"Execute SQLite statement")
async def execute(db_file: str, statement: str):
    """Execute a statement on a sqlite database."""
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute(statement)
    return c.fetchall()
