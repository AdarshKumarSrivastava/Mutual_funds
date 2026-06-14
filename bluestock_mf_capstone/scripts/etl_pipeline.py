"""
ETL Pipeline for Bluestock Mutual Fund Capstone.

Handles the extraction of raw CSV data, transformation (including 
forward-filling dates for NAV history to handle weekends/holidays), 
and loading the cleaned data into the processed directory.
"""

import pandas as pd
from pathlib import Path

def extract(raw_dir: Path) -> dict:
    """
    Extract raw CSVs from the specified raw directory.
    
    Args:
        raw_dir (Path): The Path object pointing to the raw data directory.
        
    Returns:
        dict: A dictionary mapping filenames to their respective pandas DataFrames.
    """
    dataframes = {}
    if not raw_dir.exists():
        return dataframes

    for file in raw_dir.glob("*.csv"):
        try:
            dataframes[file.name] = pd.read_csv(file)
        except Exception:
            pass # Silently skip unreadable files in production
            
    return dataframes

def transform(dataframes: dict) -> dict:
    """
    Clean and transform the extracted dataframes based on business rules.
    
    Args:
        dataframes (dict): A dictionary mapping filenames to pandas DataFrames.
        
    Returns:
        dict: A dictionary mapping filenames to cleaned pandas DataFrames.
    """
    cleaned_data = {}
    
    for filename, df in dataframes.items():
        if filename == "02_nav_history.csv":
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df = df.dropna(subset=['date'])
            df = df.sort_values(by=['amfi_code', 'date'])
            df = df.drop_duplicates(subset=['amfi_code', 'date'])
            df = df[df['nav'] > 0]
            
            def fill_missing_dates(group):
                min_date = group['date'].min()
                max_date = group['date'].max()
                if pd.isna(min_date) or pd.isna(max_date):
                    return group
                
                amfi_val = group.name
                if 'amfi_code' in group.columns:
                    group = group.drop(columns=['amfi_code'])
                
                all_dates = pd.date_range(start=min_date, end=max_date, freq='D')
                group = group.set_index('date').reindex(all_dates)
                group['amfi_code'] = amfi_val
                group['nav'] = group['nav'].ffill()
                return group.rename_axis('date').reset_index()

            df = df.groupby('amfi_code', group_keys=False).apply(fill_missing_dates)
            df = df.dropna(subset=['nav'])
            cleaned_data[filename] = df

        elif filename == "08_investor_transactions.csv":
            if 'transaction_date' in df.columns:
                df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')
            if 'transaction_type' in df.columns:
                df['transaction_type'] = df['transaction_type'].str.title().str.strip()
                df['transaction_type'] = df['transaction_type'].replace(
                    {'Lump Sum': 'Lumpsum', 'Redeem': 'Redemption', 'Sip': 'SIP'}
                )
            if 'amount_inr' in df.columns:
                df = df[df['amount_inr'] > 0]
            if 'kyc_status' in df.columns:
                df['kyc_status'] = df['kyc_status'].str.title().str.strip()
            cleaned_data[filename] = df
            
        elif filename == "07_scheme_performance.csv":
            return_cols = ['return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct']
            for col in return_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            if 'expense_ratio_pct' in df.columns:
                df['expense_ratio_pct'] = pd.to_numeric(df['expense_ratio_pct'], errors='coerce')
            cleaned_data[filename] = df
            
        else:
            cleaned_data[filename] = df

    return cleaned_data

def load(cleaned_data: dict, processed_dir: Path):
    """
    Load the transformed data into the processed directory.
    
    Args:
        cleaned_data (dict): Dictionary of cleaned pandas DataFrames.
        processed_dir (Path): The target directory to save the output CSVs.
    """
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    for filename, df in cleaned_data.items():
        out_path = processed_dir / filename
        try:
            df.to_csv(out_path, index=False)
        except Exception:
            pass

def run_pipeline():
    """Execute the full ETL pipeline."""
    base_path = Path(__file__).resolve().parent.parent
    raw_dir = base_path / "data" / "raw"
    processed_dir = base_path / "data" / "processed"
    
    dataframes = extract(raw_dir)
    if not dataframes:
        return
        
    cleaned_data = transform(dataframes)
    load(cleaned_data, processed_dir)

if __name__ == "__main__":
    run_pipeline()
