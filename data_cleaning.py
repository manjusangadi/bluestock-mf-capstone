"""
Legacy Wrapper: data_cleaning.py
Forwarding execution to modular src.etl.cleaning.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.etl.cleaning import clean_all_data

if __name__ == "__main__":
    clean_all_data()
