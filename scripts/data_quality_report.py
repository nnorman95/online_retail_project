from pathlib import Path

import psycopg


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SQL_FILE = PROJECT_ROOT / "sql" / "08_data_quality_report.sql"

DB_DSN = "dbname=online_retail_project user=norman"


def read_sql(file_path):
    return file_path.read_text(encoding="utf-8")


def print_report(row):
    for column_name, value in row.items():
        print(f"{column_name}: {value}")


def main():
    with psycopg.connect(DB_DSN) as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute(read_sql(SQL_FILE))
            row = cur.fetchone()

    print("Data Quality Report")
    print("-------------------")
    print_report(row)


if __name__ == "__main__":
    main()
