import os
import sqlite3
import pandas as pd
from sqlalchemy import create_engine

# Paths
db_path = "bluestock_mf.db"
processed_dir = "data/processed"
schema_path = "sql/schema.sql"

# Delete existing DB file if it exists to ensure a clean rebuild
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"Removed existing database file: {db_path}")

print("Connecting to SQLite database and applying schema...")
# Create SQLite connection and run schema.sql
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Enable foreign keys
cursor.execute("PRAGMA foreign_keys = ON;")

with open(schema_path, "r", encoding="utf-8") as f:
    sql_script = f.read()

# Execute schema script
cursor.executescript(sql_script)
conn.commit()
print("Database schema applied successfully.")

# Create SQLAlchemy engine for pandas loading
engine = create_engine(f"sqlite:///{db_path}")

# Load all cleaned datasets from data/processed
print("\nReading cleaned CSV files...")
files_to_load = {
    "01_fund_master_clean.csv": "dim_fund",
    "02_nav_history_clean.csv": "fact_nav",
    "03_aum_by_fund_house_clean.csv": "fact_aum",
    "04_monthly_sip_inflows_clean.csv": "monthly_sip_inflows",
    "05_category_inflows_clean.csv": "category_inflows",
    "06_industry_folio_count_clean.csv": "industry_folio_count",
    "07_scheme_performance_clean.csv": "fact_performance",
    "08_investor_transactions_clean.csv": "fact_transactions",
    "09_portfolio_holdings_clean.csv": "portfolio_holdings",
    "10_benchmark_indices_clean.csv": "benchmark_indices"
}

dfs = {}
for filename, table_name in files_to_load.items():
    file_path = os.path.join(processed_dir, filename)
    if os.path.exists(file_path):
        dfs[table_name] = pd.read_csv(file_path)
        print(f"  Loaded {filename} into memory: {dfs[table_name].shape[0]} rows")
    else:
        raise FileNotFoundError(f"Cleaned file not found: {file_path}")

# --- Generate dim_date table ---
print("\nGenerating dim_date dimension...")
# Collect all unique dates across fact tables to find global date range
all_dates = set()

# Fields that contain date strings
date_fields = [
    ("fact_nav", "date"),
    ("fact_transactions", "transaction_date"),
    ("fact_aum", "date"),
    ("portfolio_holdings", "portfolio_date"),
    ("benchmark_indices", "date")
]

for table_name, col_name in date_fields:
    if table_name in dfs and col_name in dfs[table_name].columns:
        dates = dfs[table_name][col_name].dropna().unique()
        all_dates.update(dates)

# Also check dim_fund launch dates to see if they should be in range
if "dim_fund" in dfs and "launch_date" in dfs["dim_fund"].columns:
    # Launch dates can go back to 2000 or earlier, let's include them to prevent join mismatch
    # (though they aren't FKs, it's good to cover them)
    dates = dfs["dim_fund"]["launch_date"].dropna().unique()
    all_dates.update(dates)

# Filter out empty or null strings
all_dates = {d for d in all_dates if str(d).strip()}

all_dates_dt = pd.to_datetime(list(all_dates))
min_date = all_dates_dt.min()
max_date = all_dates_dt.max()
print(f"  Min date: {min_date.strftime('%Y-%m-%d')}, Max date: {max_date.strftime('%Y-%m-%d')}")

# Create continuous date range from min to max
full_date_range = pd.date_range(start=min_date, end=max_date, freq="D")
dim_date_df = pd.DataFrame({"date": full_date_range})

# Extract calendar attributes
dim_date_df["year"] = dim_date_df["date"].dt.year
dim_date_df["month"] = dim_date_df["date"].dt.month
dim_date_df["month_name"] = dim_date_df["date"].dt.strftime("%B")
dim_date_df["quarter"] = dim_date_df["date"].dt.quarter
dim_date_df["day"] = dim_date_df["date"].dt.day
dim_date_df["day_of_week"] = dim_date_df["date"].dt.dayofweek # 0 (Mon) to 6 (Sun)
dim_date_df["day_name"] = dim_date_df["date"].dt.strftime("%A")
dim_date_df["is_weekend"] = dim_date_df["day_of_week"].apply(lambda x: 1 if x >= 5 else 0)

# Format the date key column as YYYY-MM-DD
dim_date_df["date"] = dim_date_df["date"].dt.strftime("%Y-%m-%d")

print(f"  Generated dim_date with {len(dim_date_df)} calendar days.")

# --- Load tables to database ---
# We load dim_date first to satisfy FK dependencies
print("\nLoading dim_date to database...")
dim_date_df.to_sql("dim_date", con=engine, if_exists="append", index=False)
print("  Loaded dim_date successfully.")

# Define loading order to handle foreign key dependencies (dimensions first, then facts)
loading_order = [
    "dim_fund",
    "fact_nav",
    "fact_performance",
    "fact_transactions",
    "fact_aum",
    "monthly_sip_inflows",
    "category_inflows",
    "industry_folio_count",
    "portfolio_holdings",
    "benchmark_indices"
]

print("\nLoading CSV DataFrames into SQLite tables...")
# Re-enable PRAGMA foreign_keys on the engine connections
with engine.connect() as con:
    con.exec_driver_sql("PRAGMA foreign_keys = ON;")

for table_name in loading_order:
    df = dfs[table_name]
    print(f"  Loading table '{table_name}' ({len(df)} rows)...")
    # Using 'append' to load into schema created by schema.sql
    df.to_sql(table_name, con=engine, if_exists="append", index=False)

print("\n--- Verifying Row Counts ---")
# Query SQLite system to check row counts
cursor = conn.cursor()
verification_results = []
all_matched = True

for table_name in loading_order:
    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
    db_count = cursor.fetchone()[0]
    csv_count = len(dfs[table_name])
    status = "MATCHED" if db_count == csv_count else "MISMATCH"
    
    if db_count != csv_count:
        all_matched = False
        
    verification_results.append({
        "Table": table_name,
        "CSV Rows": csv_count,
        "DB Rows": db_count,
        "Status": status
    })

# Format and print the row count verification table
verification_df = pd.DataFrame(verification_results)
print(verification_df.to_string(index=False))

# Verify dim_date count
cursor.execute("SELECT COUNT(*) FROM dim_date;")
print(f"\n  dim_date Rows in DB: {cursor.fetchone()[0]}")

# Close connection
conn.close()

if all_matched:
    print("\nSUCCESS: All loaded table row counts match their source CSV files!")
else:
    print("\nWARNING: Some table row counts do not match their source CSV files!")


import sqlite3

conn = sqlite3.connect("bluestock_mf.db")

conn.execute("PRAGMA foreign_keys = ON")