# Bluestock Mutual Fund Capstone 📈

Welcome to the Bluestock Mutual Fund Analytics Capstone Project. This project is an end-to-end data engineering, analytics, and visualization solution designed to extract insights from Indian mutual fund data (focusing on AUM, SIP trends, fund performance, and investor demographics).

## 🎯 Project Overview
Our primary objective is to ingest fragmented raw data, construct a reliable data pipeline, perform deep-dive exploratory and statistical analytics, and visualize the findings via an interactive dashboard.

### Key Deliverables:
1. **ETL Pipeline**: Automated extraction and cleaning (handling weekends/holidays with ffill) of mutual fund CSVs.
2. **SQLite Database Warehouse**: Relational schema hosting all standardized metrics.
3. **Advanced Analytics**: Statistical risk metrics (CAGR, Sharpe, Beta, VaR, Markowitz Efficient Frontier) developed in Jupyter Notebooks.
4. **Live NAV Fetching**: Background Python job seamlessly pulling live data from `mfapi.in`.
5. **Interactive Dashboard**: A robust multi-page application built on Streamlit showcasing Industry Overview, Fund Performance, Investor Analytics, and SIP Market Trends.
6. **Executive Reports**: Comprehensive 15-20 page PDF report and a 12-slide presentation summarizing the architecture and EDA findings.

## 🚀 Setup & Execution

### 1. Requirements
Ensure you have Python 3.9+ installed. The environment requires standard data science libraries:
```bash
pip install pandas numpy sqlite3 streamlit requests schedule matplotlib seaborn python-pptx fpdf2
```

### 2. Master Execution
We have provided a master script that sequentially runs the ETL pipeline, initializes the SQLite database, and runs the analytics generation.
```bash
# Ensure you are in the bluestock_mf_capstone directory
python run_pipeline.py
```

### 3. Launching the Dashboard
Once the pipeline has populated the SQLite warehouse, you can launch the interactive Streamlit dashboard:
```bash
python -m streamlit run dashboard/app.py
```
*(The dashboard runs on `http://localhost:8501`)*

### 4. Background NAV Updates
To keep the NAV dataset updated in real-time, run the live fetcher in the background. It is programmed to pull data at 8 PM on weekdays:
```bash
python scripts/live_nav_fetch.py
```

## 📁 Repository Structure
- `/data/raw/` - The source dataset CSVs
- `/data/processed/` - Cleaned output from the ETL process
- `/data/db/` - Contains the `bluestock_mf.db` SQLite database
- `/scripts/` - Pipeline scripts (`etl_pipeline.py`, `load_db.py`, etc.)
- `/dashboard/` - Contains the Streamlit app `app.py`
- `/notebooks/` - Analytics notebooks (VaR, Markowitz, EDA)
- `/reports/` - The final PDF report and PPTX presentation

## 📊 Published Dashboard
(Optional) This dashboard is ready to be published to Streamlit Community Cloud or Azure App Services with minimal configuration by pointing the host to the `dashboard/app.py` entrypoint.

---
*Developed as part of the Bluestock Data Analytics Capstone.*
