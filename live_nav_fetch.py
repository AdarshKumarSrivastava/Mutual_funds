import requests
import pandas as pd
import os

def fetch_nav(scheme_code, save_path=None):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        nav_data = data.get("data", [])
        df = pd.DataFrame(nav_data)
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            df.to_csv(save_path, index=False)
            print(f"Saved NAV data for scheme {scheme_code} to {save_path}")
        return df
    else:
        print(f"Failed to fetch data for scheme {scheme_code}")
        return None

if __name__ == "__main__":
    # Fetch live NAV for HDFC Top 100 Direct
    fetch_nav(125497, "data/raw/hdfc_top_100_direct_125497.csv")

    # Key schemes to fetch
    key_schemes = {
        "SBI Bluechip": 119551,
        "ICICI Bluechip": 120503,
        "Nippon Large Cap": 118632,
        "Axis Bluechip": 119092,
        "Kotak Bluechip": 120841
    }

    for name, code in key_schemes.items():
        print(f"Fetching {name} ({code})...")
        fetch_nav(code, f"data/raw/{name.replace(' ', '_').lower()}_{code}.csv")
