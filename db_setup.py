import pandas as pd
from sqlalchemy import create_engine
import glob
import os

def load_data_to_sqlite(processed_dir="data/processed", db_path="sqlite:///mutual_funds.db"):
    engine = create_engine(db_path)
    csv_files = glob.glob(os.path.join(processed_dir, "*.csv"))
    
    if not csv_files:
        print(f"No processed CSV files found in {processed_dir}")
        return

    for file in csv_files:
        filename = os.path.basename(file)
        # Create a clean table name: e.g., '01_fund_master_cleaned.csv' -> 'fund_master'
        table_name = filename.replace("_cleaned.csv", "").split("_", 1)[-1] if "_" in filename and filename[0].isdigit() else filename.replace("_cleaned.csv", "")
        
        try:
            df = pd.read_csv(file)
            # Write to SQLite
            df.to_sql(table_name, con=engine, if_exists='replace', index=False)
            print(f"Successfully loaded {filename} into table '{table_name}'")
        except Exception as e:
            print(f"Failed to load {filename} to database: {e}")

if __name__ == "__main__":
    print("Starting Database Loading Process...")
    load_data_to_sqlite()
    print("Database Loading Complete.")
