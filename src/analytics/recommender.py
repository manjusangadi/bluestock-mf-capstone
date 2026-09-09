"""
Analytics Module: Simple Fund Recommender Engine
================================================
Recommends mutual funds ranked by Sharpe ratio based on investor risk appetite.
"""

from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PERF_FILE = PROJECT_ROOT / "data" / "processed" / "07_scheme_performance_clean.csv"

RISK_MAPPING = {
    "low": ["Low"],
    "moderate": ["Moderate", "Moderately High"],
    "high": ["High", "Very High"]
}

def recommend_funds(risk_appetite: str, top_n: int = 3, data_path: Path = PERF_FILE) -> pd.DataFrame:
    """
    Filters funds by risk appetite and returns the top N funds by Sharpe ratio.
    """
    key = risk_appetite.strip().lower()
    if key not in RISK_MAPPING:
        valid_options = ", ".join([k.capitalize() for k in RISK_MAPPING.keys()])
        raise ValueError(f"Invalid risk appetite '{risk_appetite}'. Choose from: {valid_options}")
        
    allowed_grades = RISK_MAPPING[key]
    if not data_path.exists():
        raise FileNotFoundError(f"Performance data file not found at: {data_path}")
        
    df = pd.read_csv(data_path)
    filtered = df[df["risk_grade"].isin(allowed_grades)].copy()
    if filtered.empty:
        return pd.DataFrame()
        
    ranked = filtered.sort_values(by="sharpe_ratio", ascending=False).head(top_n)
    display_cols = [
        "amfi_code", "scheme_name", "fund_house", "category", "plan",
        "sharpe_ratio", "return_3yr_pct", "std_dev_ann_pct", "aum_crore", "expense_ratio_pct", "risk_grade"
    ]
    cols = [c for c in display_cols if c in ranked.columns]
    return ranked[cols].reset_index(drop=True)

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
    print("=" * 95 + "\n")

if __name__ == "__main__":
    df = recommend_funds("Moderate")
    print_recommendations("Moderate", df)
