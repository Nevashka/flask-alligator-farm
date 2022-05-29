import psycopg2
from os import environ

URL = environ.get("DATABASE_URL")

conn = psycopg2.connect(URL)