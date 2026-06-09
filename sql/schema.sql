
-- schema.sql
-- Star Schema Database Structure for Mutual Fund Capstone Project

-- Enable foreign keys (must be run on connection in SQLite)

-- Drop tables if they exist to allow clean recreations
DROP TABLE IF EXISTS benchmark_indices;
DROP TABLE IF EXISTS portfolio_holdings;
DROP TABLE IF EXISTS industry_folio_count;
DROP TABLE IF EXISTS category_inflows;
DROP TABLE IF EXISTS monthly_sip_inflows;
DROP TABLE IF EXISTS fact_aum;
DROP TABLE IF EXISTS fact_transactions;
DROP TABLE IF EXISTS fact_performance;
DROP TABLE IF EXISTS fact_nav;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS dim_fund;

-- 1. dim_fund Table
CREATE TABLE dim_fund (
    amfi_code INTEGER PRIMARY KEY,
    fund_house TEXT NOT NULL,
    scheme_name TEXT NOT NULL,
    category TEXT NOT NULL,
    sub_category TEXT NOT NULL,
    plan TEXT NOT NULL,
    launch_date TEXT,
    benchmark TEXT,
    expense_ratio_pct REAL,
    exit_load_pct REAL,
    min_sip_amount REAL,
    min_lumpsum_amount REAL,
    fund_manager TEXT,
    risk_category TEXT,
    sebi_category_code TEXT
);

-- 2. dim_date Table
CREATE TABLE dim_date (
    date TEXT PRIMARY KEY, -- YYYY-MM-DD format
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    month_name TEXT NOT NULL,
    quarter INTEGER NOT NULL,
    day INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL, -- 0 (Mon) to 6 (Sun)
    day_name TEXT NOT NULL,
    is_weekend INTEGER NOT NULL -- 0 = False, 1 = True
);

-- 3. fact_nav Table
CREATE TABLE fact_nav (
    amfi_code INTEGER NOT NULL,
    date TEXT NOT NULL,
    nav REAL NOT NULL,
    PRIMARY KEY (amfi_code, date),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund (amfi_code) ON DELETE CASCADE,
    FOREIGN KEY (date) REFERENCES dim_date (date) ON DELETE CASCADE
);

-- 4. fact_performance Table
CREATE TABLE fact_performance (
    amfi_code INTEGER PRIMARY KEY,
    scheme_name TEXT,
    fund_house TEXT,
    category TEXT,
    plan TEXT,
    return_1yr_pct REAL,
    return_3yr_pct REAL,
    return_5yr_pct REAL,
    benchmark_3yr_pct REAL,
    alpha REAL,
    beta REAL,
    sharpe_ratio REAL,
    sortino_ratio REAL,
    std_dev_ann_pct REAL,
    max_drawdown_pct REAL,
    aum_crore REAL,
    expense_ratio_pct REAL,
    morningstar_rating INTEGER,
    risk_grade TEXT,
    anomaly_flag INTEGER,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund (amfi_code) ON DELETE CASCADE
);



-- 5. fact_transactions Table
CREATE TABLE fact_transactions (
    transaction_id INTEGER PRIMARY KEY ,
    investor_id TEXT NOT NULL,
    transaction_date TEXT NOT NULL,
    amfi_code INTEGER NOT NULL,
    transaction_type TEXT NOT NULL,
    amount_inr REAL NOT NULL,
    state TEXT,
    city TEXT,
    city_tier TEXT,
    age_group TEXT,
    gender TEXT,
    annual_income_lakh REAL,
    payment_mode TEXT,
    kyc_status TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund (amfi_code) ON DELETE CASCADE,
    FOREIGN KEY (transaction_date) REFERENCES dim_date (date) ON DELETE CASCADE
);


-- 6. fact_aum Table
CREATE TABLE fact_aum (
    aum_id INTEGER PRIMARY KEY ,
    date TEXT NOT NULL,
    fund_house TEXT NOT NULL,
    aum_lakh_crore REAL,
    aum_crore REAL,
    num_schemes INTEGER,
    FOREIGN KEY (date) REFERENCES dim_date (date) ON DELETE CASCADE
);



-- 7. monthly_sip_inflows Table
CREATE TABLE monthly_sip_inflows (
    month TEXT PRIMARY KEY, -- YYYY-MM
    sip_inflow_crore REAL,
    active_sip_accounts_crore REAL,
    new_sip_accounts_lakh REAL,
    sip_aum_lakh_crore REAL,
    yoy_growth_pct REAL
);

-- 8. category_inflows Table
CREATE TABLE category_inflows (
    category_inflow_id INTEGER PRIMARY KEY ,
    month TEXT NOT NULL,
    category TEXT NOT NULL,
    net_inflow_crore REAL,
    inet_inflow_crore TEXT
);

-- 9. industry_folio_count Table
CREATE TABLE industry_folio_count (
    month TEXT PRIMARY KEY, -- YYYY-MM
    total_folios_crore REAL,
    equity_folios_crore REAL,
    debt_folios_crore REAL,
    hybrid_folios_crore REAL,
    others_folios_crore REAL
);

-- 10. portfolio_holdings Table
CREATE TABLE portfolio_holdings (
    holding_id INTEGER PRIMARY KEY ,
    amfi_code INTEGER NOT NULL,
    stock_symbol TEXT NOT NULL,
    stock_name TEXT NOT NULL,
    sector TEXT NOT NULL,
    weight_pct REAL NOT NULL,
    market_value_cr REAL NOT NULL,
    current_price_inr REAL NOT NULL,
    portfolio_date TEXT NOT NULL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund (amfi_code) ON DELETE CASCADE,
    FOREIGN KEY (portfolio_date) REFERENCES dim_date (date) ON DELETE CASCADE
);

-- 11. benchmark_indices Table
CREATE TABLE benchmark_indices (
    benchmark_index_id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    index_name TEXT NOT NULL,
    close_value REAL NOT NULL,
    FOREIGN KEY (date) REFERENCES dim_date (date) ON DELETE CASCADE
);

