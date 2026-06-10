import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path

# Setup Path
db_path = Path(__file__).resolve().parent.parent / "data" / "db" / "bluestock_mf.db"

def load_data(query):
    conn = sqlite3.connect(str(db_path))
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

st.set_page_config(page_title="Bluestock MF Dashboard", layout="wide")

st.title("📈 Bluestock Mutual Fund Capstone Dashboard")

# Navigation
page = st.sidebar.selectbox("Select Page", ["Industry Overview", "Fund Performance", "Investor Analytics", "SIP Market Trends"])

if page == "Industry Overview":
    st.header("Industry Overview")
    df_aum = load_data("SELECT * FROM aum_by_fund_house")
    
    # Filters
    col1, col2 = st.columns(2)
    fund_house_filter = col1.multiselect("Select Fund House", df_aum['fund_house'].unique(), default=df_aum['fund_house'].unique()[:5])
    aum_min = col2.slider("Min AUM (Crores)", min_value=0, max_value=int(df_aum['aum_crore'].max()), value=0)
    
    filtered_df = df_aum[(df_aum['fund_house'].isin(fund_house_filter)) & (df_aum['aum_crore'] >= aum_min)]
    
    st.bar_chart(filtered_df.set_index('fund_house')['aum_crore'])
    st.dataframe(filtered_df)

elif page == "Fund Performance":
    st.header("Fund Performance (Return vs Expense Ratio)")
    df_perf = load_data("SELECT * FROM scheme_performance")
    
    # Filters
    col1, col2 = st.columns(2)
    category_filter = col1.selectbox("Select Category", ["All"] + list(df_perf['category'].dropna().unique()))
    if category_filter != "All":
        df_perf = df_perf[df_perf['category'] == category_filter]
        
    expense_max = col2.slider("Max Expense Ratio (%)", min_value=0.0, max_value=2.5, value=2.5, step=0.1)
    df_perf = df_perf[df_perf['expense_ratio_pct'] <= expense_max]
    
    st.scatter_chart(df_perf, x="expense_ratio_pct", y="return_1yr_pct", color="category")
    st.dataframe(df_perf[['amfi_code', 'scheme_name', 'return_1yr_pct', 'expense_ratio_pct']])

elif page == "Investor Analytics":
    st.header("Investor Transactions")
    df_inv = load_data("SELECT * FROM investor_transactions")
    
    # Filters
    col1, col2 = st.columns(2)
    type_filter = col1.multiselect("Transaction Type", df_inv['transaction_type'].unique(), default=df_inv['transaction_type'].unique())
    kyc_filter = col2.selectbox("KYC Status", ["All"] + list(df_inv['kyc_status'].unique()))
    
    df_filtered = df_inv[df_inv['transaction_type'].isin(type_filter)]
    if kyc_filter != "All":
        df_filtered = df_filtered[df_filtered['kyc_status'] == kyc_filter]
        
    st.write(f"Total Transactions: {len(df_filtered)}")
    st.dataframe(df_filtered.head(100))

elif page == "SIP Market Trends":
    st.header("SIP Market Trends")
    df_sip = load_data("SELECT * FROM monthly_sip_inflows")
    
    # Filters
    col1, col2 = st.columns(2)
    
    # Convert month string (e.g. "Jan-2023" or similar) to datetime if needed
    df_sip['month'] = pd.to_datetime(df_sip['month'], format='mixed', errors='coerce')
    
    min_date = col1.date_input("Start Date", df_sip['month'].min())
    max_date = col2.date_input("End Date", df_sip['month'].max())
    
    df_filtered = df_sip[(df_sip['month'].dt.date >= min_date) & (df_sip['month'].dt.date <= max_date)]
    
    st.line_chart(df_filtered.set_index('month')['sip_inflow_crore'])
    st.dataframe(df_filtered)
