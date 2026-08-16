import os
import pandas as pd
import numpy as np

# Ensure target directories exist
raw_dir = "data/raw"
processed_dir = "data/processed"
os.makedirs(processed_dir, exist_ok=True)

print("Starting reproducible data cleaning pipeline...")

# -------------------------------------------------------------
# 1. Clean 01_fund_master.csv
# -------------------------------------------------------------
print("Cleaning 01_fund_master.csv...")
df_master = pd.read_csv(os.path.join(raw_dir, "01_fund_master.csv"))
df_master = df_master.drop_duplicates()
for col in df_master.select_dtypes(include=['object', 'string']):
    df_master[col] = df_master[col].str.strip()
df_master = df_master.dropna(subset=['amfi_code'])
df_master.to_csv(os.path.join(processed_dir, "01_fund_master_clean.csv"), index=False)
print(f"  Saved 01_fund_master_clean.csv: {df_master.shape[0]} rows")

# -------------------------------------------------------------
# 2. Clean 02_nav_history.csv
# -------------------------------------------------------------
print("Cleaning 02_nav_history.csv...")
df_nav = pd.read_csv(os.path.join(raw_dir, "02_nav_history.csv"))
df_nav['date'] = pd.to_datetime(df_nav['date'], format='mixed')
df_nav = df_nav.sort_values(["amfi_code", "date"])
df_nav['nav'] = df_nav.groupby('amfi_code')['nav'].ffill()
df_nav = df_nav.drop_duplicates()
df_nav = df_nav[df_nav['nav'] > 0]
df_nav['date'] = df_nav['date'].dt.strftime('%Y-%m-%d')
df_nav.to_csv(os.path.join(processed_dir, "02_nav_history_clean.csv"), index=False)
print(f"  Saved 02_nav_history_clean.csv: {df_nav.shape[0]} rows")

# -------------------------------------------------------------
# 3. Clean 03_aum_by_fund_house.csv
# -------------------------------------------------------------
print("Cleaning 03_aum_by_fund_house.csv...")
df_aum = pd.read_csv(os.path.join(raw_dir, "03_aum_by_fund_house.csv"))
df_aum['aum_lakh_crore'] = pd.to_numeric(df_aum['aum_lakh_crore'], errors='coerce')
df_aum = df_aum[df_aum['aum_lakh_crore'] > 0]
df_aum = df_aum.drop_duplicates()
df_aum.to_csv(os.path.join(processed_dir, "03_aum_by_fund_house_clean.csv"), index=False)
print(f"  Saved 03_aum_by_fund_house_clean.csv: {df_aum.shape[0]} rows")

# -------------------------------------------------------------
# 4. Clean 04_monthly_sip_inflows.csv
# -------------------------------------------------------------
print("Cleaning 04_monthly_sip_inflows.csv...")
df_sip = pd.read_csv(os.path.join(raw_dir, "04_monthly_sip_inflows.csv"))
df_sip['sip_aum_lakh_crore'] = pd.to_numeric(df_sip['sip_aum_lakh_crore'], errors='coerce')
df_sip = df_sip[df_sip['sip_aum_lakh_crore'] > 0]
df_sip = df_sip.drop_duplicates()
df_sip.to_csv(os.path.join(processed_dir, "04_monthly_sip_inflows_clean.csv"), index=False)
print(f"  Saved 04_monthly_sip_inflows_clean.csv: {df_sip.shape[0]} rows")

# -------------------------------------------------------------
# 5. Clean 05_category_inflows.csv
# -------------------------------------------------------------
print("Cleaning 05_category_inflows.csv...")
df_cat = pd.read_csv(os.path.join(raw_dir, "05_category_inflows.csv"))
df_cat['category'] = df_cat['category'].astype(str).str.strip()
df_cat['net_inflow_crore'] = pd.to_numeric(df_cat['net_inflow_crore'], errors='coerce')
df_cat = df_cat.drop_duplicates()
# Write only the clean standardized net_inflow_crore column, removing the redundant inet_inflow_crore
df_cat.to_csv(os.path.join(processed_dir, "05_category_inflows_clean.csv"), index=False)
print(f"  Saved 05_category_inflows_clean.csv: {df_cat.shape[0]} rows")

# -------------------------------------------------------------
# 6. Clean 06_industry_folio_count.csv
# -------------------------------------------------------------
print("Cleaning 06_industry_folio_count.csv...")
df_folio = pd.read_csv(os.path.join(raw_dir, "06_industry_folio_count.csv"))
df_folio['month'] = pd.to_datetime(df_folio['month'], format='mixed')
folio_cols = ['total_folios_crore', 'equity_folios_crore', 'debt_folios_crore', 'hybrid_folios_crore', 'others_folios_crore']
for col in folio_cols:
    df_folio[col] = pd.to_numeric(df_folio[col], errors='coerce')
df_folio = df_folio.dropna()
df_folio = df_folio.drop_duplicates()
for col in folio_cols:
    df_folio = df_folio[df_folio[col] >= 0]
df_folio['month'] = df_folio['month'].dt.strftime('%Y-%m-%d')
df_folio.to_csv(os.path.join(processed_dir, "06_industry_folio_count_clean.csv"), index=False)
print(f"  Saved 06_industry_folio_count_clean.csv: {df_folio.shape[0]} rows")

# -------------------------------------------------------------
# 7. Clean 07_scheme_performance.csv
# -------------------------------------------------------------
print("Cleaning 07_scheme_performance.csv...")
df_per = pd.read_csv(os.path.join(raw_dir, "07_scheme_performance.csv"))
return_cols = ['return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct']
for col in return_cols:
    df_per[col] = pd.to_numeric(df_per[col], errors='coerce')
df_per = df_per.dropna(subset=return_cols)
# Flag anomalies as 1 or 0 (int) to match SQLite INTEGER column
df_per['anomaly_flag'] = ((df_per['return_1yr_pct'] > 100) | (df_per['return_1yr_pct'] < -50)).astype(int)
df_per = df_per[(df_per['expense_ratio_pct'] >= 0.1) & (df_per['expense_ratio_pct'] <= 2.5)]
df_per = df_per.drop_duplicates()
df_per.to_csv(os.path.join(processed_dir, "07_scheme_performance_clean.csv"), index=False)
print(f"  Saved 07_scheme_performance_clean.csv: {df_per.shape[0]} rows")

# -------------------------------------------------------------
# 8. Clean 08_investor_transactions.csv
# -------------------------------------------------------------
print("Cleaning 08_investor_transactions.csv...")
df_tx = pd.read_csv(os.path.join(raw_dir, "08_investor_transactions.csv"))
df_tx['transaction_date'] = pd.to_datetime(df_tx['transaction_date'], format='mixed')
df_tx['transaction_type'] = df_tx['transaction_type'].astype(str).str.strip().str.lower()
type_map = {'sip': 'SIP', 'lumpsum': 'Lumpsum', 'redemption': 'Redemption'}
df_tx['transaction_type'] = df_tx['transaction_type'].map(type_map).fillna(df_tx['transaction_type'])
df_tx = df_tx[df_tx["amount_inr"] > 0]
df_tx['kyc_status'] = df_tx['kyc_status'].astype(str).str.strip().str.title()
valid_kyc = ['Verified', 'Pending', 'Failed']
df_tx = df_tx[df_tx['kyc_status'].isin(valid_kyc)]
df_tx['transaction_date'] = df_tx['transaction_date'].dt.strftime('%Y-%m-%d')
df_tx = df_tx.drop_duplicates()
df_tx = df_tx.dropna()
df_tx.to_csv(os.path.join(processed_dir, "08_investor_transactions_clean.csv"), index=False)
print(f"  Saved 08_investor_transactions_clean.csv: {df_tx.shape[0]} rows")

# -------------------------------------------------------------
# 9. Clean 09_portfolio_holdings.csv
# -------------------------------------------------------------
print("Cleaning 09_portfolio_holdings.csv...")
df_port = pd.read_csv(os.path.join(raw_dir, "09_portfolio_holdings.csv"))
df_port['portfolio_date'] = pd.to_datetime(df_port['portfolio_date'], format='mixed')
df_port = df_port.drop_duplicates()
text_cols = ['stock_symbol', 'stock_name', 'sector']
for col in text_cols:
    df_port[col] = df_port[col].astype(str).str.strip()
df_port = df_port[(df_port['weight_pct'] >= 0) & (df_port['weight_pct'] <= 100)]
df_port = df_port[df_port['market_value_cr'] >= 0]
df_port = df_port[df_port['current_price_inr'] > 0]
df_port = df_port.dropna()
df_port['portfolio_date'] = df_port['portfolio_date'].dt.strftime('%Y-%m-%d')
df_port.to_csv(os.path.join(processed_dir, "09_portfolio_holdings_clean.csv"), index=False)
print(f"  Saved 09_portfolio_holdings_clean.csv: {df_port.shape[0]} rows")

# -------------------------------------------------------------
# 10. Clean 10_benchmark_indices.csv
# -------------------------------------------------------------
print("Cleaning 10_benchmark_indices.csv...")
df_bench = pd.read_csv(os.path.join(raw_dir, "10_benchmark_indices.csv"))
df_bench['date'] = pd.to_datetime(df_bench['date'], format='mixed')
df_bench = df_bench.sort_values(['index_name', 'date'])
df_bench = df_bench.drop_duplicates()
df_bench['index_name'] = df_bench['index_name'].astype(str).str.strip().str.upper()
df_bench = df_bench[df_bench['close_value'] > 0]
df_bench = df_bench.dropna()
df_bench['date'] = df_bench['date'].dt.strftime('%Y-%m-%d')
df_bench.to_csv(os.path.join(processed_dir, "10_benchmark_indices_clean.csv"), index=False)
print(f"  Saved 10_benchmark_indices_clean.csv: {df_bench.shape[0]} rows")

print("All datasets successfully cleaned and saved!")
