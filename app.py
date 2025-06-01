from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import pandas as pd
from generator import generate_payslip
from emailer import send_email
import json
from datetime import datetime
from sklearn.ensemble import IsolationForest

app = Flask(__name__)

# Load config
with open("config.json") as f:
    config = json.load(f)

DB_PATH = "database.db"

# Ensure database exists
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            basic REAL,
            hra REAL,
            allowance REAL,
            pf REAL,
            tax REAL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return redirect(url_for('add_employee'))

@app.route("/add", methods=["GET", "POST"])
def add_employee():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        basic = float(request.form['basic'])
        hra = float(request.form['hra'])
        allowance = float(request.form['allowance'])
        pf = float(request.form['pf'])
        tax = float(request.form['tax'])

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO employees (name, email, basic, hra, allowance, pf, tax) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (name, email, basic, hra, allowance, pf, tax))
        conn.commit()
        conn.close()
        return redirect(url_for('list_employees'))

    return render_template("form.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_employee(id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        basic = float(request.form['basic'])
        hra = float(request.form['hra'])
        allowance = float(request.form['allowance'])
        pf = float(request.form['pf'])
        tax = float(request.form['tax'])

        c.execute("""
            UPDATE employees SET name=?, email=?, basic=?, hra=?, allowance=?, pf=?, tax=?
            WHERE id=?
        """, (name, email, basic, hra, allowance, pf, tax, id))
        conn.commit()
        conn.close()
        return redirect(url_for('list_employees'))

    c.execute("SELECT * FROM employees WHERE id=?", (id,))
    employee = c.fetchone()
    conn.close()
    return render_template("form.html", employee=employee)

@app.route("/delete/<int:id>")
def delete_employee(id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM employees WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('list_employees'))

@app.route("/employees")
def list_employees():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM employees", conn)
    conn.close()
    return render_template("list.html", employees=df.to_dict(orient="records"))

@app.route("/generate")
def generate():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM employees", conn)
    conn.close()

    # Anomaly detection
    features = df[["basic", "hra", "allowance", "pf", "tax"]]
    model = IsolationForest(contamination=0.1, random_state=42)
    preds = model.fit_predict(features)
    df["anomaly"] = preds

    anomalies = df[df["anomaly"] == -1]
    normal_df = df[df["anomaly"] != -1]

    month_year = datetime.now().strftime("%B %Y")

    for _, row in normal_df.iterrows():
        employee_data = {
            "name": row["name"],
            "email": row["email"],
            "basic": float(row["basic"]),
            "hra": float(row["hra"]),
            "allowance": float(row["allowance"]),
            "pf": float(row["pf"]),
            "tax": float(row["tax"])
        }
        pdf_path = generate_payslip(employee_data, month_year)
        send_email(employee_data["email"], employee_data["name"], pdf_path, config, month_year)

    if anomalies.empty:
        return f"Payslips for {month_year} generated and sent successfully. <a href='/employees'>Back to Employees</a>"
    else:
        return render_template("anomalies.html", anomalies=anomalies)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
