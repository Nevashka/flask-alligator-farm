from sqlalchemy import create_engine
from os import environ

engine = create_engine(environ.get("DB_URI"))

setup_statement = """
    CREATE TABLE IF NOT EXISTS alligator (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL
    );
"""

seed_statement = """
    INSERT INTO alligator
        (name, age)
    VALUES
        ("Barry", 4),
        ("Leonie", 2),
        ("Melvin", 7)
"""

with engine.connect() as conn:
    conn.execute(setup_statement)
    conn.execute(seed_statement)