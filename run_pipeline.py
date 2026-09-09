"""
Bluestock Mutual Fund Analytics - Master Pipeline Runner
========================================================
Executes the full capstone analytics and reporting pipeline end-to-end:
1. Live NAV fetch & raw data validation (live_nav_fetch.py)
2. Data cleaning and standardization (data_cleaning.py)
3. SQLite database loading & Star Schema verification (db_loading.py)
4. Exploratory Data Analysis & visual charts (generating_eda.py)
5. Fund performance analytics & scorecard (run_performance_analytics.py)
6. Advanced risk analytics, VaR/CVaR & HHI (run_advanced_analytics.py)
7. 12-Slide PowerPoint presentation (generate_presentation.py)
8. Comprehensive 18-page final PDF report (generate_final_report.py)

Usage:
    python run_pipeline.py           (runs full pipeline end-to-end)
    python run_pipeline.py --quick   (runs analytics and report compilation)
"""

import os
import sys
import time
import subprocess
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PIPELINE_STAGES = [
    ("Live NAV API & Ingestion Check", "live_nav_fetch.py", True),
    ("Data Cleaning & Validation", "data_cleaning.py", True),
    ("SQLite Warehouse Loading", "db_loading.py", True),
    ("Exploratory Data Analysis", "generating_eda.py", True),
    ("Fund Performance Analytics", "run_performance_analytics.py", True),
    ("Advanced Risk Analytics & VaR", "run_advanced_analytics.py", True),
    ("12-Slide Presentation Generation", "generate_presentation.py", True),
    ("Final 18-Page PDF Report Compilation", "generate_final_report.py", True),
]

def run_stage(title: str, script_name: str) -> bool:
    """Executes a single pipeline script with timing and status logging."""
    script_path = os.path.join(BASE_DIR, script_name)
    if not os.path.exists(script_path):
        print(f"  [ERROR] Script not found: {script_name}")
        return False
        
    print("\n" + "=" * 80)
    print(f"  RUNNING STAGE: {title.upper()} ({script_name})")
    print("=" * 80)
    
    start_time = time.time()
    try:
        res = subprocess.run([sys.executable, script_path], cwd=BASE_DIR, check=True)
        elapsed = time.time() - start_time
        print(f"\n  [OK] {title} completed successfully in {elapsed:.2f}s")
        return True
    except subprocess.CalledProcessError as e:
        elapsed = time.time() - start_time
        print(f"\n  [FAIL] {title} failed with exit code {e.returncode} after {elapsed:.2f}s")
        return False
    except Exception as e:
        print(f"\n  [ERROR] {title} encountered unexpected error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Bluestock Capstone Master Pipeline Runner")
    parser.add_argument("--quick", action="store_true", help="Run only analytical calculations and report generators")
    args = parser.parse_args()
    
    print("\n" + "#" * 80)
    print("  BLUESTOCK MUTUAL FUND ANALYTICS CAPSTONE — MASTER PIPELINE EXECUTION")
    print("  Version: 1.0  |  Candidate: Manju Angadi  |  Date: June 2026")
    print("#" * 80)
    
    total_start = time.time()
    stages_to_run = PIPELINE_STAGES
    
    if args.quick:
        # Run stages 5 through 8
        stages_to_run = [s for s in PIPELINE_STAGES if s[1] in [
            "run_performance_analytics.py",
            "run_advanced_analytics.py",
            "generate_presentation.py",
            "generate_final_report.py"
        ]]
        print("  Mode: QUICK EXECUTION (Analytics + Reporting stages)")
    else:
        print("  Mode: FULL END-TO-END PIPELINE (All 8 stages)")
        
    success_count = 0
    failed_stages = []
    
    for title, script_name, _ in stages_to_run:
        ok = run_stage(title, script_name)
        if ok:
            success_count += 1
        else:
            failed_stages.append(title)
            print(f"\n  [WARNING] Pipeline failed at '{title}'. Halting execution.")
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
        print("    - Final_Report.pdf                     (18-page comprehensive report)")
        print("    - Bluestock_MF_Presentation.pptx       (12-slide executive presentation)")
        print("    - bluestock_mf.db                      (Cleaned SQLite Star Schema database)")
        print("    - reports/var_cvar_report.csv          (Historical VaR/CVaR dataset)")
        print("    - reports/charts/                      (All EDA & performance charts)")
        print("=" * 80 + "\n")
    else:
        print(f"\n  [WARNING] Pipeline terminated early due to errors in: {failed_stages}")
        print("=" * 80 + "\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
