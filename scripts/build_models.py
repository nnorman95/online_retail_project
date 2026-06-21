import psycopg

conn = psycopg.connect("dbname=online_retail_project user=norman")
cur = conn.cursor()

cur.execute("""
DROP TABLE IF EXISTS stg_online_retail;

CREATE TABLE stg_online_retail AS
SELECT
    invoice_no,
    stock_code,
    NULLIF(TRIM(description), '') AS description,
    quantity,
    invoice_date,
    unit_price,
    customer_id::INTEGER AS customer_id,
    country,
    invoice_no LIKE 'C%' AS is_cancelled,
    (
        invoice_no NOT LIKE 'C%'
        AND quantity > 0
        AND unit_price > 0
    ) AS is_valid_sale,
    quantity * unit_price AS revenue
FROM raw_online_retail;
""")

cur.execute("""
DROP TABLE IF EXISTS fact_invoice_items;

CREATE TABLE fact_invoice_items AS
SELECT
    invoice_no,
    stock_code,
    quantity,
    invoice_date,
    unit_price,
    customer_id,
    country,
    revenue
FROM stg_online_retail
WHERE is_valid_sale = TRUE;
""")

cur.execute("""
DROP TABLE IF EXISTS dim_products;

CREATE TABLE dim_products AS
SELECT
    stock_code,
    MAX(description) AS product_name
FROM stg_online_retail
WHERE is_valid_sale = TRUE
  AND description IS NOT NULL
GROUP BY stock_code;
""")

cur.execute("""
DROP TABLE IF EXISTS dim_customers;

CREATE TABLE dim_customers AS
SELECT
    customer_id,
    MIN(invoice_date) AS first_purchase_at,
    MAX(invoice_date) AS last_purchase_at,
    COUNT(DISTINCT invoice_no) AS total_orders,
    SUM(revenue) AS total_revenue
FROM fact_invoice_items
WHERE customer_id IS NOT NULL
GROUP BY customer_id;
""")

cur.execute("""
DROP TABLE IF EXISTS mart_daily_sales;

CREATE TABLE mart_daily_sales AS
SELECT
    invoice_date::DATE AS sales_date,
    COUNT(DISTINCT invoice_no) AS total_orders,
    COUNT(*) AS total_items,
    SUM(quantity) AS total_quantity,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM fact_invoice_items
GROUP BY invoice_date::DATE
ORDER BY sales_date;
""")

cur.execute("""
DROP TABLE IF EXISTS mart_country_sales;

CREATE TABLE mart_country_sales AS
SELECT
    country,
    COUNT(DISTINCT invoice_no) AS total_orders,
    COUNT(*) AS total_items,
    SUM(quantity) AS total_quantity,
    ROUND(SUM(revenue), 2) AS total_revenue
FROM fact_invoice_items
GROUP BY country
ORDER BY total_revenue DESC;
""")


cur.execute("""
SELECT
    ROUND((SELECT SUM(revenue) FROM fact_invoice_items), 2) AS fact_revenue,
    ROUND((SELECT SUM(total_revenue) FROM mart_daily_sales), 2) AS daily_mart_revenue,
    ROUND((SELECT SUM(total_revenue) FROM mart_country_sales), 2) AS country_mart_revenue;
""")

fact_revenue, daily_mart_revenue, country_mart_revenue = cur.fetchone()

if fact_revenue != daily_mart_revenue or fact_revenue != country_mart_revenue:
    raise ValueError("Revenue validation failed")

conn.commit()

print("Revenue validation passed!")

print("Built stg_online_retail.")
print("Built fact_invoice_items.")
print("Built dim_products.")
print("Built dim_customers.")
print("Built mart_daily_sales.")
print("Built mart_country_sales.")

conn.close()