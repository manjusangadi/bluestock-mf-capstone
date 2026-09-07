# Implementation Plan - Day 6: Advanced Analytics & Risk Metrics

This plan details the implementation of **Day 6 — Advanced Analytics + Risk Metrics** for the Bluestock Mutual Fund Analytics Capstone Project, fulfilling all 7 tasks and required deliverables.

---

## User Review Required

> [!IMPORTANT]
> **Risk Appetite Tier Mapping in Fund Recommender**:
> In our dataset (`07_scheme_performance_clean.csv`), the `risk_grade` column contains 5 tiers: `Low`, `Moderate`, `Moderately High`, `High`, and `Very High`.
> To provide an intuitive 3-choice input (`Low`, `Moderate`, `High`), we propose mapping:
> - **Low** $\rightarrow$ `risk_grade == 'Low'` (Fixed income / Liquid / Low volatility)
> - **Moderate** $\rightarrow$ `risk_grade IN ('Moderate', 'Moderately High')` (Large Cap, Hybrid, balanced funds)
> - **High** $\rightarrow$ `risk_grade IN ('High', 'Very High')` (Mid Cap, Small Cap, Sectoral/Thematic funds)
> The recommender will rank by `sharpe_ratio` descending and return the top 3 schemes.

---

## Proposed Changes & Tasks

### 1. Historical Value at Risk (VaR 95%) & Conditional VaR (CVaR)
* **Dataset**: [`data/processed/02_nav_history_clean.csv`](file:///d:/desktop2/bluestock_mf_capstone/data/processed/02_nav_history_clean.csv) & [`01_fund_master_clean.csv`](file:///d:/desktop2/bluestock_mf_capstone/data/processed/01_fund_master_clean.csv).
* **Mathematical Formulations**:
  - Daily return: $R_t = \frac{\text{NAV}_t}{\text{NAV}_{t-1}} - 1$
  - $\text{VaR}_{95\%} = \text{Percentile}(R, 5\%)$ (the loss threshold exceeded only 5% of trading days).
  - $\text{CVaR}_{95\%} = \mathbb{E}[R \mid R \le \text{VaR}_{95\%}]$ (Expected Shortfall: average loss on the worst 5% days).
  - Annualized VaR: $\text{VaR}_{\text{ann}} = \text{VaR}_{\text{daily}} \times \sqrt{252}$
  - Annualized CVaR: $\text{CVaR}_{\text{ann}} = \text{CVaR}_{\text{daily}} \times \sqrt{252}$
* **Deliverable**: Generated for all 40 mutual fund schemes. Saved to `var_cvar_report.csv` and `reports/var_cvar_report.csv`.

---

### 2. Rolling 90-Day Sharpe Ratio & Multi-Asset Plot
* **Dataset**: NAV daily returns over the complete history (2022–2026).
* **Formula**:
  $$\text{Rolling Sharpe}_{90d}(t) = \frac{\mu_{90}(t)}{\sigma_{90}(t)} \times \sqrt{252}$$
  *(where $\mu_{90}$ is the 90-day rolling mean and $\sigma_{90}$ is the 90-day rolling sample standard deviation)*.
* **5 Key Funds Selected**:
  1. `148567` — Mirae Asset Large Cap Fund (Large Cap)
  2. `100033` — HDFC Mid-Cap Opportunities Fund (Mid Cap)
  3. `120843` — Kotak Flexicap Fund (Flexicap)
  4. `120504` — ICICI Prudential Bluechip Fund (Large Cap)
  5. `120505` — ICICI Prudential Midcap Fund (Mid Cap)
* **Visualization**: Generate a multi-line comparison plot with Bluestock styling (`#1A365D`, `#3182CE`, etc.), zero reference line, and grid.
* **Deliverable**: Saved as `rolling_sharpe_chart.png` and `reports/charts/rolling_sharpe_chart.png`.

---

### 3. Investor Cohort Analysis
* **Dataset**: [`data/processed/08_investor_transactions_clean.csv`](file:///d:/desktop2/bluestock_mf_capstone/data/processed/08_investor_transactions_clean.csv).
* **Methodology**:
  - Identify the earliest transaction year per investor (`2024` or `2025`) as their cohort year.
  - Group transactions by cohort year.
  - Aggregate:
    - Unique investor count per cohort.
    - Total investment volume (INR).
    - Average transaction size.
    - Total SIP contributions and average SIP ticket size.
    - Top preferred mutual fund scheme by investment count and volume.
* **Deliverable**: Saved as `cohort_analysis.csv` and `reports/cohort_analysis.csv`.

---

### 4. SIP Continuity & Churn Analysis
* **Dataset**: [`data/processed/08_investor_transactions_clean.csv`](file:///d:/desktop2/bluestock_mf_capstone/data/processed/08_investor_transactions_clean.csv) filtered to `transaction_type == 'SIP'`.
* **Methodology**:
  - Filter to investors with 6 or more SIP transactions (1,362 investors).
  - Compute consecutive transaction date differences ($\Delta t = t_i - t_{i-1}$) in days.
  - Calculate average gap per investor.
  - Flag investors with $\text{avg\_gap} > 35\text{ days}$ as `"at-risk"` (signals missed monthly SIP mandates or early termination).
* **Deliverable**: Saved as `sip_continuity.csv` and `reports/sip_continuity.csv`.

---

### 5. Simple Fund Recommender Script (`recommender.py`)
* **File**: [`recommender.py`](file:///d:/desktop2/bluestock_mf_capstone/recommender.py)
* **Functionality**:
  - Standalone script with command-line argument parsing (`--risk Low|Moderate|High`) and interactive fallback prompt.
  - Loads [`07_scheme_performance_clean.csv`](file:///d:/desktop2/bluestock_mf_capstone/data/processed/07_scheme_performance_clean.csv).
  - Filters by risk tier and sorts by `sharpe_ratio` in descending order.
  - Outputs a cleanly formatted recommendation table displaying Scheme Name, Category, Sharpe Ratio, 3Y CAGR (%), AUM (Cr), and Risk Grade.

---

### 6. Sector Concentration (Herfindahl-Hirschman Index - HHI)
* **Dataset**: [`data/processed/09_portfolio_holdings_clean.csv`](file:///d:/desktop2/bluestock_mf_capstone/data/processed/09_portfolio_holdings_clean.csv).
* **Methodology**:
  - Group holdings by fund and sector to obtain sector portfolio weight $w_s$ ($0 \le w_s \le 100$).
  - Calculate HHI:
    $$\text{HHI} = \sum_{s=1}^{N} (w_s)^2$$
  - Scale interpretation:
    - $\text{HHI} < 1,500$: Diversified sector allocation.
    - $1,500 \le \text{HHI} \le 2,500$: Moderate concentration.
    - $\text{HHI} > 2,500$: High sector concentration risk.
  - Compare all 34 equity funds and identify dominant sector per fund.
* **Deliverable**: Saved as `sector_hhi.csv` and `reports/sector_hhi.csv`.

---

### 7. Comprehensive Jupyter Notebook (`notebooks/Advanced_Analytics.ipynb`)
* **File**: [`notebooks/Advanced_Analytics.ipynb`](file:///d:/desktop2/bluestock_mf_capstone/notebooks/Advanced_Analytics.ipynb).
* **Contents**:
  - Clean, sequential cells implementing all 6 analyses.
  - Formatted tables and embedded charts.
  - **Section 5: 5 Key Strategic Insights** written in rich markdown:
    1. **Tail Risk Disparity**: High-beta Mid/Small cap schemes carry daily VaR up to -2.69% and CVaR past -3.5%, while debt funds maintain daily downside under -0.05%.
    2. **Rolling Sharpe Cyclicality**: Mid-cap funds exhibit wide Sharpe swings (-0.5 to +3.0) across 90-day windows, highlighting the risk of point-in-time performance evaluation.
    3. **Cohort Maturity**: 2024 cohort accounts for over 98% of total volume, while 2025 new entrants exhibit higher initial SIP ticket sizes.
    4. **SIP Continuity & Mandate Health**: Over 97% of investors with 6+ SIPs exceed a 35-day average cadence, revealing significant cadence irregularities and potential churn.
    5. **Sector Concentration Dynamics**: Thematic and mid-cap equity schemes show elevated HHI (> 2,200) heavily weighted toward Financial Services and Industrials.

---

### 8. Project Master Script & Documentation
* Create a master execution script [`run_advanced_analytics.py`](file:///d:/desktop2/bluestock_mf_capstone/run_advanced_analytics.py) that generates all CSVs and the chart cleanly.
* Update [`README.md`](file:///d:/desktop2/bluestock_mf_capstone/README.md) with complete Day 6 documentation, methodology, table summaries, and git commit instructions.

---

## Verification Plan

### Automated Verification
1. Run the Python pipeline:
   ```bash
   python run_advanced_analytics.py
   ```
2. Verify output files exist and are populated:
   - `var_cvar_report.csv` (40 rows)
   - `rolling_sharpe_chart.png` (non-empty image)
   - `cohort_analysis.csv` (2 cohort rows)
   - `sip_continuity.csv` (1,362 rows)
   - `sector_hhi.csv` (34 equity funds)
3. Test `recommender.py`:
   ```bash
   python recommender.py --risk Low
   python recommender.py --risk Moderate
   python recommender.py --risk High
   ```
4. Verify `notebooks/Advanced_Analytics.ipynb` is well-formed and can execute without error.
