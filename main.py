import sqlite3
import pandas as pd
import json
from datetime import datetime
from generator import generate_payslip
from emailer import send_email

# === Load Configuration ===
with open("config.json", "r") as f:
    config = json.load(f)

# === Load Data from SQLite ===
conn = sqlite3.connect("database.db")
df = pd.read_sql_query("SELECT * FROM employees", conn)
conn.close()

# === Process Each Employee ===
month_year = datetime.now().strftime("%B %Y")
for index, row in df.iterrows():
    try:
        employee_data = {
            "name": row["name"],
            "email": row["email"],
            "basic": float(row["basic"]),
            "hra": float(row["hra"]),
            "allowance": float(row["allowance"]),
            "pf": float(row["pf"]),
            "tax": float(row["tax"])
        }

        # Generate PDF Payslip
        pdf_path = generate_payslip(employee_data, month_year)

        # Send Email with PDF
        send_email(employee_data["email"], employee_data["name"], pdf_path, config, month_year)

    except Exception as err:
        print(f"[X] Error processing row {index + 1}: {err}")
