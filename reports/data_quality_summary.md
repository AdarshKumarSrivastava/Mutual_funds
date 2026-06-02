# Data Quality Summary Report

## 1. Fund Master Exploration

Based on the exploration of `01_fund_master.csv`, here are the structural insights into the mutual fund universe within our dataset:

- **Unique Fund Houses (10):**
  - SBI Mutual Fund
  - HDFC Mutual Fund
  - ICICI Prudential MF
  - Nippon India MF
  - Kotak Mahindra MF
  - Axis Mutual Fund
  - Aditya Birla Sun Life MF
  - UTI Mutual Fund
  - Mirae Asset MF
  - DSP Mutual Fund

- **Unique Categories (2):**
  - Equity
  - Debt

- **Unique Sub-Categories (12):**
  - Large Cap
  - Small Cap
  - Gilt
  - Mid Cap
  - Short Duration
  - Value
  - Liquid
  - Index/ETF
  - Flexi Cap
  - Index
  - Large & Mid Cap
  - ELSS

- **Unique Risk Grades (5):**
  - Low
  - Moderate
  - Moderately High
  - High
  - Very High

- **AMFI Scheme Code Structure:**
  - Every AMFI scheme code in the master dataset follows a strict **6-digit integer structure** (e.g., `119551`). There are no alphanumeric codes or anomalies in length.

---

## 2. AMFI Code Validation & Mapping

A crucial step in ensuring data integrity is verifying that the relationship between the `fund_master` (metadata) and `nav_history` (time-series data) is sound. 

Validation Process:
We cross-referenced every unique `amfi_code` present in the `01_fund_master.csv` file against the `02_nav_history.csv` file to identify any orphaned records.

**Validation Results:**
- **Total unique AMFI codes in `fund_master`:** 40
- **Total unique AMFI codes in `nav_history`:** 40
- **Missing / Unmapped Codes:** 0

**Data Quality Conclusion:**
The AMFI scheme codes are in perfect synchronization. **100% of the scheme codes defined in the `fund_master` exist in the `nav_history` dataset.** The validation has passed with zero missing data mappings. The dataset is structurally sound and ready for robust time-series analysis and dashboard integration.
