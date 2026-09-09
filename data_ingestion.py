"""
Legacy Wrapper: data_ingestion.py
Forwarding execution to modular src.etl.ingestion.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.etl.ingestion import inspect_raw_datasets

if __name__ == "__main__":
    inspect_raw_datasets()
