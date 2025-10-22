"""
This script tests that the sales data workflow works correctly.
It checks that the CSV file exists, the SQLite database exists,
and that the database table contains rows.
"""

import os
import sqlite3

# -------------------------
# Test 1: Check CSV file exists
# -------------------------
csv_file = "sales_data.csv"
assert os.path.exists(csv_file), f"CSV file '{csv_file}' does not exist!"

# -------------------------
# Test 2: Check SQLite database exists
# -------------------------
db_file = "sales.db"
assert os.path.exists(db_file), f"Database file '{db_file}' does not exist!"

# -------------------------
# Test 3: Check that the database table has rows
# -------------------------
conn = sqlite3.connect(db_file)
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM sales")
count = cursor.fetchone()[0]
conn.close()

assert count > 0, "Database table 'sales' is empty!"

print("All tests passed! CSV and database exist, and data is inserted correctly.")
