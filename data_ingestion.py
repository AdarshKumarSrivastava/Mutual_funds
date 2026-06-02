import pandas as pd
import glob
import os

def load_and_summarize_datasets(data_dir="data/raw"):
    csv_files = glob.glob(os.path.join(data_dir, "*.csv"))
    if not csv_files:
        print(f"No CSV files found in {data_dir}")
        return

    print(f"Found {len(csv_files)} CSV files. Loading and summarizing...\n")
    
    for file in csv_files:
        print(f"--- Dataset: {os.path.basename(file)} ---")
        try:
            df = pd.read_csv(file)
            print(f"Shape: {df.shape}")
            print("\nDtypes:")
            print(df.dtypes)
            print("\nHead:")
            print(df.head())
            print("\n" + "="*50 + "\n")
        except Exception as e:
            print(f"Error loading {file}: {e}")

def explore_fund_master(file_path="data/raw/fund_master.csv"):
    if not os.path.exists(file_path):
        print(f"File {file_path} not found. Skipping exploration.")
        return None
    
    print("\n--- Exploring Fund Master ---")
    try:
        df = pd.read_csv(file_path)
        print("Unique Fund Houses:", df['fund_house'].unique() if 'fund_house' in df.columns else "Column not found")
        print("Unique Categories:", df['category'].unique() if 'category' in df.columns else "Column not found")
        print("Unique Sub-Categories:", df['sub_category'].unique() if 'sub_category' in df.columns else "Column not found")
        print("Unique Risk Grades:", df['risk_grade'].unique() if 'risk_grade' in df.columns else "Column not found")
        print("AMFI Scheme Code Structure:", df['scheme_code'].astype(str).str.len().unique() if 'scheme_code' in df.columns else "Column not found")
        return df
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def validate_amfi_codes(fund_master_df, nav_history_path="data/raw/nav_history.csv"):
    if fund_master_df is None or not os.path.exists(nav_history_path):
        print("Missing fund_master dataframe or nav_history.csv to validate AMFI codes.")
        return

    print("\n--- Validating AMFI Codes ---")
    try:
        nav_df = pd.read_csv(nav_history_path)
        if 'scheme_code' not in fund_master_df.columns or 'scheme_code' not in nav_df.columns:
            print("Missing 'scheme_code' column in one of the datasets.")
            return

        master_codes = set(fund_master_df['scheme_code'].unique())
        nav_codes = set(nav_df['scheme_code'].unique())

        missing_in_nav = master_codes - nav_codes
        
        print(f"Total codes in fund_master: {len(master_codes)}")
        print(f"Total codes in nav_history: {len(nav_codes)}")
        print(f"Codes in fund_master but missing in nav_history: {len(missing_in_nav)}")
        
        print("\nData Quality Summary:")
        if len(missing_in_nav) == 0:
            print("All AMFI scheme codes in fund_master exist in nav_history. Validation passed.")
        else:
            print(f"Validation failed. {len(missing_in_nav)} scheme codes are missing in nav_history.")
    except Exception as e:
        print(f"Error during validation: {e}")

if __name__ == "__main__":
    load_and_summarize_datasets()
    fund_master_df = explore_fund_master()
    validate_amfi_codes(fund_master_df)
