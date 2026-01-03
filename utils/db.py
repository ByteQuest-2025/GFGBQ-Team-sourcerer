import os
import psycopg2
import psycopg2.extras


def get_conn():
    """
    Create and return a database connection using DATABASE_URL env variable.
    """
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is not set.\n"
            "Example:\n"
            "postgresql://user:password@host:5432/dbname?sslmode=require"
        )

    return psycopg2.connect(database_url)


def fetch_all(sql, params=None):
    """
    Execute SELECT query and return all rows as list of dicts.
    """
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params or ())
            return cur.fetchall()
    finally:
        conn.close()


def fetch_one(sql, params=None):
    """
    Execute SELECT query and return a single row as dict.
    """
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params or ())
            return cur.fetchone()
    finally:
        conn.close()


def execute(sql, params=None):
    """
    Execute INSERT / UPDATE / DELETE query.
    """
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
        conn.commit()
    finally:
        conn.close()