"""
Legacy Wrapper: run_performance_analytics.py
Forwarding execution to modular src.analytics.performance.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.analytics.performance import compute_performance_analytics

if __name__ == "__main__":
    compute_performance_analytics()
