-- Find top 5 funds by 1-year return
SELECT amfi_code, scheme_name, category, return_1yr_pct
FROM scheme_performance
ORDER BY return_1yr_pct DESC
LIMIT 5;

-- Average expense ratio by category
SELECT category, AVG(expense_ratio_pct) as avg_expense_ratio
FROM scheme_performance
GROUP BY category
ORDER BY avg_expense_ratio DESC;

-- Total SIP inflows per month
SELECT month, SUM(sip_inflow_crore) as total_sip_inflows
FROM monthly_sip_inflows
GROUP BY month
ORDER BY month DESC;

-- Get NAV history for a specific fund
SELECT date, nav 
FROM nav_history
WHERE amfi_code = '119092'
ORDER BY date ASC;
