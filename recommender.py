"""
Bluestock Mutual Fund Analytics - Simple Fund Recommender
=========================================================
Recommends the top 3 mutual funds ranked by Sharpe ratio based on
the user's risk appetite (Low, Moderate, High).

Usage:
    python recommender.py --risk Low
    python recommender.py --risk Moderate
    python recommender.py --risk High
    python recommender.py  (interactive prompt)
"""

import argparse
import os
import pandas as pd

PERFORMANCE_FILE = os.path.join(
    os.path.dirname(__file__), "data", "processed", "07_scheme_performance_clean.csv"
)

# Risk Appetite Mapping to underlying risk_grade values
RISK_MAPPING = {
    "low": ["Low"],
    "moderate": ["Moderate", "Moderately High"],
    "high": ["High", "Very High"]
}

def recommend_funds(risk_appetite: str, top_n: int = 3, data_path: str = PERFORMANCE_FILE) -> pd.DataFrame:
    """
    Filter funds by risk appetite and return the top N funds by Sharpe ratio.
    
    Parameters
    ----------
    risk_appetite : str
        'Low', 'Moderate', or 'High'
    top_n : int, default 3
        Number of recommendations to return
    data_path : str
        Path to the cleaned scheme performance dataset
        
    Returns
    -------
    pd.DataFrame
        Top recommended funds with key metrics
    """
    clean_appetite = risk_appetite.strip().lower()
    if clean_appetite not in RISK_MAPPING:
        valid_options = ", ".join([k.capitalize() for k in RISK_MAPPING.keys()])
        raise ValueError(f"Invalid risk appetite '{risk_appetite}'. Please choose from: {valid_options}")
    
    allowed_grades = RISK_MAPPING[clean_appetite]
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Performance data file not found at: {data_path}")
        
    df = pd.read_csv(data_path)
    
    # Filter matching risk grades
    filtered = df[df["risk_grade"].isin(allowed_grades)].copy()
    
    if filtered.empty:
        return pd.DataFrame()
        
    # Sort strictly by Sharpe ratio descending
    ranked = filtered.sort_values(by="sharpe_ratio", ascending=False).head(top_n)
    
    display_cols = [
        "amfi_code",
        "scheme_name",
        "fund_house",
        "category",
        "plan",
        "sharpe_ratio",
        "return_3yr_pct",
        "std_dev_ann_pct",
        "aum_crore",
        "expense_ratio_pct",
        "risk_grade"
    ]
    
    cols_to_use = [c for c in display_cols if c in ranked.columns]
    return ranked[cols_to_use].reset_index(drop=True)


def print_recommendations(risk_appetite: str, recommendations: pd.DataFrame):
    """Prints a clean ASCII table of recommendations."""
    print("\n" + "=" * 95)
    print(f"  BLUESTOCK MUTUAL FUND RECOMMENDER  |  Risk Appetite: {risk_appetite.upper()}")
    print("=" * 95)
    
    if recommendations.empty:
        print("  No matching funds found.")
        print("=" * 95)
        return
        
    header_fmt = "  {:<4} {:<42} {:<12} {:<8} {:<10} {:<10}"
    row_fmt    = "  {:<4} {:<42} {:<12} {:<8.2f} {:<10.2f} {:<10}"
    
    print(header_fmt.format("Rank", "Scheme Name", "Category", "Sharpe", "3Y CAGR(%)", "Risk Grade"))
    print("  " + "-" * 91)
    
    for i, row in recommendations.iterrows():
        short_name = (row['scheme_name'][:39] + "...") if len(row['scheme_name']) > 42 else row['scheme_name']
        print(row_fmt.format(
            i + 1,
            short_name,
            str(row['category']),
            float(row['sharpe_ratio']),
            float(row.get('return_3yr_pct', 0.0)),
            str(row['risk_grade'])
        ))
        
    print("=" * 95)
    print("  * Metrics sorted by Risk-Adjusted Return (Sharpe Ratio). Risk-free rate assumed at 6.5% p.a.\n")


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
