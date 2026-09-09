"""
ETL Module: Live NAV Fetcher (mfapi.in REST API)
================================================
Fetches real-time mutual fund valuation data from mfapi.in API.
"""

from pathlib import Path
import requests
import json

DEFAULT_AMFI_CODE = 119551  # SBI Bluechip Fund - Regular Plan

def fetch_live_nav(amfi_code: int = DEFAULT_AMFI_CODE) -> dict:
    """
    Fetches real-time NAV and scheme metadata from mfapi.in.
    """
    url = f"https://api.mfapi.in/mf/{amfi_code}"
    print(f"Fetching live NAV for AMFI scheme code: {amfi_code} ...")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        meta = data.get("meta", {})
        nav_history = data.get("data", [])
        latest_record = nav_history[0] if nav_history else {}
        
        print(f"  [OK] Scheme:     {meta.get('scheme_name')}")
        print(f"  [OK] Fund House: {meta.get('fund_house')}")
        print(f"  [OK] Latest NAV: Rs. {latest_record.get('nav')} (Date: {latest_record.get('date')})")
        return {
            "amfi_code": amfi_code,
            "scheme_name": meta.get("scheme_name"),
            "fund_house": meta.get("fund_house"),
            "latest_nav": latest_record.get("nav"),
            "latest_date": latest_record.get("date")
        }
    except Exception as e:
        print(f"  [WARNING] Could not fetch live NAV from API: {e}")
        return {}

if __name__ == "__main__":
    fetch_live_nav()
