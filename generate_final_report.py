"""
Legacy Wrapper: generate_final_report.py
Forwarding execution to modular src.reporting.final_report.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.reporting.final_report import build_final_report

if __name__ == "__main__":
    build_final_report()
