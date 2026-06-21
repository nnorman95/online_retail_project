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
