"""
Legacy Wrapper: generating_eda.py
Forwarding execution to modular src.analytics.eda.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.analytics.eda import generate_eda_charts

if __name__ == "__main__":
    generate_eda_charts()
