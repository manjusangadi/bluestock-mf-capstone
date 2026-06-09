import os
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import nbformat as nbf

# Ensure directories exist
charts_dir = "reports/charts"
os.makedirs(charts_dir, exist_ok=True)
db_path = "bluestock_mf.db"

# -------------------------------------------------------------------------
# Static Plotting & PNG Export Logic (runs locally to generate report assets)
# -------------------------------------------------------------------------
print("Connecting to database and extracting data for static chart exports...")
conn = sqlite3.connect(db_path)

# Set Seaborn style
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 10, 'axes.labelsize': 11, 'axes.titlesize': 12, 'figure.titlesize': 14})

# 1. NAV Trend Analysis
print("Exporting Chart 1: NAV Trends...")
df_nav = pd.read_sql_query("""
    SELECT n.amfi_code, f.scheme_name, f.category, n.date, n.nav 
    FROM fact_nav n
    JOIN dim_fund f ON n.amfi_code = f.amfi_code
    ORDER BY n.amfi_code, n.date;
""", conn)
df_nav["date"] = pd.to_datetime(df_nav["date"])

# Select 5 key schemes (one per category/style) for static plot readability
selected_amfi = [119551, 119598, 119120, 120844, 100025] # SBI Bluechip, SBI Small Cap, SBI Gilt, Kotak Liquid, HDFC Short Term
df_nav_subset = df_nav[df_nav["amfi_code"].isin(selected_amfi)]

plt.figure(figsize=(12, 6))
sns.lineplot(data=df_nav_subset, x="date", y="nav", hue="scheme_name", linewidth=1.5)
plt.title("Daily NAV Trends of Selected Mutual Fund Schemes (2022 - 2026)")
plt.xlabel("Date")
plt.ylabel("Net Asset Value (INR)")
# Highlight 2023 Bull Run
plt.axvspan(pd.to_datetime("2023-01-01"), pd.to_datetime("2023-12-31"), color='green', alpha=0.1, label='2023 Bull Run')
# Highlight 2024 Correction
plt.axvspan(pd.to_datetime("2024-03-01"), pd.to_datetime("2024-06-30"), color='red', alpha=0.1, label='2024 Corrections')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(f"{charts_dir}/01_nav_trends.png", dpi=150)
plt.close()

# 2. AUM Growth grouped bar chart
print("Exporting Chart 2: AUM Growth...")
df_aum = pd.read_sql_query("""
    SELECT date, fund_house, aum_lakh_crore, aum_crore, num_schemes 
    FROM fact_aum 
    ORDER BY date, fund_house;
""", conn)
df_aum["year"] = pd.to_datetime(df_aum["date"]).dt.year

plt.figure(figsize=(12, 6))
# Filter to major AMCs to avoid clutter
major_amcs = ["SBI Mutual Fund", "ICICI Prudential MF", "HDFC Mutual Fund", "Nippon India MF", "Kotak Mahindra MF"]
df_aum_filtered = df_aum[df_aum["fund_house"].isin(major_amcs)]
sns.barplot(data=df_aum_filtered, x="year", y="aum_lakh_crore", hue="fund_house", palette="Blues_r")
plt.title("AUM Growth by Major Fund Houses (2022 - 2025)")
plt.xlabel("Year")
plt.ylabel("AUM (Lakh Crore INR)")
# Highlight SBI Dominance (approx 12.5L Cr in 2025, check value)
# Let's add annotation above SBI 2025 bar
plt.annotate("SBI dominance at ~12.5L Cr", xy=(3.0, 12.0), xytext=(2.2, 13.0),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6))
plt.tight_layout()
plt.savefig(f"{charts_dir}/02_aum_growth.png", dpi=150)
plt.close()

# 3. SIP Inflow time-series
print("Exporting Chart 3: SIP Inflows...")
df_sip = pd.read_sql_query("SELECT month, sip_inflow_crore, active_sip_accounts_crore, new_sip_accounts_lakh, sip_aum_lakh_crore FROM monthly_sip_inflows ORDER BY month;", conn)
df_sip["month_dt"] = pd.to_datetime(df_sip["month"] + "-01")

plt.figure(figsize=(10, 5))
plt.plot(df_sip["month_dt"], df_sip["sip_inflow_crore"], marker='o', color='purple', linewidth=2)
plt.title("Monthly Systematic Investment Plan (SIP) Inflows (2022 - 2025)")
plt.xlabel("Month")
plt.ylabel("SIP Inflow (Crore INR)")
# Annotate December 2025 Peak
dec_2025 = df_sip[df_sip["month"] == "2025-12"].iloc[0]
plt.annotate(f"All-Time High:\n₹{dec_2025['sip_inflow_crore']:,} Cr\n(Dec 2025)", 
             xy=(dec_2025['month_dt'], dec_2025['sip_inflow_crore']), 
             xytext=(pd.to_datetime("2024-06-01"), 25000),
             arrowprops=dict(facecolor='purple', shrink=0.08, width=1.5, headwidth=8))
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.savefig(f"{charts_dir}/03_sip_inflows.png", dpi=150)
plt.close()

# 4. Category Inflow Heatmap
print("Exporting Chart 4: Category Inflow Heatmap...")
df_cat = pd.read_sql_query("SELECT month, category, net_inflow_crore FROM category_inflows ORDER BY month, category;", conn)
# Pivot table for heatmap: Y-axis = Category, X-axis = Month
df_cat_pivot = df_cat.pivot(index="category", columns="month", values="net_inflow_crore")

plt.figure(figsize=(14, 8))
sns.heatmap(df_cat_pivot, cmap="RdYlGn", center=0, annot=False, cbar_kws={'label': 'Net Inflow (Crore INR)'})
plt.title("Net Monthly Inflows by Asset Category (Heatmap)")
plt.xlabel("Month")
plt.ylabel("Mutual Fund Category")
plt.tight_layout()
plt.savefig(f"{charts_dir}/04_category_inflow_heatmap.png", dpi=150)
plt.close()

# 5. Investor Demographics - Age group pie chart
print("Exporting Chart 5: Investor Age Group Pie...")
df_tx = pd.read_sql_query("SELECT age_group, gender, amount_inr, state, city, city_tier, kyc_status FROM fact_transactions;", conn)
age_counts = df_tx["age_group"].value_counts().sort_index()

plt.figure(figsize=(7, 7))
plt.pie(age_counts, labels=age_counts.index, autopct='%1.1f%%', colors=sns.color_palette("pastel"), startangle=140)
plt.title("Investor Distribution by Age Group")
plt.tight_layout()
plt.savefig(f"{charts_dir}/05_age_distribution.png", dpi=150)
plt.close()

# 6. SIP Box Plot by Age Group
print("Exporting Chart 6: SIP Box Plot by Age Group...")
plt.figure(figsize=(9, 6))
# Filter out extreme outliers for visualization clarity
sns.boxplot(data=df_tx[df_tx["amount_inr"] < 25000], x="age_group", y="amount_inr", palette="Set3")
plt.title("SIP / Lumpsum Transaction Amount Distribution by Age Group")
plt.xlabel("Investor Age Group")
plt.ylabel("Transaction Amount (INR)")
plt.tight_layout()
plt.savefig(f"{charts_dir}/06_sip_box_by_age.png", dpi=150)
plt.close()

# 7. Gender Split
print("Exporting Chart 7: Gender Split...")
gender_counts = df_tx["gender"].value_counts()
plt.figure(figsize=(6, 6))
plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', colors=["skyblue", "lightpink"], startangle=90)
plt.title("Investor Split by Gender")
plt.tight_layout()
plt.savefig(f"{charts_dir}/07_gender_split.png", dpi=150)
plt.close()

# 8. Geographic Distribution - Horizontal Bar by State
print("Exporting Chart 8: State-wise Inflows...")
state_totals = df_tx.groupby("state")["amount_inr"].sum().reset_index()
state_totals["amount_crore"] = state_totals["amount_inr"] / 10000000.0
state_totals = state_totals.sort_values(by="amount_crore", ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(data=state_totals, x="amount_crore", y="state", palette="viridis")
plt.title("Total Transaction Inflows by State (in Crores INR)")
plt.xlabel("Total Amount (Crore INR)")
plt.ylabel("State")
plt.tight_layout()
plt.savefig(f"{charts_dir}/08_sip_by_state.png", dpi=150)
plt.close()

# 9. T30 vs B30 City Tier Pie
print("Exporting Chart 9: T30 vs B30 split...")
tier_counts = df_tx["city_tier"].value_counts()
plt.figure(figsize=(6, 6))
plt.pie(tier_counts, labels=tier_counts.index, autopct='%1.1f%%', colors=["coral", "aquamarine"], startangle=140)
plt.title("Transaction Allocation: T30 (Top 30) vs B30 (Beyond 30) Cities")
plt.tight_layout()
plt.savefig(f"{charts_dir}/09_city_tier_distribution.png", dpi=150)
plt.close()

# 10. Folio Count Growth
print("Exporting Chart 10: Folio Count Growth...")
df_folio = pd.read_sql_query("SELECT month, total_folios_crore, equity_folios_crore, debt_folios_crore FROM industry_folio_count ORDER BY month;", conn)
df_folio["month_dt"] = pd.to_datetime(df_folio["month"] + "-01")

plt.figure(figsize=(10, 5))
plt.plot(df_folio["month_dt"], df_folio["total_folios_crore"], marker='s', color='teal', linewidth=2, label="Total Folios")
plt.plot(df_folio["month_dt"], df_folio["equity_folios_crore"], marker='^', color='orange', linewidth=1.5, label="Equity Folios")
plt.plot(df_folio["month_dt"], df_folio["debt_folios_crore"], marker='v', color='blue', linewidth=1.5, label="Debt Folios")
plt.title("Mutual Fund Folio Count Growth (2022 - 2025)")
plt.xlabel("Month")
plt.ylabel("Folio Count (Crores)")
# Milestones
plt.axvline(pd.to_datetime("2022-01-01"), color="red", linestyle="--", alpha=0.5)
plt.text(pd.to_datetime("2022-02-01"), 15, "13.26 Cr Start", color="red")
plt.axvline(pd.to_datetime("2025-12-01"), color="red", linestyle="--", alpha=0.5)
plt.text(pd.to_datetime("2024-06-01"), 24, "26.12 Cr Peak", color="red")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig(f"{charts_dir}/10_folio_growth.png", dpi=150)
plt.close()

# 11. NAV Return Correlation Matrix
print("Exporting Chart 11: Daily Return Correlation...")
df_nav_daily = pd.read_sql_query("""
    SELECT date, amfi_code, nav FROM fact_nav;
""", conn)
df_nav_daily["date"] = pd.to_datetime(df_nav_daily["date"])

# Select 10 major fund codes
major_10_codes = [119551, 119552, 120503, 118632, 119092, 120841, 119598, 119599, 119120, 120844]
# SBI Bluechip Reg/Dir, ICICI Bluechip, Nippon Large Cap, Axis Bluechip, Kotak Bluechip, SBI Small Cap Reg/Dir, SBI Gilt, Kotak Liquid
df_nav_corr_subset = df_nav_daily[df_nav_daily["amfi_code"].isin(major_10_codes)]

# Pivot
df_pivot = df_nav_corr_subset.pivot(index="date", columns="amfi_code", values="nav")
# Calculate daily pct returns
df_returns = df_pivot.pct_change().dropna()
# Rename columns to scheme names
df_fund_names = pd.read_sql_query("SELECT amfi_code, scheme_name FROM dim_fund WHERE amfi_code IN (119551, 119552, 120503, 118632, 119092, 120841, 119598, 119599, 119120, 120844);", conn)
name_map = dict(zip(df_fund_names["amfi_code"], df_fund_names["scheme_name"].apply(lambda x: x.split(" - ")[0])))
df_returns.rename(columns=name_map, inplace=True)

# Compute Correlation
corr_matrix = df_returns.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", vmin=-1, vmax=1)
plt.title("Pairwise Correlation Matrix of Daily NAV Returns (10 Selected Funds)")
plt.tight_layout()
plt.savefig(f"{charts_dir}/11_return_correlation.png", dpi=150)
plt.close()

# 12. Sector Allocation Donut
print("Exporting Chart 12: Sector Allocation Donut...")
df_port = pd.read_sql_query("""
    SELECT p.amfi_code, f.scheme_name, p.sector, p.weight_pct 
    FROM portfolio_holdings p
    JOIN dim_fund f ON p.amfi_code = f.amfi_code
    WHERE f.category = 'Equity';
""", conn)
sector_totals = df_port.groupby("sector")["weight_pct"].mean().reset_index()
sector_totals = sector_totals.sort_values(by="weight_pct", ascending=False).head(8) # Top 8 sectors

# Remainder to 'Others'
total_top_weight = sector_totals["weight_pct"].sum()
others_weight = max(0.0, 100.0 - total_top_weight)
if others_weight > 0:
    sector_totals = pd.concat([sector_totals, pd.DataFrame([{"sector": "Others", "weight_pct": others_weight}])], ignore_index=True)

plt.figure(figsize=(8, 8))
plt.pie(sector_totals["weight_pct"], labels=sector_totals["sector"], autopct='%1.1f%%', 
        colors=sns.color_palette("Set2"), startangle=90, pctdistance=0.85)
# Draw center circle to make it a donut
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.title("Aggregated Sector Allocation Donut (Equity Funds)")
plt.tight_layout()
plt.savefig(f"{charts_dir}/12_sector_allocation_donut.png", dpi=150)
plt.close()

conn.close()
print("All static charts successfully generated and saved under reports/charts/!")
