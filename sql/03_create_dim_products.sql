DROP TABLE IF EXISTS dim_products;

CREATE TABLE dim_products AS
SELECT
    stock_code,
    MAX(description) AS product_name
FROM stg_online_retail
WHERE is_valid_sale = TRUE
  AND description IS NOT NULL
GROUP BY stock_code;
