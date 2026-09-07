"""
Bluestock Mutual Fund Analytics - Day 6 Advanced Analytics Pipeline
===================================================================
Executes all quantitative analyses for Day 6:
1. Historical Value at Risk (VaR 95%) and Conditional VaR (CVaR) for all 40 schemes.
2. Rolling 90-day Sharpe Ratio computation and charting for 5 key funds.
3. Investor Cohort Analysis by initial transaction year.
4. SIP Continuity and Churn Analysis for investors with 6+ SIP contributions.
5. Sector Concentration (Herfindahl-Hirschman Index - HHI) across equity funds.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# File paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
CHARTS_DIR = os.path.join(REPORTS_DIR, "charts")

os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(CHARTS_DIR, exist_ok=True)

NAV_FILE = os.path.join(DATA_DIR, "02_nav_history_clean.csv")
MASTER_FILE = os.path.join(DATA_DIR, "01_fund_master_clean.csv")
TX_FILE = os.path.join(DATA_DIR, "08_investor_transactions_clean.csv")
HOLDINGS_FILE = os.path.join(DATA_DIR, "09_portfolio_holdings_clean.csv")
PERF_FILE = os.path.join(DATA_DIR, "07_scheme_performance_clean.csv")


def task1_compute_var_cvar():
    """
    Task 1: Compute Historical VaR (95%) and CVaR for all 40 schemes.
    VaR = 5th percentile of daily return distribution.
    CVaR = Mean of daily returns at or below the VaR threshold.
    """
    print("\n" + "=" * 80)
    print("TASK 1: Historical VaR (95%) and CVaR (Expected Shortfall) Computation")
    print("=" * 80)
    
    nav_df = pd.read_csv(NAV_FILE)
    nav_df["date"] = pd.to_datetime(nav_df["date"])
    nav_df = nav_df.sort_values(["amfi_code", "date"]).reset_index(drop=True)
    nav_df["daily_return"] = nav_df.groupby("amfi_code")["nav"].pct_change()
    
    master_df = pd.read_csv(MASTER_FILE)[["amfi_code", "scheme_name", "category", "sub_category", "risk_category"]]
    
    results = []
    for amfi_code, group in nav_df.groupby("amfi_code"):
        rets = group["daily_return"].dropna()
        if len(rets) < 30:
            continue
            
        # 95% Historical VaR corresponds to the 5th percentile of return distribution
        var_95_daily = np.percentile(rets, 5)
        # CVaR is expected return conditioned on return <= VaR_95
        tail_losses = rets[rets <= var_95_daily]
        cvar_95_daily = tail_losses.mean() if len(tail_losses) > 0 else var_95_daily
        
        var_95_ann = var_95_daily * np.sqrt(252)
        cvar_95_ann = cvar_95_daily * np.sqrt(252)
        
        results.append({
            "amfi_code": amfi_code,
            "var_95_daily_pct": round(var_95_daily * 100, 4),
            "cvar_95_daily_pct": round(cvar_95_daily * 100, 4),
            "var_95_ann_pct": round(var_95_ann * 100, 2),
            "cvar_95_ann_pct": round(cvar_95_ann * 100, 2),
            "std_daily_pct": round(rets.std() * 100, 4),
            "observation_days": len(rets)
        })
        
    res_df = pd.DataFrame(results)
    res_df = res_df.merge(master_df, on="amfi_code", how="left")
    
    # Sort by highest tail risk (most negative VaR)
    res_df = res_df.sort_values("var_95_daily_pct", ascending=True).reset_index(drop=True)
    
    # Save output CSVs
    out_path_root = os.path.join(BASE_DIR, "var_cvar_report.csv")
    out_path_rep = os.path.join(REPORTS_DIR, "var_cvar_report.csv")
    res_df.to_csv(out_path_root, index=False)
    res_df.to_csv(out_path_rep, index=False)
    
    print(f"Successfully computed VaR & CVaR for {len(res_df)} mutual fund schemes.")
    print("Top 5 Highest Downside Risk Schemes (Largest 1-Day Potential Loss):")
    print(res_df[["amfi_code", "scheme_name", "category", "risk_category", "var_95_daily_pct", "cvar_95_daily_pct"]].head(5).to_string(index=False))
    print(f"\nSaved report to:\n  - {out_path_root}\n  - {out_path_rep}")
    return res_df


def task2_rolling_sharpe():
    """
    Task 2: Compute Rolling 90-day Sharpe Ratio and plot over time for 5 key funds.
    Formula: returns.rolling(90).mean() / returns.rolling(90).std() * sqrt(252)
    """
    print("\n" + "=" * 80)
    print("TASK 2: Rolling 90-Day Sharpe Ratio Analysis & Chart Generation")
    print("=" * 80)
    
    nav_df = pd.read_csv(NAV_FILE)
    nav_df["date"] = pd.to_datetime(nav_df["date"])
    nav_df = nav_df.sort_values(["amfi_code", "date"]).reset_index(drop=True)
    nav_df["daily_return"] = nav_df.groupby("amfi_code")["nav"].pct_change()
    
    master_df = pd.read_csv(MASTER_FILE).set_index("amfi_code")["scheme_name"].to_dict()
    
    key_fund_codes = [148567, 100033, 120843, 120504, 120505]
    fund_labels = {
        148567: "Mirae Asset Large Cap Fund",
        100033: "HDFC Mid-Cap Opportunities Fund",
        120843: "Kotak Flexicap Fund",
        120504: "ICICI Pru Bluechip Fund",
        120505: "ICICI Pru Midcap Fund"
    }
    
    palette = {
        148567: "#1A365D",  # Dark Navy
        100033: "#DD6B20",  # Burnt Orange
        120843: "#3182CE",  # Slate Blue
        120504: "#38A169",  # Emerald Green
        120505: "#805AD5"   # Purple
    }
    
    sub = nav_df[nav_df["amfi_code"].isin(key_fund_codes)].copy()
    pivoted = sub.pivot(index="date", columns="amfi_code", values="daily_return")
    
    # Rolling 90-day Sharpe ratio
    rolling_mean = pivoted.rolling(window=90).mean()
    rolling_std = pivoted.rolling(window=90).std()
    rolling_sharpe = (rolling_mean / rolling_std) * np.sqrt(252)
    rolling_sharpe = rolling_sharpe.dropna(how="all")
    
    # Plotting
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    fig, ax = plt.subplots(figsize=(14, 7), dpi=300)
    
    for code in key_fund_codes:
        if code in rolling_sharpe.columns:
            series = rolling_sharpe[code]
            ax.plot(
                series.index,
                series.values,
                label=fund_labels.get(code, master_df.get(code, str(code))),
                color=palette.get(code, "#333333"),
                linewidth=2.2,
                alpha=0.9
            )
            
    # Zero Sharpe reference line
    ax.axhline(0, color="#E53E3E", linestyle="--", linewidth=1.5, alpha=0.7, label="Neutral Threshold (Sharpe = 0)")
    ax.axhline(1.0, color="#718096", linestyle=":", linewidth=1.2, alpha=0.6, label="Benchmark Benchmark (Sharpe = 1.0)")
    
    ax.set_title("90-Day Rolling Annualized Sharpe Ratio Comparison (2022–2026)", fontsize=15, fontweight="bold", pad=15, color="#1A365D")
    ax.set_xlabel("Date", fontsize=12, fontweight="bold", labelpad=10, color="#2D3748")
    ax.set_ylabel("Annualized Sharpe Ratio", fontsize=12, fontweight="bold", labelpad=10, color="#2D3748")
    
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.xticks(rotation=30, ha="right", fontsize=10)
    plt.yticks(fontsize=10)
    
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(loc="upper left", frameon=True, facecolor="#F7FAFC", edgecolor="#CBD5E0", fontsize=10)
    
    plt.tight_layout()
    
    chart_root = os.path.join(BASE_DIR, "rolling_sharpe_chart.png")
    chart_reports = os.path.join(CHARTS_DIR, "rolling_sharpe_chart.png")
    fig.savefig(chart_root, dpi=300)
    fig.savefig(chart_reports, dpi=300)
    plt.close()
    
    print("Successfully generated Rolling 90-Day Sharpe Ratio chart.")
    print(f"Saved chart to:\n  - {chart_root}\n  - {chart_reports}")
    return rolling_sharpe


def task3_investor_cohort_analysis():
    """
    Task 3: Investor cohort analysis grouped by first transaction year.
    Computes avg SIP amount, total invested, and top fund preference per cohort.
    """
    print("\n" + "=" * 80)
    print("TASK 3: Investor Cohort Analysis by Initial Entry Year")
    print("=" * 80)
    
    tx_df = pd.read_csv(TX_FILE)
    tx_df["transaction_date"] = pd.to_datetime(tx_df["transaction_date"])
    master_df = pd.read_csv(MASTER_FILE)[["amfi_code", "scheme_name"]]
    tx_df = tx_df.merge(master_df, on="amfi_code", how="left")
    
    # Identify first transaction year per investor
    first_tx = tx_df.groupby("investor_id")["transaction_date"].min().dt.year.rename("cohort_year")
    tx_df = tx_df.merge(first_tx, on="investor_id", how="left")
    
    cohort_list = []
    for year, group in tx_df.groupby("cohort_year"):
        total_inv = group["investor_id"].nunique()
        total_amount = group["amount_inr"].sum()
        avg_tx = group["amount_inr"].mean()
        
        sip_group = group[group["transaction_type"] == "SIP"]
        total_sip_amount = sip_group["amount_inr"].sum()
        avg_sip = sip_group["amount_inr"].mean() if len(sip_group) > 0 else 0
        sip_tx_count = len(sip_group)
        
        # Top fund preference by transaction volume
        top_fund_series = group["scheme_name"].value_counts()
        top_fund_name = top_fund_series.index[0] if not top_fund_series.empty else "N/A"
        top_fund_count = top_fund_series.iloc[0] if not top_fund_series.empty else 0
        
        cohort_list.append({
            "cohort_year": int(year),
            "total_investors": total_inv,
            "total_invested_inr": total_amount,
            "avg_transaction_inr": round(avg_tx, 2),
            "total_sip_inr": total_sip_amount,
            "avg_sip_inr": round(avg_sip, 2),
            "sip_transaction_count": sip_tx_count,
            "top_preferred_scheme": top_fund_name,
            "top_scheme_transactions": top_fund_count
        })
        
    cohort_df = pd.DataFrame(cohort_list).sort_values("cohort_year").reset_index(drop=True)
    
    out_root = os.path.join(BASE_DIR, "cohort_analysis.csv")
    out_rep = os.path.join(REPORTS_DIR, "cohort_analysis.csv")
    cohort_df.to_csv(out_root, index=False)
    cohort_df.to_csv(out_rep, index=False)
    
    print("Investor Cohort Breakdown:")
    print(cohort_df.to_string(index=False))
    print(f"\nSaved cohort analysis to:\n  - {out_root}\n  - {out_rep}")
    return cohort_df


def task4_sip_continuity_analysis():
    """
    Task 4: SIP continuity analysis for investors with 6+ SIP transactions.
    Computes avg gap between dates and flags investors with gap > 35 days as 'at-risk'.
    """
    print("\n" + "=" * 80)
    print("TASK 4: SIP Continuity and Churn Risk Analysis")
    print("=" * 80)
    
    tx_df = pd.read_csv(TX_FILE)
    tx_df["transaction_date"] = pd.to_datetime(tx_df["transaction_date"])
    
    # Filter to SIP transactions only
    sip_df = tx_df[tx_df["transaction_type"] == "SIP"].sort_values(["investor_id", "transaction_date"])
    
    # Select investors with 6 or more SIP transactions
    sip_counts = sip_df.groupby("investor_id").size()
    eligible_investors = sip_counts[sip_counts >= 6].index
    
    eligible_df = sip_df[sip_df["investor_id"].isin(eligible_investors)].copy()
    
    # Calculate consecutive difference in days
    eligible_df["gap_days"] = eligible_df.groupby("investor_id")["transaction_date"].diff().dt.days
    
    continuity_summary = eligible_df.groupby("investor_id").agg(
        sip_count=("transaction_date", "count"),
        first_sip_date=("transaction_date", "min"),
        latest_sip_date=("transaction_date", "max"),
        total_sip_amount=("amount_inr", "sum"),
        avg_sip_amount=("amount_inr", "mean"),
        avg_gap_days=("gap_days", "mean"),
        max_gap_days=("gap_days", "max"),
        std_gap_days=("gap_days", "std")
    ).reset_index()
    
    # Round metrics
    continuity_summary["avg_sip_amount"] = continuity_summary["avg_sip_amount"].round(2)
    continuity_summary["avg_gap_days"] = continuity_summary["avg_gap_days"].round(2)
    continuity_summary["max_gap_days"] = continuity_summary["max_gap_days"].round(1)
    continuity_summary["std_gap_days"] = continuity_summary["std_gap_days"].round(2)
    
    # Flag investors with average gap > 35 days as "at-risk"
    continuity_summary["is_at_risk"] = continuity_summary["avg_gap_days"] > 35
    continuity_summary["retention_status"] = np.where(continuity_summary["is_at_risk"], "At-Risk", "Healthy Cadence")
    
    out_root = os.path.join(BASE_DIR, "sip_continuity.csv")
    out_rep = os.path.join(REPORTS_DIR, "sip_continuity.csv")
    continuity_summary.to_csv(out_root, index=False)
    continuity_summary.to_csv(out_rep, index=False)
    
    total_analyzed = len(continuity_summary)
    at_risk_count = continuity_summary["is_at_risk"].sum()
    healthy_count = total_analyzed - at_risk_count
    at_risk_pct = (at_risk_count / total_analyzed) * 100
    
    print(f"Total Eligible SIP Investors (6+ transactions): {total_analyzed}")
    print(f"At-Risk Investors (Avg Gap > 35 Days):         {at_risk_count} ({at_risk_pct:.2f}%)")
    print(f"Healthy Cadence Investors (Avg Gap <= 35 Days):  {healthy_count} ({100 - at_risk_pct:.2f}%)")
    print(f"Overall Average Gap Across Cohort:             {continuity_summary['avg_gap_days'].mean():.2f} days")
    print(f"\nSaved SIP continuity dataset to:\n  - {out_root}\n  - {out_rep}")
    return continuity_summary


def task5_sector_hhi():
    """
    Task 5: Sector HHI Concentration analysis across equity funds.
    Herfindahl-Hirschman Index = sum(weight_i^2) per fund.
    High HHI = Concentrated portfolio; Low HHI = Diversified portfolio.
    """
    print("\n" + "=" * 80)
    print("TASK 5: Sector Concentration (Herfindahl-Hirschman Index - HHI)")
    print("=" * 80)
    
    holdings_df = pd.read_csv(HOLDINGS_FILE)
    master_df = pd.read_csv(MASTER_FILE)[["amfi_code", "scheme_name", "category", "sub_category"]]
    holdings_df = holdings_df.merge(master_df, on="amfi_code", how="left")
    
    # Filter equity schemes
    equity_holdings = holdings_df[holdings_df["category"] == "Equity"].copy()
    
    # Sector weight per fund
    sector_alloc = equity_holdings.groupby(["amfi_code", "scheme_name", "category", "sub_category", "sector"])["weight_pct"].sum().reset_index()
    
    hhi_list = []
    for (code, name, cat, sub_cat), group in sector_alloc.groupby(["amfi_code", "scheme_name", "category", "sub_category"]):
        weights = group["weight_pct"].values
        # Standard HHI calculation: sum of squared percentage allocations (0 - 10,000 scale)
        hhi_score = np.sum(weights ** 2)
        
        # Sort sectors to find top sector exposure
        sorted_sec = group.sort_values("weight_pct", ascending=False)
        top_sector = sorted_sec.iloc[0]["sector"]
        top_sector_weight = sorted_sec.iloc[0]["weight_pct"]
        num_sectors = len(group)
        
        # Classification according to DOJ/FTC guidelines:
        # < 1500: Unconcentrated / Diversified
        # 1500 - 2500: Moderately Concentrated
        # > 2500: Highly Concentrated
        if hhi_score < 1500:
            tier = "Diversified"
        elif hhi_score <= 2500:
            tier = "Moderately Concentrated"
        else:
            tier = "Highly Concentrated"
            
        hhi_list.append({
            "amfi_code": code,
            "scheme_name": name,
            "category": cat,
            "sub_category": sub_cat,
            "hhi_score": round(hhi_score, 2),
            "concentration_tier": tier,
            "num_sectors": num_sectors,
            "top_sector": top_sector,
            "top_sector_weight_pct": round(top_sector_weight, 2)
        })
        
    hhi_df = pd.DataFrame(hhi_list).sort_values("hhi_score", ascending=False).reset_index(drop=True)
    
    out_root = os.path.join(BASE_DIR, "sector_hhi.csv")
    out_rep = os.path.join(REPORTS_DIR, "sector_hhi.csv")
    hhi_df.to_csv(out_root, index=False)
    hhi_df.to_csv(out_rep, index=False)
    
    print(f"Evaluated HHI Sector Concentration for {len(hhi_df)} equity schemes.")
    print("\nTop 5 Most Concentrated Equity Funds (Highest HHI):")
    print(hhi_df[["amfi_code", "scheme_name", "sub_category", "hhi_score", "concentration_tier", "top_sector", "top_sector_weight_pct"]].head(5).to_string(index=False))
    print("\nTop 5 Most Diversified Equity Funds (Lowest HHI):")
    print(hhi_df[["amfi_code", "scheme_name", "sub_category", "hhi_score", "concentration_tier", "top_sector", "top_sector_weight_pct"]].tail(5).to_string(index=False))
    print(f"\nSaved HHI report to:\n  - {out_root}\n  - {out_rep}")
    return hhi_df


def main():
    print("=" * 80)
    print("STARTING BLUESTOCK MUTUAL FUND CAPSTONE - DAY 6 QUANTITATIVE PIPELINE")
    print("=" * 80)
    
    task1_compute_var_cvar()
    task2_rolling_sharpe()
    task3_investor_cohort_analysis()
    task4_sip_continuity_analysis()
    task5_sector_hhi()
    
    print("\n" + "=" * 80)
    print("DAY 6 ANALYTICS PIPELINE COMPLETED SUCCESSFULLY!")
    print("=" * 80)


if __name__ == "__main__":
    main()
