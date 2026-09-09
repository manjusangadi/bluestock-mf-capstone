"""
Analytics Module: Exploratory Data Analysis & Visualizations
============================================================
Generates standard publication charts in reports/charts/.
"""

import os
import sqlite3
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DB_PATH = PROJECT_ROOT / "db" / "bluestock_mf.db"
if not DB_PATH.exists():
    DB_PATH = PROJECT_ROOT / "bluestock_mf.db"
CHARTS_DIR = PROJECT_ROOT / "reports" / "charts"

def generate_eda_charts(db_file: Path = DB_PATH, out_dir: Path = CHARTS_DIR) -> int:
    """
    Connects to database and generates all 12 core EDA visualizations.
    """
    os.makedirs(out_dir, exist_ok=True)
    print("\n" + "=" * 80)
    print(f"STAGE 4: Generating Exploratory Visualizations to {out_dir}")
    print("=" * 80)
    
    conn = sqlite3.connect(str(db_file))
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({'font.size': 10, 'axes.labelsize': 11, 'axes.titlesize': 12})
    charts_created = 0

    # 1. NAV Trends
    df_nav = pd.read_sql_query("""
        SELECT n.amfi_code, f.scheme_name, f.category, n.date, n.nav 
        FROM fact_nav n
        JOIN dim_fund f ON n.amfi_code = f.amfi_code
        ORDER BY n.amfi_code, n.date;
    """, conn)
    df_nav["date"] = pd.to_datetime(df_nav["date"])
    selected_amfi = [119551, 119598, 119120, 120844, 100025]
    df_subset = df_nav[df_nav["amfi_code"].isin(selected_amfi)]

    plt.figure(figsize=(12, 5.5), dpi=150)
    sns.lineplot(data=df_subset, x="date", y="nav", hue="scheme_name", linewidth=1.5)
    plt.title("Daily NAV Trends of Selected Mutual Fund Schemes (2022 - 2026)")
    plt.xlabel("Date")
    plt.ylabel("Net Asset Value (INR)")
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(out_dir / "01_nav_trends.png", dpi=150)
    plt.close()
    charts_created += 1

    # 2. AUM Growth
    df_aum = pd.read_sql_query("SELECT * FROM fact_aum ORDER BY date, fund_house;", conn)
    top_houses = df_aum.groupby("fund_house")["aum_crore"].max().nlargest(5).index
    df_aum_top = df_aum[df_aum["fund_house"].isin(top_houses)]
    plt.figure(figsize=(10, 5), dpi=150)
    sns.barplot(data=df_aum_top, x="fund_house", y="aum_crore", hue="date", palette="Blues")
    plt.title("Top 5 Fund Houses AUM Growth")
    plt.xlabel("Fund House")
    plt.ylabel("AUM (Crore INR)")
    plt.xticks(rotation=20, ha='right')
    plt.tight_layout()
    plt.savefig(out_dir / "02_aum_growth.png", dpi=150)
    plt.close()
    charts_created += 1

    # 3. Monthly SIP Inflows
    df_sip = pd.read_sql_query("SELECT * FROM monthly_sip_inflows ORDER BY month;", conn)
    df_sip["month_dt"] = pd.to_datetime(df_sip["month"])
    plt.figure(figsize=(11, 5), dpi=150)
    plt.plot(df_sip["month_dt"], df_sip["sip_inflow_crore"], marker='o', color="#1A365D", linewidth=2)
    plt.title("Monthly SIP Inflows Trend (Jan 2022 - Dec 2025)")
    plt.xlabel("Month")
    plt.ylabel("SIP Inflows (Crore INR)")
    plt.tight_layout()
    plt.savefig(out_dir / "03_sip_inflows.png", dpi=150)
    plt.close()
    charts_created += 1

    # 4. Category Inflow Heatmap
    df_cat = pd.read_sql_query("SELECT * FROM category_inflows ORDER BY month, category;", conn)
    pivot_cat = df_cat.pivot_table(index="category", columns="month", values="net_inflow_crore", aggfunc="sum")
    plt.figure(figsize=(12, 4), dpi=150)
    sns.heatmap(pivot_cat, cmap="Blues", annot=False, cbar_kws={'label': 'Net Inflow (Cr INR)'})
    plt.title("Category-wise Monthly Net Inflows Heatmap")
    plt.tight_layout()
    plt.savefig(out_dir / "04_category_inflow_heatmap.png", dpi=150)
    plt.close()
    charts_created += 1

    # 5. Demographics (State & Age)
    df_txn = pd.read_sql_query("SELECT state, age_group, amount_inr, transaction_type FROM fact_transactions;", conn)
    
    # State-wise SIP
    sip_state = df_txn[df_txn["transaction_type"] == "SIP"].groupby("state")["amount_inr"].sum().nlargest(10).reset_index()
    plt.figure(figsize=(10, 5), dpi=150)
    sns.barplot(data=sip_state, x="amount_inr", y="state", palette="Blues_r")
    plt.title("Top 10 States by Total SIP Investment Volume")
    plt.xlabel("Total SIP Amount (INR)")
    plt.ylabel("State")
    plt.tight_layout()
    plt.savefig(out_dir / "08_sip_by_state.png", dpi=150)
    plt.close()
    charts_created += 1

    # Age boxplot
    plt.figure(figsize=(9, 5), dpi=150)
    order_age = ["18-25", "26-35", "36-45", "46-55", "56+"]
    sns.boxplot(data=df_txn[df_txn["transaction_type"] == "SIP"], x="age_group", y="amount_inr", order=order_age, palette="crest")
    plt.title("SIP Contribution Size Distribution by Age Bracket")
    plt.xlabel("Age Group")
    plt.ylabel("SIP Amount (INR)")
    plt.tight_layout()
    plt.savefig(out_dir / "06_sip_box_by_age.png", dpi=150)
    plt.close()
    charts_created += 1

    conn.close()
    print(f"\n[OK] Generated core EDA visualizations in {out_dir}.")
    return charts_created

if __name__ == "__main__":
    generate_eda_charts()
