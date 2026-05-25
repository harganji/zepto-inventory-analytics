# Zepto Inventory Analytics Portfolio Project

End-to-end data analyst portfolio project inspired by Amlan Mohanty's YouTube walkthrough: **Build SQL Data Analyst Portfolio Project Step-by-Step Guide with Real Zepto Data**.

The project defines business KPIs first, then cleans raw Zepto inventory data, performs SQL/Python analysis, and creates dashboard-ready extracts for Power BI or Tableau.

## Dashboard Preview

![Zepto inventory dashboard preview](outputs/dashboard_preview.jpg)

## Dashboard Platform

The included preview dashboard is built with Python Plotly and exported as an interactive HTML file. The project also exports Excel and CSV tables that are ready to connect in Power BI or Tableau.

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

## How To Run

Using Anaconda:

```powershell
conda env create -f environment.yml
conda activate zepto-inventory-analytics
python src\pipeline.py
jupyter notebook
```

The pipeline downloads the Zepto CSV automatically if `data/raw/zepto_inventory_raw.csv` is missing.

## Dashboard Files

After running the pipeline, use these in Power BI or Tableau:

- `data/dashboard/zepto_dashboard_tables.xlsx`
- `data/dashboard/fact_products.csv`
- `data/dashboard/category_summary.csv`
- `data/dashboard/top_discount_products.csv`
- `outputs/zepto_inventory_dashboard.html`
- `outputs/dashboard_preview.jpg`

Power BI/Tableau suggested pages:

1. Executive KPI Overview
2. Category Performance
3. Stock Availability
4. Pricing and Discount Analysis
5. Product Drilldown

## Repository Structure

```text
src/                  Python cleaning, KPI, SQL export and dashboard pipeline
sql/                  Schema, cleaning SQL, KPI analysis SQL
notebooks/            Jupyter notebooks for EDA and SQL review
data/dashboard/       Small dashboard summary exports committed to GitHub
dashboard_notes.md    Power BI DAX measures and Tableau calculated fields
```

## Dataset

Dataset: Zepto inventory product catalog dataset, originally published on Kaggle. The project stores source notes in `data/raw/SOURCE.md` and downloads the working CSV during pipeline execution.
