# Mutual Funds Data Engineering Project

## Overview
This project focuses on the data ingestion, cleaning, database integration, and visualization of Mutual Fund datasets. The current phase (Day 1) includes fetching live NAV data via APIs and performing initial explorations on raw CSV datasets provided.

## Project Structure
- `data/raw/`: Contains raw CSV datasets (both provided and fetched from APIs).
- `data/processed/`: Will contain cleaned and processed datasets.
- `notebooks/`: Jupyter notebooks for exploratory data analysis (EDA).
- `sql/`: SQL scripts for database schemas and queries.
- `dashboard/`: Application code for the final visualization dashboard.
- `reports/`: Generated reports and summaries.

## Setup Instructions

1. **Install Dependencies:**
   Ensure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Fetch Live NAV Data:**
   Run the following script to fetch the latest NAV data for key mutual fund schemes:
   ```bash
   python live_nav_fetch.py
   ```

3. **Run Data Ingestion and Quality Checks:**
   Run the ingestion script to summarize and validate the datasets:
   ```bash
   python data_ingestion.py
   ```

## Current Progress
- **Day 1:** Data Ingestion Complete. Set up project structure, installed dependencies, fetched API data, loaded CSVs, and validated AMFI codes.
