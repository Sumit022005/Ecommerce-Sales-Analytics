import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------
# 1. Load Data
# ---------------------------
df = pd.read_csv("../data/ecommerce_sales_data.csv")

# ---------------------------
# 2. Clean Data
# ---------------------------
df.columns = df.columns.str.strip().str.lower()
df.dropna(inplace=True)

# Detect columns
date_col = [col for col in df.columns if 'date' in col][0]
sales_col = [col for col in df.columns if 'sales' in col][0]
profit_col = [col for col in df.columns if 'profit' in col][0]
category_col = [col for col in df.columns if 'category' in col][0]
region_col = [col for col in df.columns if 'region' in col][0]
product_col = [col for col in df.columns if 'product' in col][0]

df[date_col] = pd.to_datetime(df[date_col])

# ---------------------------
# 3. Feature Engineering
# ---------------------------
df['month'] = df[date_col].dt.month
df['year'] = df[date_col].dt.year

# ---------------------------
# 4. KPI Metrics
# ---------------------------
total_revenue = df[sales_col].sum()
total_profit = df[profit_col].sum()
total_orders = len(df)
avg_order_value = total_revenue / total_orders

print(f"\nTotal Revenue: {total_revenue:,.0f}")
print(f"Total Profit: {total_profit:,.0f}")
print(f"Total Orders: {total_orders}")
print(f"Average Order Value: {avg_order_value:.2f}")

# ---------------------------
# 5. Analysis
# ---------------------------

# Category Analysis
category_sales = df.groupby(category_col)[sales_col].sum().sort_values(ascending=False)

# Region Profit
region_profit = df.groupby(region_col)[profit_col].sum().sort_values(ascending=False)

# Top Products
top_products = df.groupby(product_col)[sales_col].sum().sort_values(ascending=False).head(10)

# Monthly Trend
monthly_sales = df.groupby('month')[sales_col].sum()

# ---------------------------
# 6. Visualization (Advanced)
# ---------------------------
sns.set_style("whitegrid")

# Category Sales
plt.figure()
category_sales.plot(kind='bar')
plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Sales")
plt.show()

# Region Profit
plt.figure()
region_profit.plot(kind='bar')
plt.title("Profit by Region")
plt.xlabel("Region")
plt.ylabel("Profit")
plt.show()

# Monthly Trend
plt.figure()
monthly_sales.plot(marker='o')
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.show()

# Top Products
plt.figure()
top_products.plot(kind='barh')
plt.title("Top 10 Products by Sales")
plt.xlabel("Sales")
plt.show()

# ---------------------------
# 7. RFM Analysis (Advanced)
# ---------------------------
customer_col = None
for col in df.columns:
    if 'customer' in col:
        customer_col = col

if customer_col:
    today = df[date_col].max()

    rfm = df.groupby(customer_col).agg({
        date_col: lambda x: (today - x.max()).days,
        sales_col: ['count', 'sum']
    })

    rfm.columns = ['recency', 'frequency', 'monetary']

    # Score (Advanced)
    rfm['r_score'] = pd.qcut(rfm['recency'], 4, labels=[4,3,2,1])
    rfm['f_score'] = pd.qcut(rfm['frequency'], 4, labels=[1,2,3,4])
    rfm['m_score'] = pd.qcut(rfm['monetary'], 4, labels=[1,2,3,4])

    rfm['rfm_score'] = rfm[['r_score','f_score','m_score']].sum(axis=1)

    print("\nRFM Analysis:\n", rfm.head())

# ---------------------------
# 8. Insights (Auto Generated)
# ---------------------------
print("\n📊 Key Insights:")

print(f"- Top Category: {category_sales.idxmax()}")
print(f"- Most Profitable Region: {region_profit.idxmax()}")
print(f"- Best Product: {top_products.idxmax()}")
print(f"- Peak Month: {monthly_sales.idxmax()}")