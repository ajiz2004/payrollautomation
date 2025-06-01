import smtplib
import os
from email.message import EmailMessage

def send_email(to_email, employee_name, pdf_path, config, month_year):
    msg = EmailMessage()
    msg['Subject'] = f"Payslip for {month_year} - {config['company_name']}"
    msg['From'] = config['sender_email']
    msg['To'] = to_email

    # Email body
    msg.set_content(
        f"""Dear {employee_name},

Please find attached your payslip for {month_year}.

Best regards,
{config['company_name']} Payroll Team
"""
    )

    with open(pdf_path, 'rb') as f:
        file_data = f.read()
        filename = os.path.basename(pdf_path)
        msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=filename)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(config['sender_email'], config['sender_password'])
            smtp.send_message(msg)
            print(f"[✓] Sent payslip to {to_email}")
    except Exception as e:
        print(f"[X] Failed to send to {to_email}: {e}")
