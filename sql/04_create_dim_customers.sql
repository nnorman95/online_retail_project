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
