# 🧾 Payroll Automation System with ML-Based Anomaly Detection

A Python-based payroll automation system that generates PDF payslips and emails them to employees via a Flask admin panel. Includes ML-powered anomaly detection to automatically skip suspicious salary configurations.

---

## 🚀 Features

- 🧑‍💼 Add, edit, and delete employee records via a web UI (Flask)
- 📄 Generate professional PDF payslips using `reportlab`
- 📧 Automatically email payslips to employees using SMTP
- ⚠️ Detect anomalies in salary data using `IsolationForest` (ML)
- 🗃️ Store data securely in a local SQLite database
- 🧠 Smart filtering to prevent incorrect payroll processing

---

## 🛠 Tech Stack

- **Backend**: Python, Flask
- **Database**: SQLite
- **PDF Generation**: ReportLab
- **Email Service**: smtplib (Gmail SMTP)
- **ML Anomaly Detection**: Scikit-learn (`IsolationForest`)
- **Other Libraries**: Pandas, NumPy

---

