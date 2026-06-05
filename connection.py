import sqlite3

conn = sqlite3.connect("bluestock_mf.db")

print("Database Connected")


import sqlite3

conn = sqlite3.connect("bluestock_mf.db")

cursor = conn.cursor()

with open("sql/schema.sql", "r") as file:
    sql_script = file.read()

# cursor.executescript(sql_script)

conn.commit()

print("Tables Created Successfully")

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table';
""")

print(cursor.fetchall())

import pandas as pd

fund_df = pd.read_csv(
    "data/raw/01_fund_master.csv"
)

fund_df.to_sql(
    "dim_fund",
    conn,
    if_exists="append",
    index=False
)

print("Data Loaded")


import sqlite3

conn = sqlite3.connect("bluestock_mf.db")

cursor = conn.cursor()

cursor.execute("SELECT sqlite_version();")

print(cursor.fetchone())


import sqlite3

conn = sqlite3.connect("bluestock_mf.db")

conn.execute("PRAGMA foreign_keys = ON")