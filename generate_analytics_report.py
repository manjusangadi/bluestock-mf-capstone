"""
Legacy Wrapper: generate_analytics_report.py
Forwarding execution to modular src.reporting.day4_report.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.reporting.day4_report import build_pdf

if __name__ == "__main__":
    build_pdf()
