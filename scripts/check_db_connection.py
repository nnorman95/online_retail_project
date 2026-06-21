import psycopg

from config import DB_DSN


with psycopg.connect(DB_DSN) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT current_database(), current_user")
        result = cur.fetchone()

print(result)