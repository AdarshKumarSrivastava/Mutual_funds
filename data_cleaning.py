import pandas as pd
import os
import glob

def clean_data(raw_dir="data/raw", processed_dir="data/processed"):
    os.makedirs(processed_dir, exist_ok=True)
    
    # 1. Clean Fund Master
    fund_master_path = os.path.join(raw_dir, "01_fund_master.csv")
    if os.path.exists(fund_master_path):
        df_fund = pd.read_csv(fund_master_path)
        # Convert launch_date to datetime
        if 'launch_date' in df_fund.columns:
            df_fund['launch_date'] = pd.to_datetime(df_fund['launch_date'], errors='coerce')
        # Fill missing values
        df_fund.fillna({
            'expense_ratio_pct': df_fund['expense_ratio_pct'].median() if 'expense_ratio_pct' in df_fund.columns else 0.0,
            'exit_load_pct': 0.0
        }, inplace=True)
        df_fund.to_csv(os.path.join(processed_dir, "01_fund_master_cleaned.csv"), index=False)
        print("Cleaned 01_fund_master.csv")

    # 2. Clean NAV History
    nav_history_path = os.path.join(raw_dir, "02_nav_history.csv")
    if os.path.exists(nav_history_path):
        df_nav = pd.read_csv(nav_history_path)
        if 'date' in df_nav.columns:
            df_nav['date'] = pd.to_datetime(df_nav['date'], errors='coerce')
        df_nav.dropna(subset=['nav', 'date'], inplace=True)
        df_nav.to_csv(os.path.join(processed_dir, "02_nav_history_cleaned.csv"), index=False)
        print("Cleaned 02_nav_history.csv")

    # 3. Clean Investor Transactions
    investor_path = os.path.join(raw_dir, "08_investor_transactions.csv")
    if os.path.exists(investor_path):
        df_inv = pd.read_csv(investor_path)
        if 'transaction_date' in df_inv.columns:
            df_inv['transaction_date'] = pd.to_datetime(df_inv['transaction_date'], errors='coerce')
        df_inv.to_csv(os.path.join(processed_dir, "08_investor_transactions_cleaned.csv"), index=False)
        print("Cleaned 08_investor_transactions.csv")

    # Process all other remaining CSVs by just copying them over to processed with simple cleaning
    all_files = glob.glob(os.path.join(raw_dir, "*.csv"))
    skip_files = ["01_fund_master.csv", "02_nav_history.csv", "08_investor_transactions.csv"]
    
    for file in all_files:
        filename = os.path.basename(file)
        if filename not in skip_files:
            try:
                df = pd.read_csv(file)
                # Apply basic date parsing if 'date' column exists
                if 'date' in df.columns:
                    df['date'] = pd.to_datetime(df['date'], errors='coerce')
                
                out_name = filename.replace(".csv", "_cleaned.csv")
                df.to_csv(os.path.join(processed_dir, out_name), index=False)
                print(f"Cleaned {filename}")
            except Exception as e:
                print(f"Failed to clean {filename}: {e}")

if __name__ == "__main__":
    print("Starting Data Cleaning Process...")
    clean_data()
    print("Data Cleaning Complete.")
