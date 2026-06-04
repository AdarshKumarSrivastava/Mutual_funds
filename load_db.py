import pandas as pd
from sqlalchemy import create_engine
import os
import sqlite3

def load_data():
    db_path = "bluestock_mf.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    
    engine = create_engine(f'sqlite:///{db_path}')
    
    # Run schema.sql
    with sqlite3.connect(db_path) as conn:
        with open("schema.sql", "r") as f:
            conn.executescript(f.read())
            
    processed_dir = "data/processed"
    
    # 1. dim_fund
    df_fund = pd.read_csv(os.path.join(processed_dir, "01_fund_master.csv"))
    df_fund.to_sql('dim_fund', engine, if_exists='append', index=False)
    print(f"Loaded dim_fund: {len(df_fund)} rows")

    # 2. fact_nav
    df_nav = pd.read_csv(os.path.join(processed_dir, "02_nav_history.csv"))
    df_nav.to_sql('fact_nav', engine, if_exists='append', index=False)
    print(f"Loaded fact_nav: {len(df_nav)} rows")

    # 3. fact_transactions
    df_trans = pd.read_csv(os.path.join(processed_dir, "08_investor_transactions.csv"))
    df_trans.to_sql('fact_transactions', engine, if_exists='append', index=False)
    print(f"Loaded fact_transactions: {len(df_trans)} rows")

    # 4. fact_performance
    df_perf = pd.read_csv(os.path.join(processed_dir, "07_scheme_performance.csv"))
    # The CSV has scheme_name, fund_house, category, plan which are in dim_fund. 
    # To match schema, we should drop those or let them be ignored/loaded. 
    # Let's keep columns that are in the table.
    perf_cols = [
        'amfi_code', 'return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct',
        'benchmark_3yr_pct', 'alpha', 'beta', 'sharpe_ratio', 'sortino_ratio',
        'std_dev_ann_pct', 'max_drawdown_pct', 'aum_crore', 'expense_ratio_pct',
        'morningstar_rating', 'risk_grade', 'anomaly_flag'
    ]
    perf_cols = [c for c in perf_cols if c in df_perf.columns]
    df_perf[perf_cols].to_sql('fact_performance', engine, if_exists='append', index=False)
    print(f"Loaded fact_performance: {len(df_perf)} rows")

    # 5. fact_aum
    df_aum = pd.read_csv(os.path.join(processed_dir, "03_aum_by_fund_house.csv"))
    df_aum.to_sql('fact_aum', engine, if_exists='append', index=False)
    print(f"Loaded fact_aum: {len(df_aum)} rows")

    # 6. dim_date
    dates = pd.concat([
        df_nav['date'],
        df_trans['transaction_date'],
        df_aum['date']
    ]).dropna().unique()
    
    df_date = pd.DataFrame({'date': dates})
    df_date['date'] = pd.to_datetime(df_date['date'])
    df_date['year'] = df_date['date'].dt.year
    df_date['quarter'] = df_date['date'].dt.quarter
    df_date['month'] = df_date['date'].dt.month
    df_date['day'] = df_date['date'].dt.day
    df_date['day_of_week'] = df_date['date'].dt.dayofweek
    df_date['is_weekend'] = df_date['day_of_week'].isin([5, 6])
    
    df_date['date'] = df_date['date'].dt.strftime('%Y-%m-%d')
    df_date.to_sql('dim_date', engine, if_exists='append', index=False)
    print(f"Loaded dim_date: {len(df_date)} rows")

    # Other files just loaded as flat tables
    df_sip = pd.read_csv(os.path.join(processed_dir, "04_monthly_sip_inflows.csv"))
    df_sip.to_sql('monthly_sip_inflows', engine, if_exists='replace', index=False)
    print(f"Loaded monthly_sip_inflows: {len(df_sip)} rows")

    df_cat = pd.read_csv(os.path.join(processed_dir, "05_category_inflows.csv"))
    df_cat.to_sql('category_inflows', engine, if_exists='replace', index=False)
    print(f"Loaded category_inflows: {len(df_cat)} rows")

    df_ind = pd.read_csv(os.path.join(processed_dir, "06_industry_folio_count.csv"))
    df_ind.to_sql('industry_folio_count', engine, if_exists='replace', index=False)
    print(f"Loaded industry_folio_count: {len(df_ind)} rows")

    df_port = pd.read_csv(os.path.join(processed_dir, "09_portfolio_holdings.csv"))
    df_port.to_sql('portfolio_holdings', engine, if_exists='replace', index=False)
    print(f"Loaded portfolio_holdings: {len(df_port)} rows")

    df_bench = pd.read_csv(os.path.join(processed_dir, "10_benchmark_indices.csv"))
    df_bench.to_sql('benchmark_indices', engine, if_exists='replace', index=False)
    print(f"Loaded benchmark_indices: {len(df_bench)} rows")

if __name__ == "__main__":
    load_data()
