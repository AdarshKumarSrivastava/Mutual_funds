import pandas as pd, numpy as np, matplotlib.pyplot as plt, sqlite3, warnings
warnings.filterwarnings('ignore')

DB_PATH = 'bluestock_mf.db'
conn = sqlite3.connect(DB_PATH)

# Load tables
nav_df = pd.read_sql('SELECT * FROM fact_nav', conn)
fund_df = pd.read_sql('SELECT * FROM dim_fund', conn)
perf_df = pd.read_sql('SELECT * FROM fact_performance', conn)

# Ensure date column
nav_df['date'] = pd.to_datetime(nav_df['date'])

# ---------- Historical VaR (95%) and CVaR ----------
var_cvar_records = []
for amfi, grp in nav_df.groupby('amfi_code'):
    grp = grp.sort_values('date')
    grp['return'] = grp['nav'].pct_change()
    returns = grp['return'].dropna()
    if returns.empty:
        continue
    var95 = np.percentile(returns, 5)
    cvar95 = returns[returns <= var95].mean()
    scheme_name = grp['amfi_code'].iloc[0]
    # join scheme name from dim_fund
    name_row = fund_df.loc[fund_df['amfi_code'] == amfi, 'scheme_name']
    scheme_name = name_row.iloc[0] if not name_row.empty else ''
    var_cvar_records.append({
        'amfi_code': amfi,
        'scheme_name': scheme_name,
        'VaR_95': var95,
        'CVaR_95': cvar95
    })
var_cvar_df = pd.DataFrame(var_cvar_records)
var_cvar_df.to_csv('var_cvar_report.csv', index=False)
print('Saved var_cvar_report.csv')

# ---------- Rolling 90‑day Sharpe Ratio (annualised) ----------
# Determine top‑5 funds by latest AUM
aum_df = pd.read_sql('SELECT * FROM fact_aum', conn)
latest_date = aum_df['date'].max()
top5_fund_houses = aum_df[aum_df['date'] == latest_date].nlargest(5, 'aum_crore')['fund_house'].tolist()
top5_codes = fund_df[fund_df['fund_house'].isin(top5_fund_houses)]['amfi_code'].unique()

plt.figure(figsize=(12, 6))
for code in top5_codes:
    sub = nav_df[nav_df['amfi_code'] == code].sort_values('date')
    sub['return'] = sub['nav'].pct_change()
    roll_sharpe = (sub['return'].rolling(90).mean() / sub['return'].rolling(90).std()) * np.sqrt(252)
    scheme_name = fund_df.loc[fund_df['amfi_code'] == code, 'scheme_name'].iloc[0]
    plt.plot(sub['date'], roll_sharpe, label=scheme_name)
plt.title('90‑Day Rolling Sharpe Ratio – Top 5 Funds by AUM')
plt.xlabel('Date')
plt.ylabel('Sharpe (Annualised)')
plt.legend()
plt.tight_layout()
plt.savefig('rolling_sharpe_chart.png')
print('Saved rolling_sharpe_chart.png')

conn.close()
