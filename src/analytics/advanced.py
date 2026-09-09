"""
Analytics Module: Advanced Risk Analytics & Investor Behavior
=============================================================
Computes VaR/CVaR, Rolling 90-Day Sharpe, Cohort Analysis, SIP Churn, and HHI.
"""

import os
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"
CHARTS_DIR = REPORTS_DIR / "charts"

NAV_FILE = DATA_DIR / "02_nav_history_clean.csv"
MASTER_FILE = DATA_DIR / "01_fund_master_clean.csv"
TX_FILE = DATA_DIR / "08_investor_transactions_clean.csv"
HOLDINGS_FILE = DATA_DIR / "09_portfolio_holdings_clean.csv"

def compute_var_cvar(nav_path: Path = NAV_FILE, master_path: Path = MASTER_FILE, out_dir: Path = REPORTS_DIR) -> pd.DataFrame:
    """Computes 1-Day 95% Historical VaR and CVaR across all 40 schemes."""
    nav_df = pd.read_csv(nav_path)
    nav_df["date"] = pd.to_datetime(nav_df["date"])
    nav_df = nav_df.sort_values(["amfi_code", "date"]).reset_index(drop=True)
    nav_df["daily_return"] = nav_df.groupby("amfi_code")["nav"].pct_change()
    
    master_df = pd.read_csv(master_path)[["amfi_code", "scheme_name", "category", "sub_category", "risk_category"]]
    
    records = []
    for amfi_code, group in nav_df.groupby("amfi_code"):
        rets = group["daily_return"].dropna()
        if len(rets) < 30:
            continue
        var_95_daily = np.percentile(rets, 5)
        tail = rets[rets <= var_95_daily]
        cvar_95_daily = tail.mean() if len(tail) > 0 else var_95_daily
        
        records.append({
            "amfi_code": amfi_code,
            "var_95_daily_pct": round(var_95_daily * 100, 4),
            "cvar_95_daily_pct": round(cvar_95_daily * 100, 4),
            "var_95_ann_pct": round(var_95_daily * np.sqrt(252) * 100, 2),
            "cvar_95_ann_pct": round(cvar_95_daily * np.sqrt(252) * 100, 2),
            "std_daily_pct": round(rets.std() * 100, 4),
            "observation_days": len(rets)
        })
    df_var = pd.DataFrame(records).merge(master_df, on="amfi_code", how="left")
    df_var = df_var.sort_values("var_95_daily_pct", ascending=True).reset_index(drop=True)
    df_var.to_csv(out_dir / "var_cvar_report.csv", index=False)
    return df_var

def compute_rolling_sharpe(nav_path: Path = NAV_FILE, out_dir: Path = CHARTS_DIR) -> str:
    """Generates 90-day rolling Sharpe ratio chart for 5 key funds."""
    nav_df = pd.read_csv(nav_path)
    nav_df["date"] = pd.to_datetime(nav_df["date"])
    nav_df = nav_df.sort_values(["amfi_code", "date"]).reset_index(drop=True)
    nav_df["daily_return"] = nav_df.groupby("amfi_code")["nav"].pct_change()
    
    key_funds = [148567, 100033, 120843, 120504, 120505]
    labels = {
        148567: "Mirae Asset Large Cap Fund",
        100033: "HDFC Mid-Cap Opportunities Fund",
        120843: "Kotak Flexicap Fund",
        120504: "ICICI Pru Bluechip Fund",
        120505: "ICICI Pru Midcap Fund"
    }
    palette = {
        148567: "#1A365D",
        100033: "#DD6B20",
        120843: "#3182CE",
        120504: "#38A169",
        120505: "#805AD5"
    }
    sub = nav_df[nav_df["amfi_code"].isin(key_funds)].pivot(index="date", columns="amfi_code", values="daily_return")
    rolling_sharpe = (sub.rolling(90).mean() / sub.rolling(90).std()) * np.sqrt(252)
    rolling_sharpe = rolling_sharpe.dropna(how="all")
    
    fig, ax = plt.subplots(figsize=(12, 5.5), dpi=150)
    for code in key_funds:
        if code in rolling_sharpe.columns:
            ax.plot(rolling_sharpe.index, rolling_sharpe[code], label=labels.get(code, str(code)), color=palette.get(code, "#333"), linewidth=2.0)
    ax.axhline(0, color="#E53E3E", linestyle="--", linewidth=1.5, alpha=0.7, label="Neutral Threshold (Sharpe = 0)")
    ax.axhline(1.0, color="#718096", linestyle=":", linewidth=1.2, alpha=0.6, label="Benchmark Level (Sharpe = 1.0)")
    ax.set_title("90-Day Rolling Annualized Sharpe Ratio Comparison (2022–2026)", fontsize=13, fontweight="bold", color="#1A365D")
    ax.set_xlabel("Date", fontweight="bold")
    ax.set_ylabel("Annualized Sharpe", fontweight="bold")
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.xticks(rotation=30, ha="right")
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(loc="upper left")
    plt.tight_layout()
    
    chart_path = out_dir / "rolling_sharpe_chart.png"
    fig.savefig(chart_path, dpi=150)
    plt.close()
    return str(chart_path)

def compute_cohort_analysis(tx_path: Path = TX_FILE, master_path: Path = MASTER_FILE, out_dir: Path = REPORTS_DIR) -> pd.DataFrame:
    """Performs investor cohort analysis by entry year."""
    tx_df = pd.read_csv(tx_path)
    tx_df["transaction_date"] = pd.to_datetime(tx_df["transaction_date"])
    master_df = pd.read_csv(master_path)[["amfi_code", "scheme_name"]]
    tx_df = tx_df.merge(master_df, on="amfi_code", how="left")
    
    first_tx = tx_df.groupby("investor_id")["transaction_date"].min().dt.year.rename("cohort_year")
    tx_df = tx_df.merge(first_tx, on="investor_id", how="left")
    
    cohorts = []
    for year, group in tx_df.groupby("cohort_year"):
        sip_group = group[group["transaction_type"] == "SIP"]
        top_scheme = group["scheme_name"].value_counts().index[0]
        cohorts.append({
            "cohort_year": int(year),
            "total_investors": group["investor_id"].nunique(),
            "total_invested_inr": group["amount_inr"].sum(),
            "avg_transaction_inr": round(group["amount_inr"].mean(), 2),
            "total_sip_inr": sip_group["amount_inr"].sum(),
            "avg_sip_inr": round(sip_group["amount_inr"].mean(), 2) if len(sip_group) > 0 else 0,
            "top_preferred_scheme": top_scheme
        })
    df_cohort = pd.DataFrame(cohorts).sort_values("cohort_year").reset_index(drop=True)
    df_cohort.to_csv(out_dir / "cohort_analysis.csv", index=False)
    return df_cohort

def compute_sip_continuity(tx_path: Path = TX_FILE, out_dir: Path = REPORTS_DIR) -> pd.DataFrame:
    """Calculates cadence gaps and churn risk flags for regular SIP investors (6+ txns)."""
    tx_df = pd.read_csv(tx_path)
    tx_df["transaction_date"] = pd.to_datetime(tx_df["transaction_date"])
    sip_df = tx_df[tx_df["transaction_type"] == "SIP"].sort_values(["investor_id", "transaction_date"])
    
    sip_counts = sip_df.groupby("investor_id").size()
    eligible = sip_counts[sip_counts >= 6].index
    sub = sip_df[sip_df["investor_id"].isin(eligible)].copy()
    sub["gap_days"] = sub.groupby("investor_id")["transaction_date"].diff().dt.days
    
    continuity = sub.groupby("investor_id").agg(
        sip_count=("transaction_date", "count"),
        avg_gap_days=("gap_days", "mean"),
        max_gap_days=("gap_days", "max"),
        total_sip_amount=("amount_inr", "sum")
    ).reset_index()
    continuity["avg_gap_days"] = continuity["avg_gap_days"].round(2)
    continuity["is_at_risk"] = continuity["avg_gap_days"] > 35
    continuity.to_csv(out_dir / "sip_continuity.csv", index=False)
    return continuity

def compute_sector_hhi(holdings_path: Path = HOLDINGS_FILE, master_path: Path = MASTER_FILE, out_dir: Path = REPORTS_DIR) -> pd.DataFrame:
    """Computes Herfindahl-Hirschman Index across sector allocations for equity funds."""
    holdings_df = pd.read_csv(holdings_path)
    master_df = pd.read_csv(master_path)[["amfi_code", "scheme_name", "category", "sub_category"]]
    holdings_df = holdings_df.merge(master_df, on="amfi_code", how="left")
    equity_holdings = holdings_df[holdings_df["category"] == "Equity"]
    
    sector_alloc = equity_holdings.groupby(["amfi_code", "scheme_name", "sub_category", "sector"])["weight_pct"].sum().reset_index()
    hhi_list = []
    for (code, name, sub_cat), group in sector_alloc.groupby(["amfi_code", "scheme_name", "sub_category"]):
        weights = group["weight_pct"].values
        hhi = np.sum(weights ** 2)
        sorted_sec = group.sort_values("weight_pct", ascending=False)
        tier = "Diversified" if hhi < 1500 else ("Moderately Concentrated" if hhi <= 2500 else "Highly Concentrated")
        hhi_list.append({
            "amfi_code": code,
            "scheme_name": name,
            "sub_category": sub_cat,
            "hhi_score": round(hhi, 2),
            "concentration_tier": tier,
            "top_sector": sorted_sec.iloc[0]["sector"],
            "top_sector_weight_pct": round(sorted_sec.iloc[0]["weight_pct"], 2)
        })
    df_hhi = pd.DataFrame(hhi_list).sort_values("hhi_score", ascending=False).reset_index(drop=True)
    df_hhi.to_csv(out_dir / "sector_hhi.csv", index=False)
    return df_hhi

def run_all_advanced_analytics() -> bool:
    """Runs all Day 6 quantitative calculations and outputs CSVs and charts."""
    print("\n" + "=" * 80)
    print("STAGE 6: Executing Advanced Risk Analytics, VaR/CVaR & Behavioral Models")
    print("=" * 80)
    compute_var_cvar()
    print("  [OK] Computed Historical VaR (95%) & CVaR (var_cvar_report.csv)")
    compute_rolling_sharpe()
    print("  [OK] Generated 90-Day Rolling Sharpe Ratio comparison chart")
    compute_cohort_analysis()
    print("  [OK] Generated Investor Cohort Analysis (cohort_analysis.csv)")
    compute_sip_continuity()
    print("  [OK] Completed SIP Continuity & Churn Risk Analysis (sip_continuity.csv)")
    compute_sector_hhi()
    print("  [OK] Calculated Sector HHI Concentration across equity funds (sector_hhi.csv)")
    return True

if __name__ == "__main__":
    run_all_advanced_analytics()
