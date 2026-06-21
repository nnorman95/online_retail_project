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
