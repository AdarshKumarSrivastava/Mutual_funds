import pandas as pd
from pathlib import Path

def extract(raw_dir: Path) -> dict:
    """Extract raw CSVs from the data/raw directory."""
    print("--- EXTRACT ---")
    dataframes = {}
    if not raw_dir.exists():
        print(f"Raw directory not found: {raw_dir}")
        return dataframes

    for file in raw_dir.glob("*.csv"):
        try:
            dataframes[file.name] = pd.read_csv(file)
            print(f"Extracted {file.name} with shape {dataframes[file.name].shape}")
        except Exception as e:
            print(f"Error reading {file.name}: {e}")
    return dataframes

def transform(dataframes: dict) -> dict:
    """Clean and transform the extracted dataframes."""
    print("\n--- TRANSFORM ---")
    cleaned_data = {}
    
    for filename, df in dataframes.items():
        if filename == "02_nav_history.csv":
            print(f"Transforming {filename}...")
            # Parse dates
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df = df.dropna(subset=['date'])
            df = df.sort_values(by=['amfi_code', 'date'])
            df = df.drop_duplicates(subset=['amfi_code', 'date'])
            df = df[df['nav'] > 0]
            
            # Forward-fill missing NAV for holidays/weekends
            def fill_missing_dates(group):
                min_date = group['date'].min()
                max_date = group['date'].max()
                if pd.isna(min_date) or pd.isna(max_date):
                    return group
                
                amfi_val = group.name
                if 'amfi_code' in group.columns:
                    group = group.drop(columns=['amfi_code'])
                
                # Create continuous date range covering weekends
                all_dates = pd.date_range(start=min_date, end=max_date, freq='D')
                
                group = group.set_index('date').reindex(all_dates)
                group['amfi_code'] = amfi_val
                group['nav'] = group['nav'].ffill()
                
                return group.rename_axis('date').reset_index()

            df = df.groupby('amfi_code', group_keys=False).apply(fill_missing_dates)
            df = df.dropna(subset=['nav'])
            print(f"  Shape after ffill: {df.shape}")
            cleaned_data[filename] = df

        elif filename == "08_investor_transactions.csv":
            print(f"Transforming {filename}...")
            if 'transaction_date' in df.columns:
                df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')
            if 'transaction_type' in df.columns:
                df['transaction_type'] = df['transaction_type'].str.title().str.strip()
                df['transaction_type'] = df['transaction_type'].replace({'Lump Sum': 'Lumpsum', 'Redeem': 'Redemption', 'Sip': 'SIP'})
            if 'amount_inr' in df.columns:
                df = df[df['amount_inr'] > 0]
            if 'kyc_status' in df.columns:
                df['kyc_status'] = df['kyc_status'].str.title().str.strip()
            cleaned_data[filename] = df
            
        elif filename == "07_scheme_performance.csv":
            print(f"Transforming {filename}...")
            return_cols = ['return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct']
            for col in return_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            if 'expense_ratio_pct' in df.columns:
                df['expense_ratio_pct'] = pd.to_numeric(df['expense_ratio_pct'], errors='coerce')
                # Optional filtering based on expense ratio logic, keeping it simple
            cleaned_data[filename] = df
            
        else:
            # Pass through other files as is
            print(f"Passing through {filename}...")
            cleaned_data[filename] = df

    return cleaned_data

def load(cleaned_data: dict, processed_dir: Path):
    """Load the transformed data into the processed directory."""
    print("\n--- LOAD ---")
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    for filename, df in cleaned_data.items():
        out_path = processed_dir / filename
        try:
            df.to_csv(out_path, index=False)
            print(f"Saved {filename} to {processed_dir}")
        except Exception as e:
            print(f"Failed to save {filename}: {e}")

def run_pipeline():
    base_path = Path(__file__).resolve().parent.parent
    raw_dir = base_path / "data" / "raw"
    processed_dir = base_path / "data" / "processed"
    
    dataframes = extract(raw_dir)
    if not dataframes:
        print("No data extracted. Pipeline stopped.")
        return
        
    cleaned_data = transform(dataframes)
    load(cleaned_data, processed_dir)
    print("\nETL Pipeline completed successfully!")

if __name__ == "__main__":
    run_pipeline()
