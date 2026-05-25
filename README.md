# Zepto Inventory Analytics Portfolio Project

End-to-end data analyst portfolio project inspired by Amlan Mohanty's YouTube walkthrough: **Build SQL Data Analyst Portfolio Project Step-by-Step Guide with Real Zepto Data**.

The project defines business KPIs first, then cleans raw Zepto inventory data, performs SQL/Python analysis, and creates dashboard-ready extracts for Power BI or Tableau.

## Business Questions

- Which categories carry the highest product range and inventory value?
- What share of products are out of stock?
- Which products and categories offer the strongest discounts?
- Where is inventory value concentrated?
- Which products look expensive with low discounts?
- Which products give the best value by price per gram?

## KPIs

- Total SKUs
- Active SKUs
- Out-of-stock SKUs
- Out-of-stock rate
- Total available units
- Estimated inventory value
- Average MRP
- Average selling price
- Average discount percent
- Average price per gram

## Project Structure

```text
zepto-inventory-analytics/
  data/
    raw/zepto_inventory_raw.csv
    processed/
    dashboard/
  notebooks/
    01_cleaning_kpis_eda.ipynb
    02_sql_analysis_dashboard_prep.ipynb
  outputs/
  sql/
    01_schema.sql
    02_cleaning.sql
    03_kpi_analysis.sql
  src/
    pipeline.py
    make_notebooks.py
```

## How To Run

Using Anaconda:

```powershell
cd "C:\Users\saiha\OneDrive\Documents\New project\zepto-inventory-analytics"
C:\Users\saiha\anaconda3\python.exe src\pipeline.py
C:\Users\saiha\anaconda3\python.exe src\make_notebooks.py
C:\Users\saiha\anaconda3\Scripts\jupyter.exe notebook
```

Or create a dedicated environment:

```powershell
conda env create -f environment.yml
conda activate zepto-inventory-analytics
python src\pipeline.py
python src\make_notebooks.py
jupyter notebook
```

## Dashboard Files

After running the pipeline, use these in Power BI or Tableau:

- `data/dashboard/zepto_dashboard_tables.xlsx`
- `data/dashboard/fact_products.csv`
- `data/dashboard/category_summary.csv`
- `data/dashboard/top_discount_products.csv`
- `outputs/zepto_inventory_dashboard.html`

Power BI/Tableau suggested pages:

1. Executive KPI Overview
2. Category Performance
3. Stock Availability
4. Pricing and Discount Analysis
5. Product Drilldown

## Dataset

Dataset: Zepto inventory product catalog dataset, originally published on Kaggle. A public copy of the CSV is included so the project can run offline.
