"""
ETL Module: Data Ingestion & Raw Data Inspection
================================================
Inspects and loads raw CSV datasets from data/raw/.
"""

import os
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

def inspect_raw_datasets(data_dir: Path = RAW_DATA_DIR) -> dict:
    """
    Inspects all CSV files in data_dir for shapes, column types, missing values, and duplicates.
    """
    print("\n" + "=" * 80)
    print(f"STAGE 1: Ingesting & Inspecting Raw Datasets from {data_dir}")
    print("=" * 80)
    
    datasets = {}
    csv_files = sorted(list(data_dir.glob("*.csv")))
    
    if not csv_files:
        print(f"[WARNING] No CSV files found in {data_dir}")
        return datasets
        
    for file in csv_files:
        df = pd.read_csv(file)
        datasets[file.name] = df
        null_count = df.isnull().sum().sum()
        dup_count = df.duplicated().sum()
        print(f"  • {file.name:<32} | Shape: {str(df.shape):<14} | Nulls: {null_count:<6} | Duplicates: {dup_count}")
        
    print(f"\n[OK] Successfully ingested and verified {len(datasets)} raw datasets.")
    return datasets

if __name__ == "__main__":
    inspect_raw_datasets()
