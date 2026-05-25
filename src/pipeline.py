from pathlib import Path
import sqlite3

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "zepto_inventory_raw.csv"
PROCESSED_DIR = ROOT / "data" / "processed"
DASHBOARD_DIR = ROOT / "data" / "dashboard"
OUTPUTS_DIR = ROOT / "outputs"
DB_PATH = PROCESSED_DIR / "zepto_inventory.db"


def clean_products(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
        .str.replace(" ", "_", regex=False)
        .str.replace(r"(?<!^)(?=[A-Z])", "_", regex=True)
        .str.lower()
    )
    df = df.rename(columns={"discounted_selling_price": "selling_price", "weight_in_gms": "weight_gms"})
    df["category"] = df["category"].astype(str).str.strip().str.title()
    df["product_name"] = df["name"].astype(str).str.strip()
    df = df.drop(columns=["name"])

    numeric_cols = ["mrp", "discount_percent", "available_quantity", "selling_price", "weight_gms", "quantity"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["out_of_stock"] = df["out_of_stock"].astype(str).str.lower().isin(["true", "1", "yes"])
    df = df.dropna(subset=["category", "product_name", "mrp", "selling_price", "weight_gms"])
    df = df[(df["mrp"] > 0) & (df["selling_price"] > 0) & (df["weight_gms"] > 0)]

    df["mrp_rupees"] = (df["mrp"] / 100).round(2)
    df["selling_price_rupees"] = (df["selling_price"] / 100).round(2)
    df["discount_amount_rupees"] = (df["mrp_rupees"] - df["selling_price_rupees"]).round(2)
    df["price_per_gram"] = (df["selling_price_rupees"] / df["weight_gms"]).round(4)
    df["inventory_value_rupees"] = (df["selling_price_rupees"] * df["available_quantity"]).round(2)
    df["stock_status"] = np.where(df["out_of_stock"], "Out of Stock", "In Stock")
    df["weight_band"] = pd.cut(df["weight_gms"], bins=[0, 250, 1000, np.inf], labels=["Low Weight", "Medium Weight", "Bulk"]).astype(str)
    df["sku_id"] = np.arange(1, len(df) + 1)

    return df[[
        "sku_id", "category", "product_name", "mrp_rupees", "selling_price_rupees",
        "discount_amount_rupees", "discount_percent", "available_quantity", "weight_gms",
        "price_per_gram", "inventory_value_rupees", "out_of_stock", "stock_status",
        "weight_band", "quantity"
    ]]


def build_kpis(df: pd.DataFrame) -> pd.DataFrame:
    metrics = {
        "total_skus": len(df),
        "active_skus": int((~df["out_of_stock"]).sum()),
        "out_of_stock_skus": int(df["out_of_stock"].sum()),
        "out_of_stock_rate": round(df["out_of_stock"].mean(), 4),
        "total_available_units": int(df["available_quantity"].sum()),
        "estimated_inventory_value_rupees": round(df["inventory_value_rupees"].sum(), 2),
        "avg_mrp_rupees": round(df["mrp_rupees"].mean(), 2),
        "avg_selling_price_rupees": round(df["selling_price_rupees"].mean(), 2),
        "avg_discount_percent": round(df["discount_percent"].mean(), 2),
        "avg_price_per_gram": round(df["price_per_gram"].mean(), 4),
    }
    return pd.DataFrame([{"kpi": key, "value": value} for key, value in metrics.items()])


def build_category_summary(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby("category", as_index=False).agg(
        skus=("sku_id", "count"),
        active_skus=("out_of_stock", lambda x: int((~x).sum())),
        out_of_stock_skus=("out_of_stock", "sum"),
        total_units=("available_quantity", "sum"),
        inventory_value_rupees=("inventory_value_rupees", "sum"),
        avg_mrp_rupees=("mrp_rupees", "mean"),
        avg_selling_price_rupees=("selling_price_rupees", "mean"),
        avg_discount_percent=("discount_percent", "mean"),
        avg_price_per_gram=("price_per_gram", "mean"),
    ).sort_values("inventory_value_rupees", ascending=False)
    grouped["out_of_stock_rate"] = (grouped["out_of_stock_skus"] / grouped["skus"]).round(4)
    return grouped.round(2)


def build_dashboard_tables(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    return {
        "fact_products": df,
        "kpis": build_kpis(df),
        "category_summary": build_category_summary(df),
        "top_discount_products": df.sort_values(["discount_percent", "discount_amount_rupees"], ascending=False).head(25),
        "high_value_out_of_stock": df[df["out_of_stock"]].sort_values("mrp_rupees", ascending=False).head(25),
        "low_discount_expensive": df[(df["mrp_rupees"] > 500) & (df["discount_percent"] < 10)].sort_values("mrp_rupees", ascending=False),
        "best_value_products": df.sort_values("price_per_gram").head(25),
        "stock_summary": df.groupby("stock_status", as_index=False).agg(skus=("sku_id", "count")),
        "weight_summary": df.groupby("weight_band", as_index=False).agg(skus=("sku_id", "count"), inventory_value_rupees=("inventory_value_rupees", "sum")),
    }


def save_outputs(tables: dict[str, pd.DataFrame]) -> None:
    for directory in [PROCESSED_DIR, DASHBOARD_DIR, OUTPUTS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
    tables["fact_products"].to_csv(PROCESSED_DIR / "zepto_inventory_clean.csv", index=False)
    for name, table in tables.items():
        table.to_csv(DASHBOARD_DIR / f"{name}.csv", index=False)
    with pd.ExcelWriter(DASHBOARD_DIR / "zepto_dashboard_tables.xlsx", engine="openpyxl") as writer:
        for name, table in tables.items():
            table.to_excel(writer, sheet_name=name[:31], index=False)
    with sqlite3.connect(DB_PATH) as conn:
        for name, table in tables.items():
            table.to_sql(name, conn, if_exists="replace", index=False)


def make_dashboard(tables: dict[str, pd.DataFrame]) -> None:
    kpis = tables["kpis"].set_index("kpi")["value"]
    category = tables["category_summary"].head(10)
    stock = tables["stock_summary"]
    products = tables["top_discount_products"].head(10)
    fig = make_subplots(rows=3, cols=2, specs=[[{"type": "indicator"}, {"type": "indicator"}], [{"type": "bar"}, {"type": "pie"}], [{"type": "bar"}, {"type": "bar"}]], subplot_titles=("Total SKUs", "Estimated Inventory Value", "Top Categories by Inventory Value", "Stock Availability", "Top Discounted Products", "Average Discount by Category"))
    fig.add_trace(go.Indicator(mode="number", value=float(kpis["total_skus"])), row=1, col=1)
    fig.add_trace(go.Indicator(mode="number", value=float(kpis["estimated_inventory_value_rupees"]), number={"prefix": "Rs. ", "valueformat": ",.0f"}), row=1, col=2)
    fig.add_trace(go.Bar(x=category["inventory_value_rupees"], y=category["category"], orientation="h", marker_color="#2563eb"), row=2, col=1)
    fig.add_trace(go.Pie(labels=stock["stock_status"], values=stock["skus"], hole=0.45), row=2, col=2)
    fig.add_trace(go.Bar(x=products["discount_percent"], y=products["product_name"], orientation="h", marker_color="#16a34a"), row=3, col=1)
    fig.add_trace(go.Bar(x=category["avg_discount_percent"], y=category["category"], orientation="h", marker_color="#f97316"), row=3, col=2)
    fig.update_layout(title="Zepto Inventory Analytics Dashboard", height=1100, template="plotly_white", showlegend=False)
    fig.write_html(OUTPUTS_DIR / "zepto_inventory_dashboard.html", include_plotlyjs="cdn")


def main() -> None:
    raw = pd.read_csv(RAW_PATH)
    clean = clean_products(raw)
    tables = build_dashboard_tables(clean)
    save_outputs(tables)
    make_dashboard(tables)
    print(f"Pipeline complete. Clean rows: {len(clean):,}")


if __name__ == "__main__":
    main()
