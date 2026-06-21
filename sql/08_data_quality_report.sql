SELECT
    COUNT(*) AS total_rows,
    COUNT(*) FILTER (WHERE description IS NULL) AS null_descriptions,
    COUNT(*) FILTER (WHERE customer_id IS NULL) AS null_customer_ids,
    COUNT(*) FILTER (WHERE quantity <= 0) AS non_positive_quantity_rows,
    COUNT(*) FILTER (WHERE unit_price <= 0) AS non_positive_unit_price_rows,
    COUNT(*) FILTER (WHERE invoice_no LIKE 'C%') AS cancelled_rows,
    COUNT(*) FILTER (WHERE is_valid_sale = TRUE) AS valid_sale_rows,
    COUNT(*) FILTER (WHERE is_valid_sale = FALSE) AS invalid_sale_rows,
    MIN(invoice_date) AS first_invoice_at,
    MAX(invoice_date) AS last_invoice_at,
    COUNT(DISTINCT country) AS country_count,
    ROUND(SUM(revenue) FILTER (WHERE is_valid_sale = TRUE), 2) AS valid_revenue
FROM stg_online_retail;
