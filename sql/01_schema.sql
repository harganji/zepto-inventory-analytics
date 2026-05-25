DROP TABLE IF EXISTS raw_zepto_inventory;

CREATE TABLE raw_zepto_inventory (
    category TEXT,
    name TEXT,
    mrp INTEGER,
    discount_percent NUMERIC,
    available_quantity INTEGER,
    discounted_selling_price INTEGER,
    weight_in_gms INTEGER,
    out_of_stock BOOLEAN,
    quantity INTEGER
);

DROP TABLE IF EXISTS clean_zepto_inventory;

CREATE TABLE clean_zepto_inventory (
    sku_id INTEGER PRIMARY KEY,
    category TEXT,
    product_name TEXT,
    mrp_rupees NUMERIC,
    selling_price_rupees NUMERIC,
    discount_amount_rupees NUMERIC,
    discount_percent NUMERIC,
    available_quantity INTEGER,
    weight_gms INTEGER,
    price_per_gram NUMERIC,
    inventory_value_rupees NUMERIC,
    out_of_stock BOOLEAN,
    stock_status TEXT,
    weight_band TEXT,
    quantity INTEGER
);
