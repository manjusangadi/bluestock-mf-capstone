"""
Analytics Module: Fund Performance Analytics & Scorecard
=========================================================
Computes CAGR, Sharpe, Sortino, Alpha, Beta, Max DD, and Scorecard.
"""

import os
import sqlite3
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DB_PATH = PROJECT_ROOT / "db" / "bluestock_mf.db"
if not DB_PATH.exists():
    DB_PATH = PROJECT_ROOT / "bluestock_mf.db"
REPORTS_DIR = PROJECT_ROOT / "reports"
CHARTS_DIR = REPORTS_DIR / "charts"

def compute_performance_analytics(db_file: Path = DB_PATH, reports_dir: Path = REPORTS_DIR) -> pd.DataFrame:
    """
    Executes full fund performance calculations and compiles composite scorecard.
    """
    os.makedirs(reports_dir, exist_ok=True)
    os.makedirs(CHARTS_DIR, exist_ok=True)
    print("\n" + "=" * 80)
    print(f"STAGE 5: Computing Fund Performance Analytics from {db_file}")
    print("=" * 80)

    conn = sqlite3.connect(str(db_file))
    df_funds = pd.read_sql_query("SELECT amfi_code, fund_house, scheme_name, category, plan, expense_ratio_pct FROM dim_fund;", conn)
    df_nav_raw = pd.read_sql_query("SELECT amfi_code, date, nav FROM fact_nav ORDER BY amfi_code, date;", conn)
    df_nav_raw['date'] = pd.to_datetime(df_nav_raw['date'])

    df_bench_raw = pd.read_sql_query("SELECT date, index_name, close_value FROM benchmark_indices ORDER BY index_name, date;", conn)
    df_bench_raw['date'] = pd.to_datetime(df_bench_raw['date'])

    # Pivot NAVs and Benchmarks
    pivoted_nav = df_nav_raw.pivot(index='date', columns='amfi_code', values='nav')
    daily_returns = pivoted_nav.pct_change().dropna(how='all')

    pivoted_bench = df_bench_raw.pivot(index='date', columns='index_name', values='close_value')
    bench_returns = pivoted_bench.pct_change().dropna(how='all')

    rf_daily = 0.065 / 252.0

    metrics_list = []
    # Alignment benchmark: NIFTY 100 TRI or fallback
    bench_col = "NIFTY 100 TRI" if "NIFTY 100 TRI" in bench_returns.columns else bench_returns.columns[0]
    bench_series = bench_returns[bench_col].dropna()

    for amfi_code in pivoted_nav.columns:
        nav_series = pivoted_nav[amfi_code].dropna()
        ret_series = daily_returns[amfi_code].dropna()

        if len(nav_series) < 30:
            continue

        n_days = len(nav_series)
        tot_ret = (nav_series.iloc[-1] / nav_series.iloc[0]) - 1.0
        cagr_max = ((1.0 + tot_ret) ** (252.0 / n_days) - 1.0) * 100.0

        # 3Yr CAGR
        cagr_3yr = cagr_max
        if n_days >= 756:
            cagr_3yr = ((nav_series.iloc[-1] / nav_series.iloc[-756]) ** (252.0 / 756.0) - 1.0) * 100.0

        # 1Yr CAGR
        cagr_1yr = cagr_max
        if n_days >= 252:
            cagr_1yr = ((nav_series.iloc[-1] / nav_series.iloc[-252]) ** (252.0 / 252.0) - 1.0) * 100.0

        # Sharpe & Sortino
        excess_ret = ret_series - rf_daily
        daily_std = ret_series.std()
        sharpe = (excess_ret.mean() / daily_std) * np.sqrt(252.0) if daily_std > 0 else 0.0

        downside = ret_series[ret_series < rf_daily] - rf_daily
        downside_std = np.sqrt((downside ** 2).mean()) if len(downside) > 0 else daily_std
        sortino = (excess_ret.mean() / downside_std) * np.sqrt(252.0) if downside_std > 0 else 0.0

        # Beta & Alpha vs Benchmark
        comb = pd.concat([ret_series, bench_series], axis=1, join='inner').dropna()
        if len(comb) >= 30:
            slope, intercept, r_val, _, _ = linregress(comb.iloc[:, 1], comb.iloc[:, 0])
            beta = slope
            alpha_ann = (intercept * 252.0) * 100.0
            r_sq = r_val ** 2
        else:
            beta, alpha_ann, r_sq = 1.0, 0.0, 0.0

        # Max Drawdown
        cum_max = nav_series.cummax()
        dd = (nav_series / cum_max) - 1.0
        max_dd = dd.min() * 100.0

        metrics_list.append({
            'amfi_code': amfi_code,
            'cagr_1yr_pct': round(cagr_1yr, 2),
            'cagr_3yr_pct': round(cagr_3yr, 2),
            'cagr_max_pct': round(cagr_max, 2),
            'sharpe_ratio': round(sharpe, 2),
            'sortino_ratio': round(sortino, 2),
            'beta': round(beta, 2),
            'alpha_pct': round(alpha_ann, 2),
            'r_squared': round(r_sq, 2),
            'max_drawdown_pct': round(max_dd, 2)
        })

    df_metrics = pd.DataFrame(metrics_list)
    df_merged = df_funds.merge(df_metrics, on='amfi_code', how='inner')

    # Compute Percentile Ranks for Composite Scorecard (0-100)
    df_merged['rank_3yr_cagr'] = df_merged['cagr_3yr_pct'].rank(pct=True) * 100.0
    df_merged['rank_sharpe'] = df_merged['sharpe_ratio'].rank(pct=True) * 100.0
    df_merged['rank_alpha'] = df_merged['alpha_pct'].rank(pct=True) * 100.0
    df_merged['rank_expense'] = df_merged['expense_ratio_pct'].rank(ascending=False, pct=True) * 100.0
    df_merged['rank_max_dd'] = df_merged['max_drawdown_pct'].rank(pct=True) * 100.0

    df_merged['fund_score'] = (
        0.30 * df_merged['rank_3yr_cagr'] +
        0.25 * df_merged['rank_sharpe'] +
        0.20 * df_merged['rank_alpha'] +
        0.15 * df_merged['rank_expense'] +
        0.10 * df_merged['rank_max_dd']
    ).round(2)

    df_scorecard = df_merged.sort_values('fund_score', ascending=False).reset_index(drop=True)
    df_scorecard.to_csv(reports_dir / "fund_scorecard.csv", index=False)
    
    # Save Alpha/Beta
    df_alpha_beta = df_merged[['amfi_code', 'scheme_name', 'beta', 'alpha_pct', 'r_squared']]
    df_alpha_beta.to_csv(reports_dir / "alpha_beta.csv", index=False)

    conn.close()
    print(f"  [OK] Saved fund_scorecard.csv & alpha_beta.csv in {reports_dir}")
    print("\nTop 3 Funds by Scorecard Score:")
    print(df_scorecard[['amfi_code', 'scheme_name', 'cagr_3yr_pct', 'sharpe_ratio', 'fund_score']].head(3).to_string(index=False))
    return df_scorecard

if __name__ == "__main__":
    compute_performance_analytics()
