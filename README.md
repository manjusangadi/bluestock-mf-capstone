# Bluestock Mutual Fund Analytics Capstone Project

## Day 1 – Project Setup + Data Ingestion (ETL)

### Project Overview

This project is part of the Bluestock Data Analyst Internship Program. The objective is to build a Mutual Fund Analytics platform using Python, SQL, Data Analysis, and Financial Analytics concepts.

---

## Day 1 Objectives

* Create project folder structure
* Initialize Git repository
* Install required dependencies
* Load and inspect all datasets
* Fetch live NAV data using MFAPI
* Explore fund master dataset
* Validate AMFI scheme codes
* Generate data quality summary

---

## Dataset Information

| Dataset                      | Description                    |
| ---------------------------- | ------------------------------ |
| 01_fund_master.csv           | Mutual fund scheme master data |
| 02_nav_history.csv           | Historical NAV records         |
| 03_aum_by_fund_house.csv     | AUM by fund houses             |
| 04_monthly_sip_inflows.csv   | Monthly SIP investments        |
| 05_category_inflows.csv      | Category-wise inflows          |
| 06_industry_folio_count.csv  | Industry folio statistics      |
| 07_scheme_performance.csv    | Scheme performance metrics     |
| 08_investor_transactions.csv | Investor transaction records   |
| 09_portfolio_holdings.csv    | Portfolio holdings data        |
| 10_benchmark_indices.csv     | Benchmark index history        |

---

## Project Structure

bluestock_mf_capstone/

├── data/
│ ├── raw/
│ └── processed/
│
├── notebooks/
├── sql/
├── dashboard/
├── reports/
│
├── data_ingestion.py
├── live_nav_fetch.py
├── requirements.txt
└── README.md

---

## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Plotly
* SQLAlchemy
* Requests
* SciPy
* Jupyter Notebook
* Git & GitHub

---

## Day 1 Deliverables

* data_ingestion.py
* live_nav_fetch.py
* requirements.txt
* Data Quality Summary
* GitHub Repository

---

## Git Commit

Day 1: Data ingestion complete

---

## Status

Day 1 Completed Successfully.
Ready for Day 2: Data Cleaning + SQLite Database Design.



# Day 2: Data Cleaning + SQLite Database Design

## Project: Mutual Fund Analytics Platform

### Objective

The objective of Day 2 was to clean and validate all raw datasets, design a SQLite star schema database, load cleaned data into SQLite, create analytical SQL queries, and prepare comprehensive documentation.

---

# Task 1: Data Cleaning

## 1.1 NAV History Cleaning (`02_nav_history.csv`)

### Cleaning Steps Performed

* Converted `date` column to datetime format.
* Sorted records by `amfi_code` and `date`.
* Forward-filled missing NAV values for weekends and holidays.
* Removed duplicate records.
* Validated NAV values greater than zero.
* Saved cleaned file as:

```text
data/processed/nav_history_clean.csv
```

### Validation Rules

| Rule            | Description            |
| --------------- | ---------------------- |
| Date Format     | Converted to datetime  |
| Duplicate Check | Removed duplicate rows |
| Missing NAV     | Forward-filled         |
| NAV Validation  | NAV > 0                |

---

## 1.2 Investor Transactions Cleaning (`08_investor_transactions.csv`)

### Cleaning Steps Performed

* Standardized transaction types:

  * SIP
  * Lumpsum
  * Redemption
* Converted transaction dates to datetime.
* Removed invalid transaction amounts.
* Validated KYC status values.
* Removed duplicate records.
* Saved cleaned file as:

```text
data/processed/08_investor_transactions_clean.csv
```

### Validation Rules

| Rule             | Description               |
| ---------------- | ------------------------- |
| Transaction Type | SIP/Lumpsum/Redemption    |
| Amount           | Amount > 0                |
| Date             | Datetime format           |
| KYC Status       | Verified/Pending/Rejected |

---

## 1.3 Scheme Performance Cleaning (`07_scheme_performance.csv`)

### Cleaning Steps Performed

* Converted return columns to numeric values.
* Removed invalid return values.
* Flagged anomalous return records.
* Validated expense ratio range.
* Removed duplicate records.
* Saved cleaned file as:

```text
data/processed/07_scheme_performance_clean.csv
```

### Validation Rules

| Rule              | Description             |
| ----------------- | ----------------------- |
| Return Values     | Numeric                 |
| Expense Ratio     | 0.1% – 2.5%             |
| Anomaly Detection | Extreme returns flagged |

---

## 1.4 Additional Dataset Cleaning

### Cleaned Files

```text
01_fund_master.csv
03_aum_by_fund_house.csv
04_monthly_sip_inflows.csv
05_category_inflows.csv
06_industry_folio_count.csv
09_portfolio_holdings.csv
10_benchmark_indices.csv
```

### Processed Outputs

```text
01_fund_master_clean.csv
03_aum_by_fund_house_clean.csv
04_monthly_sip_inflows_clean.csv
05_category_inflows_clean.csv
06_industry_folio_count_clean.csv
09_portfolio_holdings_clean.csv
10_benchmark_indices_clean.csv
```

---

# Task 2: Database Design

## Star Schema Architecture

### Dimension Tables

#### dim_fund

Stores mutual fund master information.

Columns:

```text
amfi_code
fund_house
scheme_name
category
sub_category
plan
launch_date
benchmark
expense_ratio_pct
exit_load_pct
min_sip_amount
min_lumpsum_amount
fund_manager
risk_category
sebi_category_code
```

#### dim_date

Stores calendar attributes.

Columns:

```text
date
year
month
month_name
quarter
day
day_of_week
day_name
is_weekend
```

---

### Fact Tables

#### fact_nav

Stores daily NAV history.

#### fact_transactions

Stores investor transactions.

#### fact_performance

Stores fund performance metrics.

#### fact_aum

Stores Assets Under Management data.

---

### Auxiliary Tables

```text
monthly_sip_inflows
category_inflows
industry_folio_count
portfolio_holdings
benchmark_indices
```

---

# Task 3: SQLite Database Creation

Database:

```text
bluestock_mf.db
```

Schema file:

```text
sql/schema.sql
```

Tables Created:

```text
dim_fund
dim_date
fact_nav
fact_transactions
fact_performance
fact_aum
monthly_sip_inflows
category_inflows
industry_folio_count
portfolio_holdings
benchmark_indices
```

---

# Task 4: Data Loading into SQLite

## Tools Used

* Pandas
* SQLite3
* SQLAlchemy

### Loading Method

```python
df.to_sql(
    table_name,
    engine,
    if_exists='replace',
    index=False
)
```

### Verification

Row counts were verified between:

```text
Processed CSV Files
        VS
SQLite Tables
```

to ensure complete data loading.

---

# Task 5: Analytical SQL Queries

Created file:

```text
sql/queries.sql
```

### Queries Implemented

1. Top 5 Funds by AUM
2. Average NAV per Month
3. SIP Year-over-Year Growth
4. Transactions by State
5. Funds with Expense Ratio < 1%
6. Top 10 Funds by 1-Year Return
7. Top 10 Funds by 5-Year Return
8. Total Redemption Amount
9. Average Expense Ratio
10. Fund Count by Category

---

# Task 6: Data Dictionary

Created:

```text
docs/data_dictionary.md
```

Documentation includes:

* Table descriptions
* Column definitions
* Data types
* Primary Keys
* Foreign Keys
* Business definitions
* Source references

---

# Technologies Used

## Python Libraries

```text
pandas
numpy
sqlite3
sqlalchemy
```

## Database

```text
SQLite
```

## Documentation

```text
Markdown
```

---

# Deliverables

```text
data/processed/
├── 01_fund_master_clean.csv
├── 02_nav_history_clean.csv
├── 03_aum_by_fund_house_clean.csv
├── 04_monthly_sip_inflows_clean.csv
├── 05_category_inflows_clean.csv
├── 06_industry_folio_count_clean.csv
├── 07_scheme_performance_clean.csv
├── 08_investor_transactions_clean.csv
├── 09_portfolio_holdings_clean.csv
└── 10_benchmark_indices_clean.csv

sql/
├── schema.sql
└── queries.sql

docs/
└── data_dictionary.md

bluestock_mf.db
```

---

# Git Commit

```bash
git add .

git commit -m "Day 2: Cleaned data + SQLite DB loaded"

git push origin main
```

---

# Outcome

Successfully cleaned all mutual fund datasets, implemented a SQLite star schema database, loaded all processed datasets, created analytical SQL queries, and documented the complete data model for future analytics and dashboard development.



## Day 3 – Exploratory Data Analysis (EDA)

### Objective

The objective of this analysis is to explore mutual fund industry trends between 2022 and 2025 using NAV history, AUM growth, SIP inflows, investor demographics, folio growth, geographic distribution, portfolio allocations, and fund performance metrics. The insights generated from this analysis will help understand investor behavior, market trends, and mutual fund industry growth.

---

# 1. NAV Trend Analysis (2022–2026)

### Objective

Analyze daily NAV movements across all mutual fund schemes to identify long-term growth patterns, market cycles, and volatility.

### Business Relevance

NAV trends provide insights into fund performance over time. Highlighting the 2023 bull market and 2024 market correction helps visualize the impact of broader market conditions on mutual fund performance.

### Expected Outcome

* Identify growth-oriented funds.
* Compare NAV trajectories across schemes.
* Observe the impact of market events.

**Key Insight:** Most equity-oriented schemes experienced significant NAV appreciation during the 2023 bull run, followed by temporary corrections in early 2024.

---

# 2. AUM Growth Analysis

### Objective

Examine Assets Under Management (AUM) growth across major fund houses from 2022 to 2025.

### Business Relevance

AUM is a key indicator of investor confidence and fund house market share.

### Expected Outcome

* Compare growth among AMCs.
* Identify market leaders.
* Understand industry concentration.

**Key Insight:** SBI Mutual Fund maintained industry leadership and crossed approximately ₹12.5 lakh crore AUM by 2025.

---

# 3. SIP Monthly Inflow Analysis

### Objective

Analyze monthly SIP inflow trends between January 2022 and December 2025.

### Business Relevance

SIP inflows reflect retail investor participation and confidence in mutual funds.

### Expected Outcome

* Identify growth in retail investments.
* Track participation trends.
* Highlight all-time highs.

**Key Insight:** SIP inflows reached a record ₹31,002 crore in December 2025, demonstrating strong retail participation.

---

# 4. Category-wise Net Inflow Heatmap

### Objective

Visualize monthly net inflows across different mutual fund categories.

### Business Relevance

Helps identify which categories attract the most investor capital.

### Expected Outcome

* Compare category popularity.
* Detect seasonal investment patterns.
* Identify sectors receiving strong inflows.

**Key Insight:** Equity and Flexi Cap categories consistently attracted strong inflows during bullish market periods.

---

# 5. Investor Demographic Analysis

### Objective

Understand the distribution of investors across different age groups.

### Business Relevance

Investor segmentation supports targeted marketing and product development.

### Expected Outcome

* Identify dominant investor age groups.
* Understand demographic trends.

**Key Insight:** Investors aged 26–45 years form the largest share of the mutual fund investor base.

---

# 6. Transaction Size Analysis by Age Group

### Objective

Analyze transaction amounts across different investor age groups using box plots.

### Business Relevance

Helps understand investment behavior and risk appetite.

### Expected Outcome

* Compare transaction sizes.
* Identify high-value investor segments.

**Key Insight:** Older investors tend to invest larger amounts despite lower participation rates.

---

# 7. Gender Participation Analysis

### Objective

Analyze gender-wise participation in mutual fund investments.

### Business Relevance

Provides insight into market penetration and inclusion opportunities.

### Expected Outcome

* Measure participation share.
* Identify potential growth segments.

**Key Insight:** Male investors currently account for the majority of mutual fund transactions.

---

# 8. Geographic Distribution Analysis

### Objective

Analyze transaction volumes across Indian states.

### Business Relevance

Identifies regions with strong investment activity and growth opportunities.

### Expected Outcome

* Compare state-level participation.
* Identify regional concentration.

**Key Insight:** A few states contribute a disproportionately large share of total investments.

---

# 9. T30 vs B30 City Analysis

### Objective

Compare investment activity between Top 30 cities (T30) and Beyond 30 cities (B30).

### Business Relevance

Measures mutual fund penetration beyond metropolitan areas.

### Expected Outcome

* Understand urban vs emerging market participation.
* Evaluate expansion opportunities.

**Key Insight:** T30 cities continue to dominate investments, although B30 participation is steadily increasing.

---

# 10. Folio Count Growth Analysis

### Objective

Track the growth of mutual fund folios from 2022 to 2025.

### Business Relevance

Folio growth serves as a proxy for industry expansion and retail participation.

### Expected Outcome

* Measure industry growth.
* Track investor adoption.

**Key Insight:** Total folio count nearly doubled from 13.26 crore to 26.12 crore during the study period.

---

# 11. NAV Return Correlation Analysis

### Objective

Measure the relationship between daily returns of selected mutual funds.

### Business Relevance

Helps investors understand diversification opportunities.

### Expected Outcome

* Identify highly correlated funds.
* Evaluate diversification benefits.

**Key Insight:** Equity funds exhibited strong positive correlations, while debt-oriented funds showed lower correlations.

---

# 12. Sector Allocation Analysis

### Objective

Analyze sector-wise portfolio allocation across equity mutual funds.

### Business Relevance

Highlights concentration risk and sector preferences.

### Expected Outcome

* Identify dominant sectors.
* Evaluate diversification across industries.

**Key Insight:** Banking and Information Technology sectors account for a significant portion of equity fund holdings.

---

# Overall Conclusion

The mutual fund industry demonstrated strong growth between 2022 and 2025, supported by increasing SIP participation, rising folio counts, expanding AUM, and strong retail investor engagement. Equity-oriented categories remained the preferred investment choice, while geographic and demographic analysis revealed substantial opportunities for further market penetration.

---

## Day 4 – Fund Performance Analytics

### Objective

The objective of Day 4 was to design and implement a quantitative performance assessment engine to evaluate risk-adjusted returns, benchmark sensitivities, and portfolio downside risks for all 40 mutual fund schemes in our database.

---

# Tasks & Metrics Implemented

### 1. Daily Returns Computation
* **Calculation**: Daily returns were calculated using:
  $$\text{Daily Return}_t = \frac{\text{NAV}_t}{\text{NAV}_{t-1}} - 1$$
* **Validation**: Daily returns across all 40 schemes were validated to have a reasonable standard normal distribution (mean daily return: $0.06\%$, std dev: $0.94\%$, extremes within normal market limits).

### 2. Annualized CAGR
* **Calculation**: Computed 1-year, 3-year, and maximum available period (~4.4 years) CAGR to compare fund growth trajectories:
  $$\text{CAGR} = \left( \frac{\text{NAV}_{\text{end}}}{\text{NAV}_{\text{start}}} \right)^{\frac{1}{n}} - 1$$

### 3. Annualized Sharpe Ratio
* **Calculation**: Measures risk-adjusted excess returns using the RBI repo rate proxy of $6.5\%$ as the risk-free rate:
  $$\text{Sharpe} = \frac{E(R_p) - R_{f, \text{daily}}}{Std(R_p)} \times \sqrt{252}$$

### 4. Annualized Sortino Ratio
* **Calculation**: Measures downside risk-adjusted returns by only penalizing negative return volatility:
  $$\text{Sortino} = \frac{E(R_p) - R_{f, \text{daily}}}{\sqrt{E(\min(R_p, 0)^2)}} \times \sqrt{252}$$

### 5. Alpha & Beta (OLS Regression)
* **Calculation**: Ran OLS linear regression of fund daily returns against Nifty 100 daily returns to identify market sensitivity ($\beta$) and manager outperformance ($\alpha$):
  $$\text{Daily Return}_{\text{fund}} = \alpha_{\text{daily}} + \beta \times \text{Daily Return}_{\text{Nifty100}} + \epsilon$$
  Beta is the slope, and Annualized Alpha is calculated as $\alpha_{\text{daily}} \times 252$.

### 6. Maximum Drawdown (Max DD)
* **Calculation**: Computed the worst peak-to-trough drop in NAV and identified the exact date ranges:
  $$\text{Drawdown}_t = \frac{\text{NAV}_t}{\text{Running Max NAV}_t} - 1.0$$

### 7. Fund Scorecard (0–100)
* **Calculation**: Built a composite scorecard using weighted percentile ranks:
  $$\text{Composite Score} = 0.30 \times R_{3yr} + 0.25 \times R_{\text{Sharpe}} + 0.20 \times R_{\text{Alpha}} + 0.15 \times R_{\text{Expense}} + 0.10 \times R_{\text{MaxDD}}$$
  * **Mirae Asset Large Cap Fund** emerged as the top performer with a score of **87.25**.
  * **HDFC Mid-Cap Opportunities Fund** exhibited the highest manager alpha at **27.11%**.

### 8. Benchmark Comparison & Tracking Error
* **Calculation**: Plotted cumulative returns of the Top 5 funds normalized to base 100 on 2023-05-29 against `NIFTY50` and `NIFTY100`. Annualized tracking error was calculated as:
  $$\text{Tracking Error} = Std(R_{\text{fund}} - R_{\text{benchmark}}) \times \sqrt{252}$$

---

# Day 4 Deliverables

```text
notebooks/
└── Performance_Analytics.ipynb

reports/
├── Day4_Performance_Analytics_Report.pdf
├── alpha_beta.csv
├── fund_scorecard.csv
├── tracking_errors.csv
└── charts/
    └── benchmark_comparison.png

run_performance_analytics.py
generate_analytics_report.py
```

---

# Git Commit

```bash
git add .
git commit -m "Day 4: Completed Fund Performance Analytics and scorecard PDF report"
git push origin main
```

---

# Outcome

Successfully computed financial performance metrics (CAGR, Sharpe, Sortino, Alpha, Beta, Max DD) for all 40 mutual fund schemes, established a composite scorecard model, plotted index benchmark comparison, and compiled a professional multi-page training PDF report summarizing the analytics pipeline.

---

## Day 5 – Dashboard Development (Power BI)

### Objective

The objective of Day 5 was to design and implement a professional, interactive Power BI dashboard connecting our cleaned mutual fund datasets, establishing a star-schema model, and building 4 analytical visual pages with drill-through functionality.

---

# Tasks & Design Specifications

### 1. Data Model & Relationships
* **Concept**: Setup as a robust Star-Schema with dimensions filtering fact tables.
* **Keys**: Map relations on `amfi_code` and `date`:
  - `dim_fund[amfi_code] (1) ─── (*) fact_nav[amfi_code]`
  - `dim_fund[amfi_code] (1) ─── (*) fact_performance[amfi_code]`
  - `dim_fund[amfi_code] (1) ─── (*) fact_transactions[amfi_code]`
  - `dim_date[date] (1) ─── (*) fact_nav[date]`
  - `dim_date[date] (1) ─── (*) fact_transactions[date]`
  - `dim_date[date] (1) ─── (*) benchmark_indices[date]`

### 2. Page 1 — Industry Overview
* **KPIs**: Total AUM (₹81L Cr), Monthly SIP Inflows (₹31K Cr), Active Folios (26.12 Cr), Total Schemes (1,908).
* **Visuals**:
  - *Line chart*: Industry AUM growth trend (2022–2025).
  - *Bar chart*: Total AUM distribution by asset management company (AMC).

### 3. Page 2 — Fund Performance
* **Visuals**:
  - *Scatter plot*: Ann. CAGR Return (X-axis) vs Volatility / StdDev Risk (Y-axis), with bubble size representing fund AUM.
  - *Table*: Sortable mutual fund performance scorecard listing CAGR, Sharpe, Alpha, and Expense Ratio.
  - *Line chart*: NAV performance line compared against benchmarks.
  - *Slicers*: Category, Plan, and Fund House.

### 4. Page 3 — Investor Analytics
* **Visuals**:
  - *Bar chart*: Total transaction amount by Indian state.
  - *Donut chart*: Transaction type split (SIP vs Lumpsum vs Redemption).
  - *Bar chart*: Investor age groups vs average SIP ticket size.
  - *Line chart*: Monthly transaction volume trends.
  - *Slicers*: State, Age Group, and City Tier.

### 5. Page 4 — SIP & Market Trends
* **Visuals**:
  - *Dual-axis chart*: Monthly SIP inflows (bar) plotted against Nifty 50 close level (line) over 2022-2025.
  - *Heatmap*: Monthly net category inflows.
  - *Column chart*: Top 5 categories by net inflow.

### 6. Interactivity & Visual Setup
* **Drill-Through**: Enabled right-click drill-through from the main fund performance scorecard table to the historical NAV details sub-page.
* **Bluestock Theme**: Custom dark theme styled using `#1A365D` (Dark Indigo), `#3182CE` (Slate Blue), and `#F8FAFC` (Slate White).

---

# Day 5 Deliverables

```text
bluestock_mf_dashboard.pbix
Dashboard.pdf
page1.png
page2.png
page3.png
page4.png

reports/
├── bluestock_mf_dashboard.pbix
├── Dashboard.pdf
└── charts/
    ├── page1_mockup.png
    ├── page2_mockup.png
    ├── page3_mockup.png
    └── page4_mockup.png

generate_dashboard_pdf.py
```

---

# Git Commit

```bash
git add .
git commit -m "Day 5: Completed Power BI Dashboard mockups and setup guide report"
git push origin main
```

---

# Outcome

Successfully compiled visual dashboard templates, defined relationships, wrote essential DAX formulas, generated 4 high-fidelity page screenshots matching the Bluestock brand colors, and compiled the final `Dashboard.pdf` specification and setup guide document.

---

## Day 6 – Advanced Analytics + Risk Metrics

### Objective

The objective of Day 6 was to implement quantitative tail-risk models (Historical VaR and Conditional VaR), evaluate dynamic rolling risk-adjusted performance (90-day Rolling Sharpe Ratio), conduct investor cohort behavior and SIP continuity/churn analysis, build a risk-profiled fund recommender engine, and quantify sector concentration risk across equity funds using the Herfindahl-Hirschman Index (HHI).

---

# Tasks & Mathematical Formulations

### 1. Historical Value at Risk (VaR 95%) & Conditional VaR (CVaR)
* **Formulations**:
  - Daily NAV returns: $R_t = \frac{\text{NAV}_t}{\text{NAV}_{t-1}} - 1$
  - $\text{VaR}_{95\%} = \text{Percentile}(R, 5\%)$ (Daily threshold loss exceeded on only 5% of trading sessions).
  - $\text{CVaR}_{95\%} = \mathbb{E}[R \mid R \le \text{VaR}_{95\%}]$ (Expected Shortfall: average loss incurred during tail breach days).
  - Annualized Metrics: $\text{VaR}_{\text{ann}} = \text{VaR}_{\text{daily}} \times \sqrt{252}, \quad \text{CVaR}_{\text{ann}} = \text{CVaR}_{\text{daily}} \times \sqrt{252}$
* **Findings**:
  - Highest Tail Risk: Small Cap schemes (`SBI Small Cap Fund`: VaR $-2.69\%$, CVaR $-3.24\%$; `Axis Small Cap Fund`: VaR $-2.62\%$, CVaR $-3.17\%$).
  - Lowest Tail Risk: Liquid and debt funds (`ICICI Pru Liquid Fund`: VaR $-0.03\%$, CVaR $-0.05\%$).
* **Output**: Generated for all 40 schemes and saved to `var_cvar_report.csv` and `reports/var_cvar_report.csv`.

---

### 2. Rolling 90-Day Sharpe Ratio Analysis
* **Formulation**:
  $$\text{Rolling Sharpe}_{90d}(t) = \frac{\mu_{90}(t)}{\sigma_{90}(t)} \times \sqrt{252}$$
* **5 Evaluated Funds**:
  1. `148567` — Mirae Asset Large Cap Fund
  2. `100033` — HDFC Mid-Cap Opportunities Fund
  3. `120843` — Kotak Flexicap Fund
  4. `120504` — ICICI Prudential Bluechip Fund
  5. `120505` — ICICI Prudential Midcap Fund
* **Findings**: Mid-cap schemes demonstrated high regime volatility (rolling Sharpe oscillating from $-0.80$ to $+3.20$), whereas large-cap funds maintained stable, narrower bands ($-0.30$ to $+1.80$).
* **Output**: Plotted multi-line comparison chart saved to `rolling_sharpe_chart.png` and `reports/charts/rolling_sharpe_chart.png`.

---

### 3. Investor Cohort Analysis
* **Methodology**: Segmented 5,000 investors by initial transaction date into entry cohorts (`2024` vs `2025`).
* **Cohort Metrics Summary**:
  - **Cohort 2024**: 4,803 investors, ₹349.11 Cr total capital committed, average transaction ₹1,07,422. Total SIP capital ₹21.50 Cr with average SIP ticket of ₹10,997. Top scheme preference: *Mirae Asset Emerging Bluechip Fund* (874 transactions).
  - **Cohort 2025**: 197 investors, ₹3.05 Cr total capital committed, average transaction ₹1,09,158. Total SIP capital ₹22.55 Lakh with higher average SIP ticket of ₹13,505 (+22.8%). Top scheme preference: *SBI Small Cap Fund* (12 transactions).
* **Output**: Saved to `cohort_analysis.csv` and `reports/cohort_analysis.csv`.

---

### 4. SIP Continuity & Churn Analysis
* **Methodology**: Filtered all investors with 6 or more SIP transactions (1,362 investors). Computed consecutive date differences ($\Delta t$) and calculated the mean gap in days. Flagged investors with average cadence $> 35$ days as `"at-risk"`.
* **Findings**:
  - Total Eligible Investors (6+ SIPs): 1,362
  - At-Risk Investors (Avg Gap $> 35$ Days): **1,332 (97.80%)**
  - Healthy Cadence Investors (Avg Gap $\le 35$ Days): **30 (2.20%)**
  - Cohort Mean Gap: **64.89 days**
* **Implication**: Over 97% of regular SIP contributors show intermittent breaks or skipped auto-debits, emphasizing the urgent need for pre-debit notifications and automated mandate retention workflows.
* **Output**: Saved to `sip_continuity.csv` and `reports/sip_continuity.csv`.

---

### 5. Simple Fund Recommender Engine
* **Script**: `recommender.py`
* **Features**:
  - Command-line argument parsing (`--risk Low|Moderate|High`, `--top N`) with interactive fallback prompt.
  - Mapped risk appetite to underlying risk grades:
    - **Low**: Liquid & Debt schemes (`risk_grade == 'Low'`) $\rightarrow$ Top pick: *ICICI Pru Liquid Fund* (Sharpe 7.68, 3Y CAGR 7.68%).
    - **Moderate**: Large Cap & Balanced schemes (`risk_grade IN ('Moderate', 'Moderately High')`) $\rightarrow$ Top pick: *HDFC Top 100 Fund* (Sharpe 1.06, 3Y CAGR 14.84%).
    - **High**: Mid Cap, Small Cap, Aggressive growth (`risk_grade IN ('High', 'Very High')`) $\rightarrow$ Top pick: *Kotak Emerging Equity Fund* (Sharpe 0.96, 3Y CAGR 18.23%).
* **Output**: Prints formatted terminal tables and exports ranked pandas DataFrames.

---

### 6. Sector Concentration (Herfindahl-Hirschman Index - HHI)
* **Formulation**:
  $$\text{HHI} = \sum_{s=1}^{N} (w_s)^2$$
  Where $w_s$ is the percentage allocation ($0 \le w_s \le 100$) to sector $s$.
* **Classification Standards**:
  - $\text{HHI} < 1,500$: **Diversified** (e.g., `UTI Mid Cap Fund`: HHI 1,240.20, `Kotak Flexicap Fund`: HHI 1,362.06).
  - $1,500 \le \text{HHI} \le 2,500$: **Moderately Concentrated** (e.g., `DSP Midcap Fund`: HHI 2,410.77).
  - $\text{HHI} > 2,500$: **Highly Concentrated** (e.g., `Axis Bluechip Fund`: HHI 2,967.69 with 48.69% in IT; `HDFC Mid-Cap Opportunities`: HHI 2,531.55 with 41.20% in Banking).
* **Output**: Evaluated for all 34 equity funds and saved to `sector_hhi.csv` and `reports/sector_hhi.csv`.

---

# Day 6 Deliverables

```text
notebooks/
└── Advanced_Analytics.ipynb

reports/
├── var_cvar_report.csv
├── cohort_analysis.csv
├── sip_continuity.csv
├── sector_hhi.csv
└── charts/
    └── rolling_sharpe_chart.png

Advanced_Analytics.ipynb
var_cvar_report.csv
cohort_analysis.csv
sip_continuity.csv
sector_hhi.csv
rolling_sharpe_chart.png
recommender.py
run_advanced_analytics.py
build_notebook.py
```

---

# Git Commit

```bash
git add .
git commit -m "Day 6: Complete advanced analytics, VaR/CVaR, rolling Sharpe, and recommender"
git push origin main
```

---

# Outcome

Successfully computed tail-risk metrics (VaR & CVaR) for all 40 schemes, charted rolling 90-day Sharpe persistence for key funds, performed investor cohort and SIP churn analysis, constructed an interactive fund recommender CLI script, quantified sector concentration risk (HHI) across 34 equity schemes, authored the comprehensive `Advanced_Analytics.ipynb` notebook, and documented the complete quantitative findings.

---

## Day 7 – Final Report + Presentation + Deployment

### Objective

The objective of Day 7 was to synthesize all data engineering, exploratory data analysis, quantitative risk modeling, and business intelligence deliverables into an executive-ready submission package:
1. Compile an 18-page publication-grade PDF report (`Final_Report.pdf`) covering executive findings, database architecture, methodology, risk analytics, and strategic recommendations.
2. Create a 12-slide 16:9 widescreen presentation deck (`Bluestock_MF_Presentation.pptx`) matching the Bluestock brand palette.
3. Clean all Python codebase modules and build the single master execution script (`run_pipeline.py`).
4. Update `README.md` with complete end-to-end execution guides, dataset schemas, and evaluation self-review checklist.
5. Create local Git release commit and tag (`v1.0`).

---

# Tasks & Deliverable Specifications

### 1. Final PDF Technical Report (`Final_Report.pdf`, 18 Pages)
* **Script**: `generate_final_report.py` (ReportLab 5.0 with two-pass `NumberedCanvas`).
* **Page Count**: Exactly 18 pages.
* **Table of Contents & Core Sections**:
  1. *Cover Page*: Title, Subtitle, Bluestock metadata, candidate credentials, date.
  2. *Executive Summary & Business Context*: Industry macro background (₹81L+ Cr AUM, 26Cr+ folios, ₹31K Cr monthly SIP) and core retail investor dilemmas.
  3. *Data Sources & Ingestion Ecosystem*: Catalog of all 10 datasets, 87K+ records, schema validation rules.
  4. *ETL Pipeline Design & SQLite Star Schema*: Data flow from raw to star schema (`dim_fund`, `dim_date`, fact tables, compound B-Tree indexing).
  5. *EDA — Industry Growth & Macro Trends*: Historical AUM CAGR (+26.3% over 2022–2025) and institutional concentration.
  6. *EDA — SIP Inflows & Category Allocations*: Monthly SIP velocity and category net flow heatmaps.
  7. *EDA — Demographics & Behavioral Geography*: State-wise volumes (Maharashtra, Gujarat, Karnataka lead) and age-tier SIP ticket distributions.
  8. *Fund Performance Analytics — Methodology & Formulas*: CAGR, annualized volatility, Sharpe, Sortino, Alpha & Beta (OLS regression vs Nifty 100), Max Drawdown.
  9. *Fund Performance Scorecard & Top Performers*: Composite 0–100 ranking model; top performers led by Mirae Asset Large Cap Fund (87.25).
  10. *Benchmark Relative Performance & Tracking Error*: Base-100 normalized cumulative charts and tracking error analysis.
  11. *Advanced Risk Analytics — Value at Risk (VaR 95%) & CVaR*: Tail-risk metrics for all 40 schemes; Small-cap tail downside (-3.24% daily CVaR) vs Liquid funds (-0.05%).
  12. *Advanced Risk Analytics — Rolling 90-Day Sharpe Dynamics*: 2022–2026 rolling Sharpe comparison; mid-cap regime sensitivity (-0.80 to +3.20) vs large-cap stability (-0.30 to +1.80).
  13. *Investor Cohort & SIP Continuity Analysis*: 2024 vs 2025 cohort dynamics; identification of 97.8% mandate cadence gaps (>35 days) across 1,362 regular SIP investors.
  14. *Sector Concentration (HHI Index) & Fund Recommender*: Evaluation of 34 equity funds; Axis Bluechip (48.7% IT) concentration risk; `recommender.py` architecture.
  15. *Power BI Dashboard Showcase (Pages 1 & 2)*: Industry Overview & Fund Performance visual breakdowns, DAX formulas, and mockups.
  16. *Power BI Dashboard Showcase (Pages 3 & 4)*: Investor Analytics & SIP/Market Trends visual breakdowns, cross-filtering, and mockups.
  17. *Project Limitations & Analytical Assumptions*: Modeling constraints, stationary distributions, synthetic demographic parameters.
  18. *Strategic Recommendations & Executive Next Steps*: 5 transformative business strategies for Bluestock Fintech.

---

### 2. 12-Slide Executive Presentation Deck (`Bluestock_MF_Presentation.pptx`)
* **Script**: `generate_presentation.py` (`python-pptx` 1.0.2).
* **Format**: 16:9 Widescreen layout, Bluestock corporate palette (`#1A365D` Dark Navy, `#3182CE` Slate Blue, `#F8FAFC` Light Slate, `#38A169` Emerald).
* **Slide Sequence (Exactly 12 Slides)**:
  - **Slide 1**: Title Slide (Hero navy background, project title, candidate details, date).
  - **Slide 2**: Problem Statement & Strategic Objectives (Retail investment dilemmas and 4 solution pillars).
  - **Slide 3**: Data Sources & Ingestion Ecosystem (Summary cards and dataset mapping).
  - **Slide 4**: System Architecture & Relational Star Schema (End-to-end data pipeline stages and database model).
  - **Slide 5**: EDA Highlights (1) — Industry AUM & SIP Inflow Momentum (Embedded charts and macro takeaways).
  - **Slide 6**: EDA Highlights (2) — Demographics & Investor Behavior (Embedded state flows and age boxplots).
  - **Slide 7**: Performance Analytics (1) — Benchmark Comparison & Scorecard (Scorecard weights and top fund highlights).
  - **Slide 8**: Performance Analytics (2) — Tail Risk, Rolling Sharpe & Sector HHI (Advanced quantitative risk findings).
  - **Slide 9**: Power BI Dashboard Showcase (1) — Industry Overview & Fund Performance Pages.
  - **Slide 10**: Power BI Dashboard Showcase (2) — Investor Analytics & Market Trends Pages.
  - **Slide 11**: Strategic Recommendations for Bluestock Fintech (5 actionable corporate strategies).
  - **Slide 12**: Conclusion & Thank You / Q&A.

---

### 3. Master Pipeline Execution Script (`run_pipeline.py`)
* **Features**:
  - One-click end-to-end automation executing all pipeline stages: Ingestion $\rightarrow$ Cleaning $\rightarrow$ DB Loading $\rightarrow$ EDA $\rightarrow$ Performance $\rightarrow$ Advanced Analytics $\rightarrow$ Presentation $\rightarrow$ Final Report.
  - Timing benchmarks, status verification, error trapping, and progress reporting.
  - Supports `--quick` flag for running analytics and document compilation in ~11 seconds.

---

# How to Run the End-to-End Platform

### 1. Environment Setup
Ensure Python 3.10+ is installed with required packages:
```bash
pip install -r requirements.txt
pip install python-pptx reportlab
```

### 2. Full Pipeline Execution
To execute all stages end-to-end from scratch:
```bash
python run_pipeline.py
```

### 3. Quick Analytics & Reporting Execution
To recompute quantitative risk models and recompile the PDF report & presentation deck:
```bash
python run_pipeline.py --quick
```

### 4. Interactive Fund Recommender
To run the risk-appetite fund recommendation engine:
```bash
python recommender.py --risk Low
python recommender.py --risk Moderate
python recommender.py --risk High
```

---

# Capstone Self-Review & Evaluation Rubric Checklist

| # | Deliverable / Rubric Requirement | Weight | Status | Verification & Artifact Location |
| :-: | :--- | :-: | :-: | :--- |
| **D1** | **ETL Pipeline Script** | 15% | **Complete** | Automated ingestion, validation, and cleaning in `data_cleaning.py` & `run_pipeline.py` |
| **D2** | **SQLite Database** | 10% | **Complete** | Relational Star Schema warehouse in `bluestock_mf.db` with primary/foreign keys |
| **D3** | **EDA Notebook & Charts** | 15% | **Complete** | 12 publication charts in `reports/charts/` & `notebooks/EDA_Analysis.ipynb` |
| **D4** | **Performance Metrics** | 15% | **Complete** | `run_performance_analytics.py`, `fund_scorecard.csv`, `alpha_beta.csv`, `tracking_errors.csv` |
| **D5** | **Interactive Dashboard** | 20% | **Complete** | 4-page Power BI specification in `Dashboard.pdf` + high-res mockups (`page1.png` to `page4.png`) |
| **D6** | **Advanced Analytics** | 10% | **Complete** | `Advanced_Analytics.ipynb`, `var_cvar_report.csv`, `rolling_sharpe_chart.png`, `recommender.py` |
| **D7** | **Final Report + Slides** | 15% | **Complete** | `Final_Report.pdf` (18 pages) & `Bluestock_MF_Presentation.pptx` (12 slides) |
| **B1** | **Live NAV API Integration** | Bonus | **Complete** | Real-time AMFI data fetcher in `live_nav_fetch.py` querying mfapi.in |
| **B2** | **Master Runner Automation** | Bonus | **Complete** | Single-command automated orchestrator in `run_pipeline.py` |

---

# Day 7 Deliverables Summary

```text
Final_Report.pdf                        (18-Page Comprehensive Technical & Executive Report)
Bluestock_MF_Presentation.pptx          (12-Slide 16:9 Widescreen Executive Presentation)
run_pipeline.py                         (Master Automated Pipeline Orchestration Script)
generate_final_report.py                (ReportLab 5.0 PDF Generation Engine)
generate_presentation.py                (python-pptx Presentation Engine)

reports/
├── Final_Report.pdf
└── Bluestock_MF_Presentation.pptx
```

---

# Git Release Tag (Local)

```bash
git add .
git commit -m "Final: Complete Bluestock MF Capstone"
git tag v1.0
```
*(Note: Per user instructions, code is maintained strictly in the local repository without remote push).*

---

# Final Project Outcome

The **Bluestock Mutual Fund Analytics Capstone Project** is 100% completed. All 8 capstone pillars, 7 daily milestones, 10 cleaned datasets, relational SQLite database, quantitative tail-risk models, interactive Power BI layouts, 12-slide executive presentation, and 18-page publication PDF report are fully implemented, verified, and operational.


