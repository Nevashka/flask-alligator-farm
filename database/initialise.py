from dotenv import load_dotenv
import psycopg2
from os import environ
from bcrypt import hashpw, gensalt

load_dotenv()

URL = environ.get("DATABASE_URL")

conn = psycopg2.connect(URL)

setup_statement = """
    CREATE EXTENSION IF NOT EXISTS citext;
    CREATE DOMAIN email_address AS citext
    CHECK ( value ~* '^[a-z0-9.!#$%&''*+/=?^_`{|}~-]+@[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)*$' );

    CREATE TYPE user_role_type AS ENUM ('admin', 'user');

    CREATE TABLE IF NOT EXISTS user_account (
        id SERIAL PRIMARY KEY,
        username citext NOT NULL
        CONSTRAINT duplicate_username UNIQUE
        CONSTRAINT username_length CHECK (LENGTH(username) BETWEEN 3 AND 30),
        password CHAR(60) NOT NULL,
        email email_address
        CONSTRAINT duplicate_email UNIQUE,
        role user_role_type DEFAULT 'user'
    );

    CREATE TABLE IF NOT EXISTS alligator (
        id SERIAL PRIMARY KEY,
        name VARCHAR(20) NOT NULL,
        age INTEGER NOT NULL
    );
    COMMIT TRANSACTION;
"""

username = environ.get("ADMIN_USERNAME")
password = bytes(environ.get("ADMIN_PASSWORD"), 'utf-8')
hashed = hashpw(password,
                gensalt(int(environ.get("BCRYPT_SALT_ROUNDS")) + 2)).decode()


seed_statement = """
    INSERT INTO user_account (
        username,
        password,
        email,
        role
    ) VALUES (
        %s,
        %s,
        NULL,
        'admin'
    );
"""

with conn.cursor() as curs:
        curs.execute(setup_statement)
        curs.execute(seed_statement, [username, hashed])
        conn.commit()