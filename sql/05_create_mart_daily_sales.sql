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
