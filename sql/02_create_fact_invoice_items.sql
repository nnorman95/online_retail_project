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
