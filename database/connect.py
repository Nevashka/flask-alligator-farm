from sqlalchemy import create_engine
from os import environ

engine = create_engine(environ.get("DB_URL"))

setup_statement = """
    CREATE TABLE IF NOT EXISTS alligator (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL
    );
"""

with engine.connect() as conn:
    conn.execute(setup_statement)