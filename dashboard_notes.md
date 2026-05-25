# Power BI / Tableau Dashboard Build Notes

Use `data/dashboard/zepto_dashboard_tables.xlsx` as the source workbook.

## Data Model

- Main table: `fact_products`
- Lookup/summary tables: `category_summary`, `stock_summary`, `weight_summary`
- KPI table: `kpis`

For a simple portfolio dashboard, one imported table is enough: use `fact_products` and create measures/calculated fields from it.

## Power BI Measures

```DAX
Total SKUs = COUNTROWS(fact_products)
Active SKUs = CALCULATE(COUNTROWS(fact_products), fact_products[out_of_stock] = FALSE())
Out of Stock SKUs = CALCULATE(COUNTROWS(fact_products), fact_products[out_of_stock] = TRUE())
Out of Stock Rate = DIVIDE([Out of Stock SKUs], [Total SKUs])
Total Available Units = SUM(fact_products[available_quantity])
Inventory Value = SUM(fact_products[inventory_value_rupees])
Average MRP = AVERAGE(fact_products[mrp_rupees])
Average Selling Price = AVERAGE(fact_products[selling_price_rupees])
Average Discount % = AVERAGE(fact_products[discount_percent])
Average Price Per Gram = AVERAGE(fact_products[price_per_gram])
```

## Recommended Dashboard Layout

Page 1: Executive Overview
- KPI cards: Total SKUs, Inventory Value, Out of Stock Rate, Average Discount %
- Bar chart: Inventory Value by Category
- Donut chart: Stock Status
- Table: Top Discounted Products

Page 2: Category Performance
- Matrix: Category, SKUs, Active SKUs, Out of Stock Rate, Inventory Value
- Bar chart: Average Discount % by Category
- Bar chart: Available Units by Category

Page 3: Product Drilldown
- Slicers: Category, Stock Status, Weight Band
- Scatter plot: MRP vs Selling Price, size by Available Quantity
- Table: Product Name, MRP, Selling Price, Discount %, Price per Gram

## Tableau Calculated Fields

```text
Out of Stock Rate = SUM(IIF([out_of_stock], 1, 0)) / COUNT([sku_id])
Inventory Value = SUM([inventory_value_rupees])
Average Discount % = AVG([discount_percent])
Average Price Per Gram = AVG([price_per_gram])
```
