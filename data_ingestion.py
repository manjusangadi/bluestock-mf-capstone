import pandas as pd
from pathlib import Path

# Folder containing CSV files
data_path = Path("data/raw")

# Read all CSV files
for file in data_path.glob("*.csv"):

    print("\n" + "="*60)
    print("\n FILE:", file.name)
    print("\n" + "="*60)

    # Load dataset
    df = pd.read_csv(file)

    # Shape
    print("\nSHAPE:")
    print(df.shape)

    # Data Types
    print("\nDATA TYPES:")
    print(df.dtypes)

    # First 5 Rows
    print("\nFIRST 5 ROWS:")
    print(df.head())

    # Missing Values
    print("\nMISSING VALUES:")
    print(df.isnull().sum())

    # Duplicate Records
    print("\nDUPLICATE RECORDS:")
    print(df.duplicated().sum())



# ============================================================

#                 Explore fund master 

# ============================================================

import pandas as pd

fund_master = pd.read_csv('data/raw/01_fund_master.csv')

print(fund_master.head())

print(fund_master.columns)

print(fund_master['fund_house'].unique())

print(fund_master["category"].unique())

print(
    fund_master["sub_category"].unique()
)

print(
    fund_master["category"]
    .value_counts()
)

print(
    fund_master[
        ["amfi_code",
         "scheme_name"]
    ].head()
)

with open("reports/fund_master_summary.txt","w",encoding="utf-8") as f:

    f.write("\n" + "="*60 + "\n")

    f.write("\n Explore fund master \n")

    f.write("\n" + "="*60 + "\n")
    f.write(
        str(
            fund_master["fund_house"]
            .unique()
        )
    )

    f.write("\n\nCategories\n")
    f.write(
        str(
            fund_master["category"]
            .unique()
        )
    )

    f.write("\n\nSub Categories\n")
    f.write(
        str(
            fund_master["sub_category"]
            .unique()
        )
    )

    f.write("\n\nRisk Grades\n")
    f.write(
        str(
            fund_master["risk_category"]
            .unique()
        )
    )

# ============================================================

#                     VALIDATE AMFI CODES

# ============================================================

import pandas as pd

fund_master = pd.read_csv(
    "data/raw/01_fund_master.csv"
)

nav_history = pd.read_csv(
    "data/raw/02_nav_history.csv"
)


#  Check Column Names
print(fund_master.columns)

print(nav_history.columns)

#  Create Sets of AMFI Codes
master_codes = set(
    fund_master["amfi_code"]
)

nav_codes = set(
    nav_history["amfi_code"]
)
print(master_codes)
print(nav_codes)

missing_codes = (master_codes - nav_codes)
print(missing_codes)
# if result shows set() means All AMFI codes exist in nav_history.


#  Count Total Codes
print(
    "Fund Master Codes:",
    len(master_codes)
)

print(
    "NAV History Codes:",
    len(nav_codes)
)

#write data to file
with open("reports/amfi_validation.txt","w",encoding="utf-8") as f:

    f.write(
        f"Fund Master Codes: {len(master_codes)}\n"
    )

    f.write(
        f"NAV History Codes: {len(nav_codes)}\n\n"
    )

    if len(missing_codes) == 0:

        f.write(
            "Validation Successful\n"
        )

        f.write(
            "All AMFI codes exist in NAV history."
        )

    else:

        f.write(
            "Missing Codes:\n"
        )

        f.write(
            str(missing_codes)
        )
# -----------------------------
# DATA QUALITY SUMMARY
# -----------------------------

dfs = {}
summary_lines = []

def log_and_print(text=""):
    print(text)
    summary_lines.append(text)

log_and_print("\nDATA QUALITY SUMMARY")
log_and_print("=" * 50)

for filename, df in dfs.items():

    log_and_print(f"\nDataset: {filename}")

    # Shape
    log_and_print(f"Rows: {df.shape[0]}")
    log_and_print(f"Columns: {df.shape[1]}")

    # Missing values
    missing_values = df.isnull().sum().sum()
    log_and_print(f"Missing Values: {missing_values}")

    # Duplicate rows
    duplicates = df.duplicated().sum()
    log_and_print(f"Duplicate Rows: {duplicates}")

# AMFI Validation
log_and_print("\nAMFI CODE VALIDATION")
log_and_print("-" * 50)

master_codes = set(fund_master["amfi_code"])
nav_codes = set(nav_history["amfi_code"])

missing_codes = master_codes - nav_codes

if len(missing_codes) == 0:
    log_and_print("All AMFI codes are present in NAV history.")
else:
    log_and_print(f"Missing AMFI Codes: {missing_codes}")


        