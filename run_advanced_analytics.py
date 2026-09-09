"""
Legacy Wrapper: run_advanced_analytics.py
Forwarding execution to modular src.analytics.advanced.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.analytics.advanced import run_all_advanced_analytics

if __name__ == "__main__":
    run_all_advanced_analytics()
