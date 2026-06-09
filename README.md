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
