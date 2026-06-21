import io

import pandas as pd
import psycopg

file_path = "data/raw/online_retail.xlsx"

df = pd.read_excel(file_path)

df = df.rename(
    columns={
        "InvoiceNo": "invoice_no",
        "StockCode": "stock_code",
        "Description": "description",
        "Quantity": "quantity",
        "InvoiceDate": "invoice_date",
        "UnitPrice": "unit_price",
        "CustomerID": "customer_id",
        "Country": "country",
    }
)

columns = [
    "invoice_no",
    "stock_code",
    "description",
    "quantity",
    "invoice_date",
    "unit_price",
    "customer_id",
    "country",
]

df = df[columns]

conn = psycopg.connect("dbname=online_retail_project user=norman")
cur = conn.cursor()

cur.execute("TRUNCATE TABLE raw_online_retail;")

buffer = io.StringIO()
df.to_csv(buffer, index=False, header=False, na_rep="\\N")
buffer.seek(0)

with cur.copy(
    """
    COPY raw_online_retail (
        invoice_no,
        stock_code,
        description,
        quantity,
        invoice_date,
        unit_price,
        customer_id,
        country
    )
    FROM STDIN WITH (FORMAT CSV, NULL '\\N')
    """
) as copy:
    copy.write(buffer.read())

conn.commit()

cur.execute("SELECT COUNT(*) FROM raw_online_retail;")
row_count = cur.fetchone()[0]

print("Rows loaded:", row_count)

conn.close()