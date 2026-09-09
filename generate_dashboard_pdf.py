"""
Legacy Wrapper: generate_dashboard_pdf.py
Forwarding execution to modular src.reporting.dashboard_report.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.reporting.dashboard_report import build_pdf, PDF_PATH_ROOT, PDF_PATH_REPORTS

if __name__ == "__main__":
    build_pdf(PDF_PATH_ROOT)
    build_pdf(PDF_PATH_REPORTS)
