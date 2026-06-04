-- 1. Top 5 funds by AUM
SELECT 
    f.scheme_name, 
    f.fund_house, 
    p.aum_crore 
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
ORDER BY p.aum_crore DESC
LIMIT 5;

-- 2. Average NAV per month
SELECT 
    f.scheme_name,
    d.year, 
    d.month, 
    AVG(n.nav) AS avg_nav
FROM fact_nav n
JOIN dim_date d ON n.date = d.date
JOIN dim_fund f ON n.amfi_code = f.amfi_code
GROUP BY f.scheme_name, d.year, d.month
ORDER BY f.scheme_name, d.year, d.month;

-- 3. SIP YoY Growth (using monthly_sip_inflows table)
SELECT 
    month, 
    sip_inflow_crore, 
    yoy_growth_pct
FROM monthly_sip_inflows
ORDER BY month;

-- 4. Transactions by State
SELECT 
    state, 
    COUNT(transaction_id) AS total_transactions, 
    SUM(amount_inr) AS total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_amount DESC;

-- 5. Funds with expense_ratio < 1%
SELECT 
    scheme_name, 
    expense_ratio_pct,
    category 
FROM dim_fund
WHERE expense_ratio_pct < 1.0
ORDER BY expense_ratio_pct ASC;

-- 6. Top 5 states by total investment amount for SIP transactions
SELECT 
    state, 
    SUM(amount_inr) as total_sip_investment
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY state
ORDER BY total_sip_investment DESC
LIMIT 5;

-- 7. Best performing funds (1yr return > 15%)
SELECT 
    f.scheme_name, 
    p.return_1yr_pct, 
    p.risk_grade
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
WHERE p.return_1yr_pct > 15
ORDER BY p.return_1yr_pct DESC;

-- 8. Total AUM by Fund House
SELECT 
    fund_house, 
    SUM(aum_crore) AS total_aum_crore
FROM fact_aum
WHERE date = (SELECT MAX(date) FROM fact_aum)
GROUP BY fund_house
ORDER BY total_aum_crore DESC;

-- 9. Number of investors by KYC status
SELECT 
    kyc_status, 
    COUNT(DISTINCT investor_id) AS num_investors
FROM fact_transactions
GROUP BY kyc_status;

-- 10. Average transaction amount by gender and age group
SELECT 
    gender, 
    age_group, 
    AVG(amount_inr) AS avg_transaction_amount
FROM fact_transactions
GROUP BY gender, age_group
ORDER BY avg_transaction_amount DESC;
