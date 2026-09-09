"""
Bluestock Mutual Fund Analytics - Master Modular Pipeline Runner
================================================================
Executes the full capstone analytics and reporting pipeline end-to-end:
1. Live NAV API & Ingestion Check (src.etl.live_nav)
2. Data Cleaning & Validation (src.etl.cleaning)
3. SQLite Warehouse Loading (src.etl.database)
4. Exploratory Data Analysis & Visualizations (src.analytics.eda)
5. Fund Performance Analytics & Scorecard (src.analytics.performance)
6. Advanced Risk Analytics & VaR/CVaR (src.analytics.advanced)
7. 12-Slide PowerPoint Presentation (src.reporting.presentation)
8. Comprehensive 18-Page PDF Report (src.reporting.final_report)

Usage:
    python run_pipeline.py           (runs full pipeline end-to-end)
    python run_pipeline.py --quick   (runs analytics and report compilation)
"""

import sys
import time
import argparse
from pathlib import Path

# Ensure root directory is on Python path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.etl.live_nav import fetch_live_nav
from src.etl.cleaning import clean_all_data
from src.etl.database import load_database
from src.analytics.eda import generate_eda_charts
from src.analytics.performance import compute_performance_analytics
from src.analytics.advanced import run_all_advanced_analytics
from src.reporting.presentation import generate_presentation_deck
from src.reporting.final_report import build_final_report

STAGES = [
    ("Live NAV API Check", fetch_live_nav),
    ("Data Cleaning & Validation", clean_all_data),
    ("SQLite Warehouse Loading", load_database),
    ("Exploratory Data Analysis", generate_eda_charts),
    ("Fund Performance Analytics", compute_performance_analytics),
    ("Advanced Risk Analytics & VaR", run_all_advanced_analytics),
    ("12-Slide Presentation Generation", generate_presentation_deck),
    ("Final 18-Page PDF Report Compilation", build_final_report)
]

def main():
    parser = argparse.ArgumentParser(description="Bluestock Capstone Master Pipeline Runner")
    parser.add_argument("--quick", action="store_true", help="Run only analytical calculations and report generators")
    args = parser.parse_args()

    print("\n" + "#" * 80)
    print("  BLUESTOCK MUTUAL FUND ANALYTICS CAPSTONE — MODULAR PIPELINE EXECUTION")
    print("  Candidate: Manju Angadi  |  Version: 1.0  |  June 2026")
    print("#" * 80)

    stages_to_run = STAGES
    if args.quick:
        stages_to_run = STAGES[4:]
        print("  Mode: QUICK EXECUTION (Analytics + Reporting stages)")
    else:
        print("  Mode: FULL END-TO-END PIPELINE (All 8 stages)")

    total_start = time.time()
    success_count = 0
    failed_stages = []

    for title, func in stages_to_run:
        print("\n" + "=" * 80)
        print(f"  RUNNING STAGE: {title.upper()}")
        print("=" * 80)
        start_t = time.time()
        try:
            func()
            elapsed = time.time() - start_t
            print(f"\n  [OK] {title} completed successfully in {elapsed:.2f}s")
            success_count += 1
        except Exception as e:
            elapsed = time.time() - start_t
            print(f"\n  [ERROR] {title} failed after {elapsed:.2f}s: {e}")
            failed_stages.append(title)
            break

    total_time = time.time() - total_start
    print("\n" + "=" * 80)
    print("  PIPELINE EXECUTION SUMMARY")
    print("=" * 80)
    print(f"  Stages Attempted:  {len(stages_to_run)}")
    print(f"  Stages Succeeded:  {success_count}")
    print(f"  Total Duration:    {total_time:.2f}s")

    if not failed_stages:
        print("\n  *** ALL PIPELINE STAGES COMPLETED SUCCESSFULLY! ***")
        print("  Key Artifacts Generated:")
        print("    - reports/Final_Report.pdf             (18-page comprehensive report)")
        print("    - reports/Bluestock_MF_Presentation.pptx (12-slide executive presentation)")
        print("    - db/bluestock_mf.db                   (Cleaned SQLite Star Schema database)")
        print("    - reports/var_cvar_report.csv          (Historical VaR/CVaR dataset)")
        print("    - reports/charts/                      (All EDA & performance charts)")
        print("=" * 80 + "\n")
    else:
        print(f"\n  [WARNING] Pipeline terminated early due to errors in: {failed_stages}")
        print("=" * 80 + "\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
