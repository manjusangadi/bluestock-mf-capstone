"""
ETL Module: SQLite Star Schema Database Loader
==============================================
Builds and populates db/bluestock_mf.db from cleaned datasets.
"""

import os
import sqlite3
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DB_DIR = PROJECT_ROOT / "db"
DB_PATH = DB_DIR / "bluestock_mf.db"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
SCHEMA_PATH = PROJECT_ROOT / "sql" / "schema.sql"

def load_database(db_file: Path = DB_PATH, processed_path: Path = PROCESSED_DIR, schema_file: Path = SCHEMA_PATH) -> bool:
    """
    Applies DDL schema and loads all cleaned tables into SQLite database.
    """
    os.makedirs(db_file.parent, exist_ok=True)
    print("\n" + "=" * 80)
    print(f"STAGE 3: Initializing SQLite Warehouse at {db_file}")
    print("=" * 80)

    conn = sqlite3.connect(str(db_file))
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    if schema_file.exists():
        with open(schema_file, "r", encoding="utf-8") as f:
            cursor.executescript(f.read())
        conn.commit()
        print("  [OK] Applied schema.sql successfully.")
    else:
        print(f"  [WARNING] Schema file not found at {schema_file}, proceeding with auto-table generation.")

    engine = create_engine(f"sqlite:///{db_file}")

    table_mapping = {
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

    loaded_tables = 0
    for filename, table_name in table_mapping.items():
        fpath = processed_path / filename
        if fpath.exists():
            df = pd.read_csv(fpath)
            df.to_sql(table_name, engine, if_exists="replace", index=False)
            print(f"  [OK] Loaded table '{table_name}': {len(df):,} rows")
            loaded_tables += 1

    # Also build dim_date
    nav_path = processed_path / "02_nav_history_clean.csv"
    if nav_path.exists():
        df_nav = pd.read_csv(nav_path)
        unique_dates = pd.to_datetime(df_nav['date']).drop_duplicates().sort_values()
        dim_date = pd.DataFrame({
            'date': unique_dates.dt.strftime('%Y-%m-%d'),
            'year': unique_dates.dt.year,
            'quarter': unique_dates.dt.quarter,
            'month': unique_dates.dt.month,
            'month_name': unique_dates.dt.strftime('%B'),
            'day': unique_dates.dt.day,
            'day_name': unique_dates.dt.strftime('%A'),
            'is_weekend': unique_dates.dt.dayofweek.isin([5, 6]).astype(int)
        })
        dim_date.to_sql("dim_date", engine, if_exists="replace", index=False)
        print(f"  [OK] Built 'dim_date' dimension: {len(dim_date):,} dates")

    conn.close()
    
    # Sync fallback copy to root if needed
    root_db = PROJECT_ROOT / "bluestock_mf.db"
    try:
        import shutil
        shutil.copy2(db_file, root_db)
    except Exception:
        pass

    print(f"\n[OK] SQLite Database Warehouse ready with {loaded_tables} relational tables.")
    return True

if __name__ == "__main__":
    load_database()
