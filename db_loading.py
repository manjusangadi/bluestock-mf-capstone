"""
Legacy Wrapper: db_loading.py
Forwarding execution to modular src.etl.database.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.etl.database import load_database

if __name__ == "__main__":
    load_database()
