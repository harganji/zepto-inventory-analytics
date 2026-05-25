-- Pricing columns in the raw dataset are stored in paise, so divide by 100.
INSERT INTO clean_zepto_inventory (
    sku_id,
    category,
    product_name,
    mrp_rupees,
    selling_price_rupees,
    discount_amount_rupees,
    discount_percent,
    available_quantity,
    weight_gms,
    price_per_gram,
    inventory_value_rupees,
    out_of_stock,
    stock_status,
    weight_band,
    quantity
)
SELECT
    ROW_NUMBER() OVER () AS sku_id,
    TRIM(category) AS category,
    TRIM(name) AS product_name,
    ROUND(mrp / 100.0, 2) AS mrp_rupees,
    ROUND(discounted_selling_price / 100.0, 2) AS selling_price_rupees,
    ROUND((mrp - discounted_selling_price) / 100.0, 2) AS discount_amount_rupees,
    discount_percent,
    available_quantity,
    weight_in_gms,
    ROUND((discounted_selling_price / 100.0) / NULLIF(weight_in_gms, 0), 4) AS price_per_gram,
    ROUND((discounted_selling_price / 100.0) * available_quantity, 2) AS inventory_value_rupees,
    out_of_stock,
    CASE WHEN out_of_stock THEN 'Out of Stock' ELSE 'In Stock' END AS stock_status,
    CASE
        WHEN weight_in_gms <= 250 THEN 'Low Weight'
        WHEN weight_in_gms <= 1000 THEN 'Medium Weight'
        ELSE 'Bulk'
    END AS weight_band,
    quantity
FROM raw_zepto_inventory
WHERE mrp > 0
  AND discounted_selling_price > 0
  AND weight_in_gms > 0
  AND category IS NOT NULL
  AND name IS NOT NULL;
