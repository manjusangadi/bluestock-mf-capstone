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
data/processed/investor_transactions_clean.csv
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
data/processed/scheme_performance_clean.csv
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
fund_master_clean.csv
aum_by_fund_house_clean.csv
monthly_sip_inflows_clean.csv
category_inflows_clean.csv
industry_folio_count_clean.csv
portfolio_holdings_clean.csv
benchmark_indices_clean.csv
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
├── fund_master_clean.csv
├── nav_history_clean.csv
├── aum_by_fund_house_clean.csv
├── monthly_sip_inflows_clean.csv
├── category_inflows_clean.csv
├── industry_folio_count_clean.csv
├── scheme_performance_clean.csv
├── investor_transactions_clean.csv
├── portfolio_holdings_clean.csv
└── benchmark_indices_clean.csv

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
