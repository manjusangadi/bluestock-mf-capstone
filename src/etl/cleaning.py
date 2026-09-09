"""
ETL Module: Data Cleaning & Validation
======================================
Cleans and standardizes raw CSVs into data/processed/.
"""

import os
from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

def clean_all_data(raw_path: Path = RAW_DIR, out_path: Path = PROCESSED_DIR) -> dict:
    """
    Executes end-to-end data cleaning across all 10 mutual fund datasets.
    """
    os.makedirs(out_path, exist_ok=True)
    print("\n" + "=" * 80)
    print("STAGE 2: Cleaning & Validating All Raw Datasets")
    print("=" * 80)
    cleaned_dfs = {}

    # 1. 01_fund_master.csv
    f1 = raw_path / "01_fund_master.csv"
    if f1.exists():
        df_master = pd.read_csv(f1).drop_duplicates()
        for col in df_master.select_dtypes(include=['object', 'string']):
            df_master[col] = df_master[col].str.strip()
        df_master = df_master.dropna(subset=['amfi_code'])
        df_master.to_csv(out_path / "01_fund_master_clean.csv", index=False)
        cleaned_dfs["fund_master"] = df_master
        print(f"  [OK] Cleaned 01_fund_master_clean.csv ({len(df_master)} rows)")

    # 2. 02_nav_history.csv
    f2 = raw_path / "02_nav_history.csv"
    if f2.exists():
        df_nav = pd.read_csv(f2)
        df_nav['date'] = pd.to_datetime(df_nav['date'], format='mixed')
        df_nav = df_nav.sort_values(["amfi_code", "date"])
        df_nav['nav'] = df_nav.groupby('amfi_code')['nav'].ffill()
        df_nav = df_nav.drop_duplicates()
        df_nav = df_nav[df_nav['nav'] > 0]
        df_nav['date'] = df_nav['date'].dt.strftime('%Y-%m-%d')
        df_nav.to_csv(out_path / "02_nav_history_clean.csv", index=False)
        cleaned_dfs["nav_history"] = df_nav
        print(f"  [OK] Cleaned 02_nav_history_clean.csv ({len(df_nav)} rows)")

    # 3. 03_aum_by_fund_house.csv
    f3 = raw_path / "03_aum_by_fund_house.csv"
    if f3.exists():
        df_aum = pd.read_csv(f3)
        df_aum['aum_lakh_crore'] = pd.to_numeric(df_aum['aum_lakh_crore'], errors='coerce')
        df_aum = df_aum[df_aum['aum_lakh_crore'] > 0].drop_duplicates()
        df_aum.to_csv(out_path / "03_aum_by_fund_house_clean.csv", index=False)
        cleaned_dfs["aum"] = df_aum
        print(f"  [OK] Cleaned 03_aum_by_fund_house_clean.csv ({len(df_aum)} rows)")

    # 4. 04_monthly_sip_inflows.csv
    f4 = raw_path / "04_monthly_sip_inflows.csv"
    if f4.exists():
        df_sip = pd.read_csv(f4)
        df_sip['sip_aum_lakh_crore'] = pd.to_numeric(df_sip['sip_aum_lakh_crore'], errors='coerce')
        df_sip = df_sip[df_sip['sip_aum_lakh_crore'] > 0].drop_duplicates()
        df_sip.to_csv(out_path / "04_monthly_sip_inflows_clean.csv", index=False)
        cleaned_dfs["sip_inflows"] = df_sip
        print(f"  [OK] Cleaned 04_monthly_sip_inflows_clean.csv ({len(df_sip)} rows)")

    # 5. 05_category_inflows.csv
    f5 = raw_path / "05_category_inflows.csv"
    if f5.exists():
        df_cat = pd.read_csv(f5)
        df_cat['category'] = df_cat['category'].astype(str).str.strip()
        df_cat['net_inflow_crore'] = pd.to_numeric(df_cat['net_inflow_crore'], errors='coerce')
        df_cat = df_cat.drop_duplicates()
        df_cat.to_csv(out_path / "05_category_inflows_clean.csv", index=False)
        cleaned_dfs["category_inflows"] = df_cat
        print(f"  [OK] Cleaned 05_category_inflows_clean.csv ({len(df_cat)} rows)")

    # 6. 06_industry_folio_count.csv
    f6 = raw_path / "06_industry_folio_count.csv"
    if f6.exists():
        df_folio = pd.read_csv(f6)
        df_folio['month'] = pd.to_datetime(df_folio['month'], format='mixed')
        folio_cols = ['total_folios_crore', 'equity_folios_crore', 'debt_folios_crore', 'hybrid_folios_crore', 'others_folios_crore']
        for col in folio_cols:
            df_folio[col] = pd.to_numeric(df_folio[col], errors='coerce')
        df_folio = df_folio.dropna().drop_duplicates()
        for col in folio_cols:
            df_folio = df_folio[df_folio[col] >= 0]
        df_folio['month'] = df_folio['month'].dt.strftime('%Y-%m-%d')
        df_folio.to_csv(out_path / "06_industry_folio_count_clean.csv", index=False)
        cleaned_dfs["folio_count"] = df_folio
        print(f"  [OK] Cleaned 06_industry_folio_count_clean.csv ({len(df_folio)} rows)")

    # 7. 07_scheme_performance.csv
    f7 = raw_path / "07_scheme_performance.csv"
    if f7.exists():
        df_per = pd.read_csv(f7)
        return_cols = ['return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct']
        for col in return_cols:
            df_per[col] = pd.to_numeric(df_per[col], errors='coerce')
        df_per = df_per.dropna(subset=return_cols)
        df_per['anomaly_flag'] = ((df_per['return_1yr_pct'] > 100) | (df_per['return_1yr_pct'] < -50)).astype(int)
        df_per = df_per[(df_per['expense_ratio_pct'] >= 0.1) & (df_per['expense_ratio_pct'] <= 2.5)]
        df_per = df_per.drop_duplicates()
        df_per.to_csv(out_path / "07_scheme_performance_clean.csv", index=False)
        cleaned_dfs["performance"] = df_per
        print(f"  [OK] Cleaned 07_scheme_performance_clean.csv ({len(df_per)} rows)")

    # 8. 08_investor_transactions.csv
    f8 = raw_path / "08_investor_transactions.csv"
    if f8.exists():
        df_txn = pd.read_csv(f8)
        df_txn['transaction_date'] = pd.to_datetime(df_txn['transaction_date'], format='mixed')
        df_txn = df_txn[df_txn['amount_inr'] > 0]
        valid_types = ['SIP', 'Lumpsum', 'Redemption']
        df_txn = df_txn[df_txn['transaction_type'].isin(valid_types)]
        valid_kyc = ['Verified', 'Pending']
        df_txn = df_txn[df_txn['kyc_status'].isin(valid_kyc)]
        df_txn = df_txn.drop_duplicates()
        df_txn['transaction_date'] = df_txn['transaction_date'].dt.strftime('%Y-%m-%d')
        df_txn.to_csv(out_path / "08_investor_transactions_clean.csv", index=False)
        cleaned_dfs["transactions"] = df_txn
        print(f"  [OK] Cleaned 08_investor_transactions_clean.csv ({len(df_txn)} rows)")

    # 9. 09_portfolio_holdings.csv
    f9 = raw_path / "09_portfolio_holdings.csv"
    if f9.exists():
        df_port = pd.read_csv(f9)
        df_port['portfolio_date'] = pd.to_datetime(df_port['portfolio_date'], format='mixed')
        df_port['weight_pct'] = pd.to_numeric(df_port['weight_pct'], errors='coerce')
        df_port = df_port[df_port['weight_pct'] > 0]
        df_port = df_port.drop_duplicates()
        df_port['portfolio_date'] = df_port['portfolio_date'].dt.strftime('%Y-%m-%d')
        df_port.to_csv(out_path / "09_portfolio_holdings_clean.csv", index=False)
        cleaned_dfs["holdings"] = df_port
        print(f"  [OK] Cleaned 09_portfolio_holdings_clean.csv ({len(df_port)} rows)")

    # 10. 10_benchmark_indices.csv
    f10 = raw_path / "10_benchmark_indices.csv"
    if f10.exists():
        df_bench = pd.read_csv(f10)
        df_bench['date'] = pd.to_datetime(df_bench['date'], format='mixed')
        if 'index_name' in df_bench.columns and 'close_value' in df_bench.columns:
            df_bench['close_value'] = pd.to_numeric(df_bench['close_value'], errors='coerce')
            df_bench = df_bench.dropna(subset=['close_value']).drop_duplicates()
        else:
            index_cols = [c for c in df_bench.columns if c != 'date']
            df_bench[index_cols] = df_bench[index_cols].ffill()
            df_bench = df_bench.drop_duplicates()
        df_bench['date'] = df_bench['date'].dt.strftime('%Y-%m-%d')
        df_bench.to_csv(out_path / "10_benchmark_indices_clean.csv", index=False)
        cleaned_dfs["benchmarks"] = df_bench
        print(f"  [OK] Cleaned 10_benchmark_indices_clean.csv ({len(df_bench)} rows)")

    print(f"\n[OK] Data cleaning pipeline completed. All cleaned CSVs saved in {out_path}.")
    return cleaned_dfs

if __name__ == "__main__":
    clean_all_data()
