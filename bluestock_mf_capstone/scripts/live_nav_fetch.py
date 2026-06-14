"""
Live NAV Fetch Script for Bluestock Mutual Fund Capstone.

Runs a continuous background loop to fetch live NAV data from mfapi.in
every weekday at 8 PM, avoiding external schedule libraries.
"""

import requests
import pandas as pd
from pathlib import Path
import time
from datetime import datetime
import subprocess

def fetch_nav(scheme_code: int, save_path: Path) -> pd.DataFrame:
    """
    Fetch NAV data from the mfapi.in API and save it locally.
    
    Args:
        scheme_code (int): AMFI code for the mutual fund.
        save_path (Path): Path destination for the CSV output.
        
    Returns:
        pd.DataFrame or None: Extracted dataframe, or None if the request fails.
    """
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        nav_data = data.get("data", [])
        df = pd.DataFrame(nav_data)
        if save_path:
            save_path.parent.mkdir(exist_ok=True, parents=True)
            df.to_csv(save_path, index=False)
        return df
    return None

def job():
    """
    Executes the fetching job for key mutual fund schemes, then triggers 
    the ETL pipeline to update downstream datasets.
    """
    base_path = Path(__file__).resolve().parent.parent / "data" / "raw"
    key_schemes = {
        "SBI Bluechip": 119551,
        "ICICI Bluechip": 120503,
        "Nippon Large Cap": 118632,
        "Axis Bluechip": 119092,
        "Kotak Bluechip": 120841,
        "HDFC Top 100": 125497
    }

    for name, code in key_schemes.items():
        save_path = base_path / f"{name.replace(' ', '_').lower()}_{code}.csv"
        fetch_nav(code, save_path)
    
    # Run the ETL pipeline automatically
    subprocess.run(["python", str(Path(__file__).resolve().parent / "etl_pipeline.py")], check=False)

if __name__ == "__main__":
    while True:
        now = datetime.now()
        # Check if it's a weekday (0=Monday, 4=Friday) and time is 20:00 (8 PM)
        if now.weekday() < 5 and now.hour == 20 and now.minute == 0:
            job()
            # Sleep for 61 seconds to avoid running multiple times in the same minute
            time.sleep(61)
        else:
            time.sleep(60)
