# Data Dictionary - Mutual Fund Database

## Database: `bluestock_mf.db`

### 1. `dim_fund`
**Source:** `01_fund_master.csv`
Contains descriptive information about mutual fund schemes.

| Column | Data Type | Description |
|--------|-----------|-------------|
| `amfi_code` | INTEGER | Primary Key. Unique code assigned by AMFI. |
| `fund_house` | TEXT | Name of the Asset Management Company (AMC). |
| `scheme_name` | TEXT | Full name of the mutual fund scheme. |
| `category` | TEXT | Broad category of the fund (e.g., Equity, Debt). |
| `sub_category` | TEXT | Specific sub-category (e.g., Large Cap, Mid Cap). |
| `plan` | TEXT | Regular or Direct plan. |
| `launch_date` | DATE | Date the fund was launched. |
| `benchmark` | TEXT | Benchmark index for the fund. |
| `expense_ratio_pct` | REAL | Total Expense Ratio (TER) in percentage. |
| `exit_load_pct` | REAL | Exit load percentage on redemption. |
| `min_sip_amount` | REAL | Minimum investment amount for SIP. |
| `min_lumpsum_amount` | REAL | Minimum investment amount for lumpsum. |
| `fund_manager` | TEXT | Name of the fund manager. |
| `risk_category` | TEXT | Risk level associated with the fund (e.g., High, Moderate). |
| `sebi_category_code` | TEXT | SEBI categorization code. |

### 2. `dim_date`
**Source:** Generated from `nav_history`, `investor_transactions`, `aum`
Central date dimension for time-series analysis.

| Column | Data Type | Description |
|--------|-----------|-------------|
| `date` | DATE | Primary Key. The calendar date. |
| `year` | INTEGER | Calendar year. |
| `quarter` | INTEGER | Calendar quarter (1-4). |
| `month` | INTEGER | Month of the year (1-12). |
| `day` | INTEGER | Day of the month. |
| `day_of_week` | INTEGER | Day of the week (0=Monday, 6=Sunday). |
| `is_weekend` | BOOLEAN | True if the day is a weekend. |

### 3. `fact_nav`
**Source:** `02_nav_history.csv`
Historical daily Net Asset Value (NAV) of funds.

| Column | Data Type | Description |
|--------|-----------|-------------|
| `nav_id` | INTEGER | Primary Key. Auto-incremented ID. |
| `amfi_code` | INTEGER | Foreign Key to `dim_fund`. |
| `date` | DATE | Foreign Key to `dim_date`. |
| `nav` | REAL | Net Asset Value on the given date. |

### 4. `fact_transactions`
**Source:** `08_investor_transactions.csv`
Investor transaction records.

| Column | Data Type | Description |
|--------|-----------|-------------|
| `transaction_id` | INTEGER | Primary Key. Auto-incremented ID. |
| `investor_id` | TEXT | Unique identifier for the investor. |
| `transaction_date`| DATE | Foreign Key to `dim_date`. |
| `amfi_code` | INTEGER | Foreign Key to `dim_fund`. |
| `transaction_type`| TEXT | Type of transaction (SIP, Lumpsum, Redemption). |
| `amount_inr` | REAL | Transaction amount in Indian Rupees. |
| `state` | TEXT | State of the investor. |
| `city` | TEXT | City of the investor. |
| `city_tier` | TEXT | Tier classification of the city. |
| `age_group` | TEXT | Age group of the investor. |
| `gender` | TEXT | Gender of the investor. |
| `annual_income_lakh` | REAL | Annual income bracket in lakhs. |
| `payment_mode` | TEXT | Mode of payment used. |
| `kyc_status` | TEXT | KYC verification status (e.g., Verified). |

### 5. `fact_performance`
**Source:** `07_scheme_performance.csv`
Performance metrics for mutual fund schemes.

| Column | Data Type | Description |
|--------|-----------|-------------|
| `performance_id`| INTEGER | Primary Key. Auto-incremented ID. |
| `amfi_code` | INTEGER | Foreign Key to `dim_fund`. |
| `return_1yr_pct`| REAL | 1-year trailing return percentage. |
| `return_3yr_pct`| REAL | 3-year trailing return percentage. |
| `return_5yr_pct`| REAL | 5-year trailing return percentage. |
| `benchmark_3yr_pct` | REAL | 3-year benchmark return percentage. |
| `alpha` | REAL | Alpha measure. |
| `beta` | REAL | Beta measure. |
| `sharpe_ratio` | REAL | Sharpe ratio. |
| `sortino_ratio` | REAL | Sortino ratio. |
| `std_dev_ann_pct` | REAL | Annualized standard deviation. |
| `max_drawdown_pct`| REAL | Maximum drawdown percentage. |
| `aum_crore` | REAL | Assets Under Management in Crores. |
| `expense_ratio_pct` | REAL | Expense ratio in percentage. |
| `morningstar_rating`| INTEGER | Morningstar rating. |
| `risk_grade` | TEXT | Risk grade assigned. |
| `anomaly_flag` | BOOLEAN | True if anomalies were detected in returns. |

### 6. `fact_aum`
**Source:** `03_aum_by_fund_house.csv`
Assets Under Management aggregated by Fund House.

| Column | Data Type | Description |
|--------|-----------|-------------|
| `aum_id` | INTEGER | Primary Key. Auto-incremented ID. |
| `fund_house` | TEXT | Name of the Asset Management Company. |
| `date` | DATE | Foreign Key to `dim_date`. |
| `aum_lakh_crore`| REAL | AUM in Lakh Crores. |
| `aum_crore` | REAL | AUM in Crores. |
| `num_schemes` | INTEGER | Number of active schemes. |
