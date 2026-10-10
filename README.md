# E-Commerce Sales Analytics Platform

## Project Overview

An end-to-end data analytics project using Python for data cleaning, SQLite for relational querying, and Power BI for executive reporting to isolate regional profit leakage and optimize product performance metrics.

## Tools Used

- **Python:** Pandas, NumPy, Matplotlib, Seaborn
- **SQL:** SQLite (Window Functions, Aggregate Joins, CTEs)
- **BI Platform:** Power BI Desktop

## Key Analytical Insights

- **Product Performance:** Category A accounts for 38% of absolute volume but contributes under 12% to the net margin due to high logistical overheads.
- **Geographical Distribution:** The West Region generated the highest profit metrics ($XX,XXX), driven by low customer acquisition costs.
- **Inventory Risk:** Identified top 10 bottleneck products contributing to 60% of total customer return volumes.

## 📊 Executive Dashboard Preview

![Interactive Business Dashboard](dashboard/dashboard.png)

👉 **[Click Here to Open and View the Complete Interactive PDF Report](./dashboard/E-Commerce_Sales_Dashboard_Report.pdf)**

## 💾 Core SQL Query Portfolio

```sql
SELECT
    product_id,
    SUM(sales) AS total_revenue,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct
FROM sales_data
GROUP BY product_id
ORDER BY total_revenue DESC
LIMIT 10;
```
