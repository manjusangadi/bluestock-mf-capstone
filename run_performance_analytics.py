import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress
import os

# Set plotting style
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 10, 'axes.labelsize': 11, 'axes.titlesize': 12, 'figure.titlesize': 14})

db_path = "bluestock_mf.db"
reports_dir = "reports"
charts_dir = "reports/charts"
os.makedirs(charts_dir, exist_ok=True)

# Connect to database
conn = sqlite3.connect(db_path)

print("1. Extracting data from SQLite...")
# Load fund master and performance details
df_funds = pd.read_sql_query("""
    SELECT amfi_code, fund_house, scheme_name, category, plan, expense_ratio_pct
    FROM dim_fund;
""", conn)

# Load daily NAV values
df_nav_raw = pd.read_sql_query("""
    SELECT amfi_code, date, nav
    FROM fact_nav
    ORDER BY amfi_code, date;
""", conn)
df_nav_raw['date'] = pd.to_datetime(df_nav_raw['date'])

# Load benchmark indices
df_bench_raw = pd.read_sql_query("""
    SELECT date, index_name, close_value
    FROM benchmark_indices
    ORDER BY index_name, date;
""", conn)
df_bench_raw['date'] = pd.to_datetime(df_bench_raw['date'])

print(f"Loaded {len(df_funds)} funds, {len(df_nav_raw)} NAV rows, and {len(df_bench_raw)} benchmark rows.")

# -------------------------------------------------------------
# Metric Calculations
# -------------------------------------------------------------
print("\n2. Computing daily returns and validating distributions...")
# Calculate daily returns for each fund
df_nav_raw['daily_return'] = df_nav_raw.groupby('amfi_code')['nav'].pct_change()

# Calculate NIFTY100 daily returns
df_n100 = df_bench_raw[df_bench_raw['index_name'] == 'NIFTY100'].copy().sort_values('date')
df_n100['n100_return'] = df_n100['close_value'].pct_change()

# Calculate NIFTY50 daily returns
df_n50 = df_bench_raw[df_bench_raw['index_name'] == 'NIFTY50'].copy().sort_values('date')
df_n50['n50_return'] = df_n50['close_value'].pct_change()

# Statistics dictionary to validate distributions
stats_list = []

# Loop through each fund to calculate metrics
fund_metrics = []

for idx, fund in df_funds.iterrows():
    amfi_code = fund['amfi_code']
    scheme_name = fund['scheme_name']
    
    # Slice NAV for current fund
    fund_nav = df_nav_raw[df_nav_raw['amfi_code'] == amfi_code].copy().sort_values('date')
    
    # 1. Daily Return Distribution Stats
    daily_rets = fund_nav['daily_return'].dropna()
    mean_ret = daily_rets.mean()
    std_ret = daily_rets.std()
    min_ret = daily_rets.min()
    max_ret = daily_rets.max()
    
    stats_list.append({
        'amfi_code': amfi_code,
        'scheme_name': scheme_name,
        'mean_daily_return': mean_ret,
        'std_daily_return': std_ret,
        'min_daily_return': min_ret,
        'max_daily_return': max_ret,
        'count_days': len(daily_rets)
    })
    
    # 2. CAGR Calculations
    latest_date = fund_nav['date'].max()
    latest_nav = fund_nav.loc[fund_nav['date'] == latest_date, 'nav'].values[0]
    
    # Find closest dates for start parameters
    def get_nav_at_offset_years(years):
        target_date = latest_date - pd.DateOffset(years=years)
        # Find index with minimum absolute date difference
        diffs = (fund_nav['date'] - target_date).abs()
        closest_idx = diffs.idxmin()
        closest_row = fund_nav.loc[closest_idx]
        # Return NAV and actual year offset
        actual_years = (latest_date - closest_row['date']).days / 365.25
        return closest_row['nav'], actual_years, closest_row['date']

    # 1-Year CAGR
    nav_1yr_start, yrs_1yr, d_1yr = get_nav_at_offset_years(1)
    cagr_1yr = (latest_nav / nav_1yr_start) ** (1.0 / yrs_1yr) - 1.0 if yrs_1yr > 0 else np.nan
    
    # 3-Year CAGR
    nav_3yr_start, yrs_3yr, d_3yr = get_nav_at_offset_years(3)
    cagr_3yr = (latest_nav / nav_3yr_start) ** (1.0 / yrs_3yr) - 1.0 if yrs_3yr > 0 else np.nan
    
    # Max Available Period CAGR
    first_row = fund_nav.iloc[0]
    yrs_max = (latest_date - first_row['date']).days / 365.25
    cagr_max = (latest_nav / first_row['nav']) ** (1.0 / yrs_max) - 1.0 if yrs_max > 0 else np.nan

    # 3. Sharpe Ratio (Annualized)
    # Rf = 6.5% repo rate proxy, daily Rf = 0.065 / 252
    rf_daily = 0.065 / 252
    excess_rets = daily_rets - rf_daily
    sharpe = (excess_rets.mean() / std_ret) * np.sqrt(252) if std_ret > 0 else np.nan
    
    # 4. Sortino Ratio (Annualized)
    downside_rets = np.minimum(daily_rets, 0)
    downside_std = np.sqrt(np.mean(downside_rets ** 2))
    sortino = (excess_rets.mean() / downside_std) * np.sqrt(252) if downside_std > 0 else np.nan

    # 5. Alpha & Beta (OLS vs Nifty 100 daily returns)
    df_reg = pd.merge(fund_nav[['date', 'daily_return']], df_n100[['date', 'n100_return']], on='date').dropna()
    if len(df_reg) > 30:
        slope, intercept, r_val, p_val, std_err = linregress(df_reg['n100_return'], df_reg['daily_return'])
        beta = slope
        alpha = intercept * 252 # Annualized Alpha
        r_squared = r_val ** 2
    else:
        beta, alpha, r_squared = np.nan, np.nan, np.nan

    # 6. Maximum Drawdown
    running_max = fund_nav['nav'].cummax()
    drawdowns = fund_nav['nav'] / running_max - 1.0
    max_dd = drawdowns.min()
    
    # Worst drawdown date range
    trough_idx = drawdowns.idxmin()
    trough_date = fund_nav.loc[trough_idx, 'date']
    peak_idx = fund_nav.loc[:trough_idx, 'nav'].idxmax()
    peak_date = fund_nav.loc[peak_idx, 'date']

    fund_metrics.append({
        'amfi_code': amfi_code,
        'scheme_name': scheme_name,
        'fund_house': fund['fund_house'],
        'category': fund['category'],
        'plan': fund['plan'],
        'expense_ratio_pct': fund['expense_ratio_pct'],
        'cagr_1yr_pct': cagr_1yr * 100,
        'cagr_3yr_pct': cagr_3yr * 100,
        'cagr_max_pct': cagr_max * 100,
        'sharpe_ratio': sharpe,
        'sortino_ratio': sortino,
        'beta': beta,
        'alpha_pct': alpha * 100,
        'r_squared': r_squared,
        'max_drawdown_pct': max_dd * 100,
        'worst_dd_start': peak_date.strftime('%Y-%m-%d'),
        'worst_dd_end': trough_date.strftime('%Y-%m-%d')
    })

# Convert list to DataFrame
df_metrics = pd.DataFrame(fund_metrics)
df_stats = pd.DataFrame(stats_list)

# Validate returns distribution statistics
print("\nDaily Returns Distribution Summary (Across all 40 schemes):")
print(df_stats[['mean_daily_return', 'std_daily_return', 'min_daily_return', 'max_daily_return']].describe().to_string())

# Save Alpha Beta results
df_alpha_beta = df_metrics[['amfi_code', 'scheme_name', 'alpha_pct', 'beta', 'r_squared']].copy()
df_alpha_beta.to_csv("alpha_beta.csv", index=False)
df_alpha_beta.to_csv(os.path.join(reports_dir, "alpha_beta.csv"), index=False)
print("Saved alpha_beta.csv successfully.")

# -------------------------------------------------------------
# Fund Scorecard (0-100)
# -------------------------------------------------------------
print("\n3. Building Fund Scorecard...")
# Ranks (Higher return, Sharpe, Alpha are better -> ascending rank.
#        Lower expense is better -> descending rank.
#        Less negative Max DD (closer to 0) is better -> ascending rank).
df_metrics['rank_3yr_cagr'] = df_metrics['cagr_3yr_pct'].rank(pct=True) * 100
df_metrics['rank_sharpe'] = df_metrics['sharpe_ratio'].rank(pct=True) * 100
df_metrics['rank_alpha'] = df_metrics['alpha_pct'].rank(pct=True) * 100
df_metrics['rank_expense'] = df_metrics['expense_ratio_pct'].rank(ascending=False, pct=True) * 100
df_metrics['rank_max_dd'] = df_metrics['max_drawdown_pct'].rank(pct=True) * 100

# Calculate weighted scorecard score (0-100)
df_metrics['fund_score'] = (
    0.30 * df_metrics['rank_3yr_cagr'] +
    0.25 * df_metrics['rank_sharpe'] +
    0.20 * df_metrics['rank_alpha'] +
    0.15 * df_metrics['rank_expense'] +
    0.10 * df_metrics['rank_max_dd']
)

# Sort by scorecard score descending
df_scorecard = df_metrics.sort_values(by='fund_score', ascending=False).reset_index(drop=True)
# Add a performance tier column
def get_tier(score):
    if score >= 80: return 'Tier 1 (Excellent)'
    elif score >= 60: return 'Tier 2 (Good)'
    elif score >= 40: return 'Tier 3 (Average)'
    else: return 'Tier 4 (Underperforming)'

df_scorecard['performance_tier'] = df_scorecard['fund_score'].apply(get_tier)

# Save Scorecard CSV
df_scorecard.to_csv("fund_scorecard.csv", index=False)
df_scorecard.to_csv(os.path.join(reports_dir, "fund_scorecard.csv"), index=False)
print("Saved fund_scorecard.csv successfully.")

# Print top 5 funds
print("\nTop 5 Funds by Scorecard Score:")
print(df_scorecard[['scheme_name', 'cagr_3yr_pct', 'sharpe_ratio', 'alpha_pct', 'expense_ratio_pct', 'fund_score']].head(5).to_string())

# -------------------------------------------------------------
# Benchmark Comparison & Tracking Error (3 Years)
# -------------------------------------------------------------
print("\n4. Generating Benchmark Comparison and Tracking Errors over 3 years...")
top_5_amfi = df_scorecard.head(5)['amfi_code'].tolist()
top_5_names = df_scorecard.head(5)['scheme_name'].tolist()

# Define start and end date for 3 year benchmark comparison
end_date = pd.to_datetime('2026-05-29')
start_date = end_date - pd.DateOffset(years=3) # 2023-05-29

# Slice daily NAV for top 5 funds in 3yr window
df_nav_3yr = df_nav_raw[(df_nav_raw['date'] >= start_date) & (df_nav_raw['date'] <= end_date)].copy()
df_n100_3yr = df_n100[(df_n100['date'] >= start_date) & (df_n100['date'] <= end_date)].copy()
df_n50_3yr = df_n50[(df_n50['date'] >= start_date) & (df_n50['date'] <= end_date)].copy()

# Plot Cumulative Return normalized to 100
plt.figure(figsize=(12, 7))

# Calculate Tracking Errors
tracking_errors = []

for code, name in zip(top_5_amfi, top_5_names):
    # Slice single fund
    df_f = df_nav_3yr[df_nav_3yr['amfi_code'] == code].copy().sort_values('date')
    if len(df_f) > 0:
        first_nav = df_f.iloc[0]['nav']
        df_f['normalized_nav'] = (df_f['nav'] / first_nav) * 100
        
        # Plot
        plt.plot(df_f['date'], df_f['normalized_nav'], label=name.split(" - ")[0], linewidth=1.5)
        
        # Align with NIFTY100 and NIFTY50 returns to compute Tracking Error
        df_align = pd.merge(df_f[['date', 'daily_return']], df_n100_3yr[['date', 'n100_return']], on='date').dropna()
        df_align = pd.merge(df_align, df_n50_3yr[['date', 'n50_return']], on='date').dropna()
        
        # Tracking Error = std(fund_return - benchmark_return) * sqrt(252)
        te_n100 = np.std(df_align['daily_return'] - df_align['n100_return']) * np.sqrt(252) * 100
        te_n50 = np.std(df_align['daily_return'] - df_align['n50_return']) * np.sqrt(252) * 100
        
        tracking_errors.append({
            'amfi_code': code,
            'scheme_name': name,
            'tracking_error_vs_nifty100_pct': te_n100,
            'tracking_error_vs_nifty50_pct': te_n50
        })

# Calculate normalized benchmarks starting on start_date
df_n100_3yr = df_n100_3yr.sort_values('date')
df_n50_3yr = df_n50_3yr.sort_values('date')

n100_start_close = df_n100_3yr.iloc[0]['close_value']
df_n100_3yr['normalized_close'] = (df_n100_3yr['close_value'] / n100_start_close) * 100

n50_start_close = df_n50_3yr.iloc[0]['close_value']
df_n50_3yr['normalized_close'] = (df_n50_3yr['close_value'] / n50_start_close) * 100

# Plot benchmarks
plt.plot(df_n100_3yr['date'], df_n100_3yr['normalized_close'], label='NIFTY 100 (Benchmark)', color='black', linewidth=2.5, linestyle='--')
plt.plot(df_n50_3yr['date'], df_n50_3yr['normalized_close'], label='NIFTY 50 (Benchmark)', color='red', linewidth=2.5, linestyle=':')

plt.title("3-Year Cumulative Return Comparison: Top 5 Funds vs Benchmarks (Base 100)")
plt.xlabel("Date")
plt.ylabel("Normalized Value (Starting at 100)")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Save comparison charts
chart_path_reports = f"{charts_dir}/benchmark_comparison.png"
chart_path_root = "benchmark_comparison.png"
plt.savefig(chart_path_reports, dpi=150)
plt.savefig(chart_path_root, dpi=150)
plt.close()
print("Saved benchmark_comparison.png successfully.")

# Save Tracking Errors CSV
df_te = pd.DataFrame(tracking_errors)
df_te.to_csv(os.path.join(reports_dir, "tracking_errors.csv"), index=False)
df_te.to_csv("tracking_errors.csv", index=False)
print("Saved tracking_errors.csv successfully.")

print("\nTracking Errors of Top 5 Funds (%):")
print(df_te[['scheme_name', 'tracking_error_vs_nifty100_pct', 'tracking_error_vs_nifty50_pct']].to_string(index=False))

conn.close()
print("\nAll performance calculations successfully completed!")
