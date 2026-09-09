"""
Bluestock Mutual Fund Analytics - Simple Fund Recommender CLI
=============================================================
User-facing CLI entrypoint importing from src.analytics.recommender.
Recommends the top 3 mutual funds ranked by Sharpe ratio based on
the user's risk appetite (Low, Moderate, High).

Usage:
    python recommender.py --risk Low
    python recommender.py --risk Moderate
    python recommender.py --risk High
    python recommender.py  (interactive prompt)
"""

import sys
import argparse
from pathlib import Path

# Ensure root directory is on Python path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.analytics.recommender import recommend_funds, print_recommendations

def main():
    parser = argparse.ArgumentParser(description="Bluestock Mutual Fund Recommender based on Risk Profile")
    parser.add_argument(
        "--risk",
        choices=["Low", "Moderate", "High", "low", "moderate", "high"],
        help="Investor risk appetite: Low, Moderate, or High"
    )
    parser.add_argument(
        "--top",
        type=int,
        default=3,
        help="Number of recommendations to return (default: 3)"
    )
    args = parser.parse_args()

    risk_choice = args.risk
    if not risk_choice:
        print("\nWelcome to Bluestock Mutual Fund Recommender!")
        print("Select investor risk appetite:")
        print("  1. Low       (Capital Preservation, Liquid & Fixed Income)")
        print("  2. Moderate  (Balanced Growth, Large Cap & Hybrid)")
        print("  3. High      (Aggressive Wealth Creation, Mid & Small Cap)")
        choice = input("\nEnter choice [1-3 or Low/Moderate/High]: ").strip().lower()
        mapping = {"1": "Low", "2": "Moderate", "3": "High"}
        risk_choice = mapping.get(choice, choice.capitalize())

    try:
        results = recommend_funds(risk_choice, top_n=args.top)
        print_recommendations(risk_choice, results)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
