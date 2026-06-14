"""
Database Setup Script for Bluestock Mutual Fund Capstone.

This module is responsible for taking the cleaned CSV data from the processed 
directory, loading it into an SQLite database (`bluestock_mf.db`), and generating 
a `schema.sql` file.
"""

import sqlite3
import pandas as pd
from pathlib import Path

def setup_database():
    """
    Connects to SQLite, ingests processed CSV files as tables, and extracts schema.
    """
    base_path = Path(__file__).resolve().parent.parent
    processed_dir = base_path / "data" / "processed"
    db_path = base_path / "data" / "db" / "bluestock_mf.db"
    sql_dir = base_path / "sql"
    
    sql_dir.mkdir(exist_ok=True)
    db_path.parent.mkdir(exist_ok=True)

    if not processed_dir.exists():
        return

    conn = sqlite3.connect(str(db_path))

    # Iterate over processed CSV files and load them into SQLite
    for file in processed_dir.glob("*.csv"):
        table_name = file.stem
        # Strip leading numbers like "01_" if present for a cleaner table name
        if table_name[0:2].isdigit() and table_name[2] == "_":
            table_name = table_name[3:]
            
        try:
            df = pd.read_csv(file)
            df.to_sql(table_name, conn, if_exists='replace', index=False)
        except Exception:
            pass

    # Generate schema.sql
    with open(sql_dir / "schema.sql", "w") as f:
        for line in conn.iterdump():
            if line.startswith("CREATE TABLE"):
                f.write(f"{line}\n")
    
    conn.close()

if __name__ == "__main__":
    setup_database()
