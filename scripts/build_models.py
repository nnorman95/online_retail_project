from pathlib import Path

import psycopg


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SQL_DIR = PROJECT_ROOT / "sql"

DB_DSN = "dbname=online_retail_project user=norman"

MODEL_SQL_FILES = [
    SQL_DIR / "01_create_staging.sql",
    SQL_DIR / "02_create_fact_invoice_items.sql",
    SQL_DIR / "03_create_dim_products.sql",
    SQL_DIR / "04_create_dim_customers.sql",
    SQL_DIR / "05_create_mart_daily_sales.sql",
    SQL_DIR / "06_create_mart_country_sales.sql",
]

VALIDATION_SQL_FILE = SQL_DIR / "07_validate_revenue.sql"


def read_sql(file_path):
    return file_path.read_text(encoding="utf-8")


def run_sql_file(cursor, file_path):
    cursor.execute(read_sql(file_path))


def validate_revenue(cursor):
    cursor.execute(read_sql(VALIDATION_SQL_FILE))

    fact_revenue, daily_mart_revenue, country_mart_revenue = cursor.fetchone()

    if fact_revenue != daily_mart_revenue or fact_revenue != country_mart_revenue:
        raise ValueError(
            "Revenue validation failed: "
            f"fact={fact_revenue}, "
            f"daily_mart={daily_mart_revenue}, "
            f"country_mart={country_mart_revenue}"
        )


def main():
    with psycopg.connect(DB_DSN) as conn:
        with conn.cursor() as cur:
            for sql_file in MODEL_SQL_FILES:
                run_sql_file(cur, sql_file)
                print(f"Built from {sql_file.name}")

            validate_revenue(cur)
            conn.commit()

    print("Revenue validation passed!")


if __name__ == "__main__":
    main()