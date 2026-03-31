import sqlite3
import pandas as pd

# ---------------------------
# 1. Load & Prepare Data
# ---------------------------
def load_data():
    df = pd.read_csv("../data/ecommerce_sales_data.csv")
    df.columns = df.columns.str.strip().str.lower()
    df.dropna(inplace=True)
    return df

# ---------------------------
# 2. Create Database
# ---------------------------
def create_db(df):
    conn = sqlite3.connect("../data/ecommerce.db")
    df.to_sql("orders", conn, if_exists="replace", index=False)
    return conn

# ---------------------------
# 3. Detect Columns
# ---------------------------
def detect_columns(df):
    cols = {
        "sales": None,
        "profit": None,
        "category": None,
        "region": None,
        "product": None,
        "date": None
    }

    for col in df.columns:
        if 'sales' in col:
            cols["sales"] = col
        elif 'profit' in col:
            cols["profit"] = col
        elif 'category' in col:
            cols["category"] = col
        elif 'region' in col:
            cols["region"] = col
        elif 'product' in col:
            cols["product"] = col
        elif 'date' in col:
            cols["date"] = col

    return cols

# ---------------------------
# 4. Run Queries
# ---------------------------
def run_queries(conn, cols):

    # KPI Query
    query_kpi = f"""
    SELECT 
        SUM({cols['sales']}) AS total_revenue,
        SUM({cols['profit']}) AS total_profit,
        COUNT(*) AS total_orders,
        AVG({cols['sales']}) AS avg_order_value
    FROM orders
    """
    print("\n📊 KPI Metrics:")
    print(pd.read_sql(query_kpi, conn))

    # Category Analysis
    query_category = f"""
    SELECT "{cols['category']}" AS category,
           SUM({cols['sales']}) AS revenue,
           SUM({cols['profit']}) AS profit
    FROM orders
    GROUP BY category
    ORDER BY revenue DESC
    """
    print("\n📊 Category Performance:")
    print(pd.read_sql(query_category, conn))

    # Region Analysis
    query_region = f"""
    SELECT "{cols['region']}" AS region,
           SUM({cols['profit']}) AS total_profit
    FROM orders
    GROUP BY region
    ORDER BY total_profit DESC
    """
    print("\n📊 Region Profit:")
    print(pd.read_sql(query_region, conn))

    # Top Products (Advanced Ranking)
    query_products = f"""
    SELECT "{cols['product']}" AS product,
           SUM({cols['sales']}) AS total_sales,
           RANK() OVER (ORDER BY SUM({cols['sales']}) DESC) AS rank
    FROM orders
    GROUP BY product
    LIMIT 10
    """
    print("\n🏆 Top Products:")
    print(pd.read_sql(query_products, conn))

    # Monthly Trend
    query_month = f"""
    SELECT strftime('%m', "{cols['date']}") AS month,
           SUM({cols['sales']}) AS revenue
    FROM orders
    GROUP BY month
    ORDER BY month
    """
    print("\n📈 Monthly Sales Trend:")
    print(pd.read_sql(query_month, conn))

    # Profit Margin (Advanced KPI)
    query_margin = f"""
    SELECT 
        (SUM({cols['profit']}) / SUM({cols['sales']})) * 100 AS profit_margin
    FROM orders
    """
    print("\n💰 Profit Margin:")
    print(pd.read_sql(query_margin, conn))

# ---------------------------
# 5. Main Execution
# ---------------------------
def main():
    df = load_data()
    print("Columns:", df.columns)

    conn = create_db(df)
    cols = detect_columns(df)

    run_queries(conn, cols)

    conn.close()
    print("\n✅ All queries executed successfully!")

# ---------------------------
# Run Script
# ---------------------------
if __name__ == "__main__":
    main()