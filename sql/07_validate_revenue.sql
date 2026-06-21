SELECT
    ROUND((SELECT SUM(revenue) FROM fact_invoice_items), 2) AS fact_revenue,
    ROUND((SELECT SUM(total_revenue) FROM mart_daily_sales), 2) AS daily_mart_revenue,
    ROUND((SELECT SUM(total_revenue) FROM mart_country_sales), 2) AS country_mart_revenue;
    