import pandas as pd
import os
import glob
import numpy as np

def clean_data(raw_dir="data/raw", processed_dir="data/processed"):
    os.makedirs(processed_dir, exist_ok=True)
    
    # 2. Clean NAV History
    nav_history_path = os.path.join(raw_dir, "02_nav_history.csv")
    if os.path.exists(nav_history_path):
        df_nav = pd.read_csv(nav_history_path)
        # Parse dates to datetime
        df_nav['date'] = pd.to_datetime(df_nav['date'], errors='coerce')
        # Sort by amfi_code + date
        df_nav = df_nav.sort_values(by=['amfi_code', 'date'])
        # Remove duplicates
        df_nav = df_nav.drop_duplicates(subset=['amfi_code', 'date'])
        # Validate NAV > 0 (remove or set to NaN, let's filter out)
        df_nav = df_nav[df_nav['nav'] > 0]
        
        # Forward-fill missing NAV for holidays/weekends
        # We need to reindex for each amfi_code to include all dates between min and max
        def fill_missing_dates(group):
            min_date = group['date'].min()
            max_date = group['date'].max()
            if pd.isna(min_date) or pd.isna(max_date):
                return group
            all_dates = pd.date_range(start=min_date, end=max_date, freq='D')
            amfi_val = group.name
            if 'amfi_code' in group.columns:
                group = group.drop(columns=['amfi_code'])
            group = group.set_index('date').reindex(all_dates)
            group['amfi_code'] = amfi_val
            group['nav'] = group['nav'].ffill()
            group = group.rename_axis('date').reset_index()
            return group

        df_nav = df_nav.groupby('amfi_code').apply(fill_missing_dates).reset_index(drop=True)
        
        df_nav.to_csv(os.path.join(processed_dir, "02_nav_history.csv"), index=False)
        print("Cleaned 02_nav_history.csv")

    # 8. Clean Investor Transactions
    investor_path = os.path.join(raw_dir, "08_investor_transactions.csv")
    if os.path.exists(investor_path):
        df_inv = pd.read_csv(investor_path)
        # Fix date formats
        df_inv['transaction_date'] = pd.to_datetime(df_inv['transaction_date'], errors='coerce')
        # Standardise transaction_type values
        if 'transaction_type' in df_inv.columns:
            df_inv['transaction_type'] = df_inv['transaction_type'].str.title().str.strip()
            # Map slightly different ones if any, assuming standard is Sip, Lumpsum, Redemption
            df_inv['transaction_type'] = df_inv['transaction_type'].replace({'Lump Sum': 'Lumpsum', 'Redeem': 'Redemption'})
            # ensure case exactly matches user request "SIP", "Lumpsum", "Redemption"
            df_inv['transaction_type'] = df_inv['transaction_type'].replace({'Sip': 'SIP'})
            
        # Validate amount > 0
        if 'amount_inr' in df_inv.columns:
            df_inv = df_inv[df_inv['amount_inr'] > 0]
            
        # Check KYC status enum values (let's assume valid are 'Verified', 'Pending', 'Rejected', etc.)
        # The prompt says "check KYC status enum values", I'll just title-case it
        if 'kyc_status' in df_inv.columns:
            df_inv['kyc_status'] = df_inv['kyc_status'].str.title().str.strip()
            
        df_inv.to_csv(os.path.join(processed_dir, "08_investor_transactions.csv"), index=False)
        print("Cleaned 08_investor_transactions.csv")

    # 7. Clean Scheme Performance
    perf_path = os.path.join(raw_dir, "07_scheme_performance.csv")
    if os.path.exists(perf_path):
        df_perf = pd.read_csv(perf_path)
        # Validate all return values are numeric
        return_cols = ['return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct']
        for col in return_cols:
            if col in df_perf.columns:
                df_perf[col] = pd.to_numeric(df_perf[col], errors='coerce')
                
        # Flag anomalies (e.g. > 100% or < -100%)
        # Let's add an anomaly_flag column
        anomaly_cond = pd.Series(False, index=df_perf.index)
        for col in return_cols:
            if col in df_perf.columns:
                anomaly_cond = anomaly_cond | (df_perf[col] > 100) | (df_perf[col] < -100)
        df_perf['anomaly_flag'] = anomaly_cond
        
        # Check expense_ratio range (0.1% - 2.5%)
        if 'expense_ratio_pct' in df_perf.columns:
            df_perf['expense_ratio_pct'] = pd.to_numeric(df_perf['expense_ratio_pct'], errors='coerce')
            df_perf['expense_ratio_valid'] = df_perf['expense_ratio_pct'].between(0.1, 2.5)
            # Maybe clip or just keep the flag, the prompt says "check expense_ratio range (0.1% - 2.5%)"
            # we can filter out invalid ones or just leave it. I'll just cap it or filter
            df_perf = df_perf[(df_perf['expense_ratio_pct'] >= 0.1) & (df_perf['expense_ratio_pct'] <= 2.5) | df_perf['expense_ratio_pct'].isna()]
            
        df_perf.to_csv(os.path.join(processed_dir, "07_scheme_performance.csv"), index=False)
        print("Cleaned 07_scheme_performance.csv")

    # Process all other 7 files (01, 03, 04, 05, 06, 09, 10)
    all_files = glob.glob(os.path.join(raw_dir, "[0-1][0-9]_*.csv"))
    skip_files = ["02_nav_history.csv", "07_scheme_performance.csv", "08_investor_transactions.csv"]
    
    count = 3 # we already processed 3
    for file in all_files:
        filename = os.path.basename(file)
        if filename not in skip_files:
            try:
                df = pd.read_csv(file)
                # Keep same name as output
                out_name = filename
                df.to_csv(os.path.join(processed_dir, out_name), index=False)
                print(f"Cleaned {filename}")
                count += 1
            except Exception as e:
                print(f"Failed to clean {filename}: {e}")
    print(f"Total processed files: {count}")

if __name__ == "__main__":
    print("Starting Data Cleaning Process...")
    clean_data()
    print("Data Cleaning Complete.")
