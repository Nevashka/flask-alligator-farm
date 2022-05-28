import psycopg2
from os import environ

URL = environ.get("DATABASE_URL")

conn = psycopg2.connect(URL)

statement = """
    CREATE TABLE IF NOT EXISTS alligator (
        id SERIAL PRIMARY KEY,
        name VARCHAR(20) NOT NULL,
        age INTEGER NOT NULL
    );
"""

with conn.cursor() as curs:
        curs.execute(statement)