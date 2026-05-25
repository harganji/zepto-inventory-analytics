-- Executive KPIs
SELECT 'total_skus' AS kpi, COUNT(*) AS value FROM clean_zepto_inventory
UNION ALL
SELECT 'active_skus', SUM(CASE WHEN out_of_stock = 0 THEN 1 ELSE 0 END) FROM clean_zepto_inventory
UNION ALL
SELECT 'out_of_stock_skus', SUM(CASE WHEN out_of_stock = 1 THEN 1 ELSE 0 END) FROM clean_zepto_inventory
UNION ALL
SELECT 'out_of_stock_rate', ROUND(AVG(CASE WHEN out_of_stock = 1 THEN 1.0 ELSE 0.0 END), 4) FROM clean_zepto_inventory
UNION ALL
SELECT 'total_available_units', SUM(available_quantity) FROM clean_zepto_inventory
UNION ALL
SELECT 'estimated_inventory_value_rupees', ROUND(SUM(inventory_value_rupees), 2) FROM clean_zepto_inventory
UNION ALL
SELECT 'avg_mrp_rupees', ROUND(AVG(mrp_rupees), 2) FROM clean_zepto_inventory
UNION ALL
SELECT 'avg_selling_price_rupees', ROUND(AVG(selling_price_rupees), 2) FROM clean_zepto_inventory
UNION ALL
SELECT 'avg_discount_percent', ROUND(AVG(discount_percent), 2) FROM clean_zepto_inventory;

-- Category performance
SELECT
    category,
    COUNT(*) AS skus,
    SUM(CASE WHEN out_of_stock = 0 THEN 1 ELSE 0 END) AS active_skus,
    SUM(CASE WHEN out_of_stock = 1 THEN 1 ELSE 0 END) AS out_of_stock_skus,
    ROUND(AVG(CASE WHEN out_of_stock = 1 THEN 1.0 ELSE 0.0 END), 4) AS out_of_stock_rate,
    SUM(available_quantity) AS total_units,
    ROUND(SUM(inventory_value_rupees), 2) AS inventory_value_rupees,
    ROUND(AVG(discount_percent), 2) AS avg_discount_percent
FROM clean_zepto_inventory
GROUP BY category
ORDER BY inventory_value_rupees DESC;

-- Top discounted products
SELECT
    category,
    product_name,
    mrp_rupees,
    selling_price_rupees,
    discount_percent,
    available_quantity,
    stock_status
FROM clean_zepto_inventory
ORDER BY discount_percent DESC, discount_amount_rupees DESC
LIMIT 10;

-- High MRP products currently out of stock
SELECT
    category,
    product_name,
    mrp_rupees,
    selling_price_rupees,
    discount_percent
FROM clean_zepto_inventory
WHERE out_of_stock = 1
ORDER BY mrp_rupees DESC
LIMIT 10;

-- Expensive products with low discounts
SELECT
    category,
    product_name,
    mrp_rupees,
    selling_price_rupees,
    discount_percent
FROM clean_zepto_inventory
WHERE mrp_rupees > 500
  AND discount_percent < 10
ORDER BY mrp_rupees DESC;

-- Best value products by price per gram
SELECT
    category,
    product_name,
    selling_price_rupees,
    weight_gms,
    price_per_gram
FROM clean_zepto_inventory
ORDER BY price_per_gram ASC
LIMIT 10;
