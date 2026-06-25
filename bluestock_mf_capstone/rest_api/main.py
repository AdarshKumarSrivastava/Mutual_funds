from fastapi import FastAPI
import sqlite3
import pandas as pd
from pathlib import Path

app = FastAPI(title="Bluestock MF RestAPI", description="API for Mutual Fund Capstone")
db_path = Path(__file__).resolve().parent.parent / "data" / "db" / "bluestock_mf.db"

def query_db(query: str):
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/")
def root():
    return {"message": "Welcome to the Bluestock MF RestAPI"}

@app.get("/api/aum")
def get_aum():
    """Get AUM by Fund House"""
    return query_db("SELECT * FROM aum_by_fund_house")

@app.get("/api/performance")
def get_performance():
    """Get Scheme Performance"""
    return query_db("SELECT * FROM scheme_performance")

@app.get("/api/transactions")
def get_transactions():
    """Get Investor Transactions"""
    return query_db("SELECT * FROM investor_transactions")

@app.get("/api/sip_trends")
def get_sip_trends():
    """Get Monthly SIP Inflows"""
    return query_db("SELECT * FROM monthly_sip_inflows")
