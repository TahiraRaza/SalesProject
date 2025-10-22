"""
This script reads a sales dataset from a CSV file, updates a SQLite database,
handles any errors, and logs them into a log file.
"""

import pandas as pd
import sqlite3
import logging

# -------------------------
# Setup logging
# -------------------------
# All errors and info messages will be saved in sales_data.log
logging.basicConfig(
    filename='sales_data.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# -------------------------
# Read the CSV file
# -------------------------
csv_file = "sales_data.csv"

try:
    df = pd.read_csv(csv_file)
    print("CSV data preview:")
    print(df.head())  # show first few rows in terminal
except Exception as e:
    logging.error(f"Error reading CSV file: {e}")
    print(f"Error reading CSV file: {e}")
    df = pd.DataFrame()  # create empty DataFrame on error

# -------------------------
# Update SQLite database
# -------------------------
try:
    # Connect to SQLite database (creates sales.db if it doesn't exist)
    conn = sqlite3.connect("sales.db")
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            date TEXT,
            product TEXT,
            sales INTEGER,
            PRIMARY KEY(date, product)
        )
    """)
    conn.commit()

    # Insert data from CSV into database
    if not df.empty:
        for index, row in df.iterrows():
            cursor.execute("""
                INSERT OR REPLACE INTO sales (date, product, sales)
                VALUES (?, ?, ?)
            """, (row['date'], row['product'], row['sales']))
        conn.commit()
        logging.info("Sales data inserted into database.")
        print("Sales data inserted into database.")
    else:
        print("No data to insert.")

except Exception as e:
    logging.error(f"Error updating database: {e}")
    print(f"Error updating database: {e}")

finally:
    conn.close()
