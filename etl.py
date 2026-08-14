import pandas as pd
import sqlite3

def extract():
    print("Extracting data...") 
    df = pd.read_csv("rawData.csv")
    return df

def transform(df):
    print("Transforming and cleaning...")
    df = df.dropna(subset=["item_name", "price", "quantity"])
    df["item_name"] = df["item_name"].str.strip().str.title()
    df["item_name"] = pd.to_datetime(df["order_date"], format='mixed').dt.strftime("%Y-%m-%d")
    df["total_spent"] = df["price"] * df["quantity"]

    return df

def load(df):
    print("Loading data into SQLite...")
    conn = sqlite3.connect("coffee_shop.db")
    df.to_sql("sales", conn, if_exists="replace", index=False)

    query = """
    SELECT
        item_name, 
        SUM(quantity) as total_units_sold,
        ROUND(SUM(total_spent), 2) AS total_revenue
    FROM sales
    GROUP BY item_name
    ORDER BY total_revenue DESC
    """
    summary_df = pd.read_sql(query, conn)
    summary_df.to_csv("daily_summary.csv", index=False)
    conn.close()
    print("pipeline finished!!!!")

if __name__ == "__main__":
    raw_data = extract()
    clean_data = transform(raw_data)
    load(clean_data)