# Bluestock Mutual Fund Capstone Project

This repository contains the end-to-end data pipeline, analytics, and dashboard for the Bluestock Mutual Fund Capstone project.

## Project Structure

- `data/`
  - `raw/`: Original CSV files and live fetched NAV datasets.
  - `processed/`: Cleaned CSV files ready for database ingestion.
  - `db/`: SQLite database `bluestock_mf.db`.
- `scripts/`
  - `etl_pipeline.py`: Pipeline for data extraction, cleaning (forward-filling weekends/holidays for NAV), and loading into `processed/`.
  - `load_db.py`: Ingests processed CSVs into the SQLite database.
  - `live_nav_fetch.py`: Scheduled job (Cron / Schedule library) for fetching live NAV from `mfapi.in` at 8 PM weekdays.
  - `email_report.py`: Automated HTML email reporting script.
- `notebooks/`: Jupyter Notebooks covering Data Ingestion, Data Cleaning, EDA, Performance Analytics (CAGR, Sharpe, VaR), and Advanced Analytics (Cohort, Markowitz Efficient Frontier, Monte Carlo).
- `dashboard/`: Streamlit Web App (`app.py`) featuring 4 interactive pages with slicers.
- `sql/`: Contains `schema.sql` and example `queries.sql`.
- `reports/`: Final presentation and project reports.

## Setup Instructions

1. **Install dependencies**:
   ```bash
   pip install pandas numpy requests streamlit schedule
   ```

2. **Run the ETL Pipeline**:
   ```bash
   python scripts/etl_pipeline.py
   ```

3. **Initialize the Database**:
   ```bash
   python scripts/load_db.py
   ```

4. **Launch the Dashboard**:
   ```bash
   streamlit run dashboard/app.py
   ```

## Bonus Features
- **B1**: Live NAV fetching schedule implemented in `live_nav_fetch.py`.
- **B2**: Streamlit Web App serving as a dynamic, interactive dashboard with filters on every page.
- **B3 & B4**: Monte Carlo NAV projection & Markowitz Optimization included in `notebooks/05_advanced_analytics.ipynb`.
- **B5**: Automated Weekly HTML email report in `scripts/email_report.py`.
