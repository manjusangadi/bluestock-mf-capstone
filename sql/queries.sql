-- queries.sql
-- 10 Analytical SQL Queries for Mutual Fund Capstone Project

-- Query 1: Top 5 funds by AUM (Assets Under Management)
-- Business Definition: Identifies the largest schemes by size in our database.
SELECT 
    amfi_code, 
    scheme_name, 
    fund_house, 
    aum_crore
FROM fact_performance
ORDER BY aum_crore DESC;

-- Query 2: Average NAV per month for each mutual fund scheme
-- Business Definition: Tracks the monthly performance trend of each scheme by averaging daily NAVs.
SELECT 
    n.amfi_code, 
    f.scheme_name,
    d.year,
    d.month_name,
    ROUND(AVG(n.nav), 4) as avg_nav
FROM fact_nav n
JOIN dim_fund f ON n.amfi_code = f.amfi_code
JOIN dim_date d ON n.date = d.date
GROUP BY n.amfi_code, d.year, d.month
ORDER BY n.amfi_code, d.year, d.month;

-- Query 3: SIP YoY growth rate of monthly inflows (comparing each month with the same month of the previous year)
-- Business Definition: Calculates YoY trend of SIP inflows to measure growth in retail investments.
SELECT 
    t1.month as current_month,
    t1.sip_inflow_crore as current_inflow_cr,
    t2.month as prev_year_month,
    t2.sip_inflow_crore as prev_year_inflow_cr,
    ROUND(((t1.sip_inflow_crore - t2.sip_inflow_crore) * 100.0 / t2.sip_inflow_crore), 2) as calculated_yoy_growth_pct,
    t1.yoy_growth_pct as documented_yoy_growth_pct
FROM monthly_sip_inflows t1
JOIN monthly_sip_inflows t2 
  ON t2.month = strftime('%Y-%m', date(t1.month || '-01', '-1 year'))
ORDER BY t1.month;

-- Query 4: Total transaction volume and amount by state
-- Business Definition: Identifies geographical density and capital flow of investments across different Indian states.
SELECT 
    state,
    COUNT(*) as transaction_count,
    ROUND(SUM(amount_inr) / 10000000.0, 4) as total_amount_crore
FROM fact_transactions
GROUP BY state
ORDER BY total_amount_crore DESC;

-- Query 5: Low-cost funds (expense ratio less than 1.0%)
-- Business Definition: Finds schemes that are cheap to invest in (cost-efficient) across classes.
SELECT 
    amfi_code, 
    scheme_name, 
    fund_house, 
    category, 
    plan, 
    expense_ratio_pct
FROM fact_performance
WHERE expense_ratio_pct < 1.0
ORDER BY expense_ratio_pct ASC;

-- Query 6: Top 5 sectors by average portfolio weight
-- Business Definition: Shows where mutual funds are allocating the highest percentage of capital on average.
SELECT 
    sector, 
    ROUND(AVG(weight_pct), 2) as avg_weight_pct,
    COUNT(DISTINCT amfi_code) as holding_funds_count
FROM portfolio_holdings
GROUP BY sector
ORDER BY avg_weight_pct DESC;

-- Query 7: Risk-adjusted performance indicators (Sharpe & Sortino) by risk grade
-- Business Definition: Evaluates which risk grades yield the best return per unit of volatility/downside risk.
SELECT 
    risk_grade,
    COUNT(*) as fund_count,
    ROUND(AVG(sharpe_ratio), 4) as average_sharpe_ratio,
    ROUND(AVG(sortino_ratio), 4) as average_sortino_ratio,
    ROUND(AVG(return_3yr_pct), 2) as average_3yr_return_pct
FROM fact_performance
GROUP BY risk_grade
ORDER BY average_sharpe_ratio DESC;

-- Query 8: High-performing schemes with aggressive market sensitivity (Beta > 1.0, 3-Year Return > 15%)
-- Business Definition: Filters for schemes offering strong returns that outperform the benchmark under high-beta allocations.
SELECT 
    scheme_name,
    fund_house,
    beta,
    return_3yr_pct,
    alpha,
    risk_grade
FROM fact_performance
WHERE beta > 1.0 AND return_3yr_pct > 15.0
ORDER BY return_3yr_pct DESC;

-- Query 9: Transaction distribution by investor demographic characteristics (Age group & Gender)
-- Business Definition: Shows the transaction volume and average ticket size across age brackets and genders.
SELECT 
    age_group,
    gender,
    COUNT(*) as transaction_count,
    ROUND(SUM(amount_inr) / 10000000.0, 4) as total_amount_crore,
    ROUND(AVG(amount_inr), 2) as avg_transaction_size_inr
FROM fact_transactions
GROUP BY age_group, gender
ORDER BY age_group, gender;

-- Query 10: Average monthly net inflow (in Crores) per asset category
-- Business Definition: Evaluates which categories (Large Cap, Mid Cap, Small Cap, etc.) attract the highest monthly inflows.
SELECT 
    category,
    ROUND(AVG(net_inflow_crore), 2) as avg_monthly_net_inflow_crore,
    ROUND(SUM(net_inflow_crore), 2) as total_net_inflow_crore
FROM category_inflows
GROUP BY category
ORDER BY avg_monthly_net_inflow_crore DESC;
