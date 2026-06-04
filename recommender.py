import sqlite3
import pandas as pd
import argparse

def recommend_funds(risk_appetite, db_path='bluestock_mf.db'):
    conn = sqlite3.connect(db_path)
    
    # Query to fetch funds based on risk appetite, ordered by sharpe ratio descending
    query = """
    SELECT f.scheme_name, f.category, p.risk_grade, p.sharpe_ratio, p.return_1yr_pct, p.return_3yr_pct
    FROM fact_performance p
    JOIN dim_fund f ON p.amfi_code = f.amfi_code
    WHERE LOWER(p.risk_grade) = ?
    ORDER BY p.sharpe_ratio DESC
    LIMIT 3
    """
    
    df = pd.read_sql(query, conn, params=(risk_appetite.lower(),))
    conn.close()
    
    if df.empty:
        print(f"No funds found for risk appetite: {risk_appetite}")
        return
        
    print(f"\n--- Top 3 Fund Recommendations for {risk_appetite.capitalize()} Risk Appetite ---")
    print("-" * 100)
    # Using pandas to format tabular output nicely
    print(df.to_string(index=False))
    print("-" * 100)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Mutual Fund Recommender')
    parser.add_argument('--risk', type=str, choices=['Low', 'Moderate', 'High', 'Very High'], 
                        default='Moderate', help='Risk appetite (Low, Moderate, High, Very High)')
    
    args = parser.parse_args()
    recommend_funds(args.risk)
