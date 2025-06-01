from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
import os

def generate_payslip(employee, month_year):
    name = employee["name"]
    basic = employee["basic"]
    hra = employee["hra"]
    allowance = employee["allowance"]
    pf = (employee["pf"] / 100) * basic
    tax = (employee["tax"] / 100) * basic
    net_salary = basic + hra + allowance - pf - tax

    filename = f"{name.replace(' ', '_')}_Payslip_{month_year.replace(' ', '')}.pdf"
    file_path = os.path.join("output", "payslips", filename)

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    margin = 1 * inch
    y = height - margin

    # Outer border (margin box)
    c.setStrokeColor(colors.lightgrey)
    c.setLineWidth(1)
    c.rect(margin / 2, margin / 2, width - margin, height - margin)

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, y, "Ajiz Infotech")
    y -= 25
    c.setFont("Helvetica", 12)
    c.drawString(margin, y, f"Payslip for: {month_year}")
    y -= 20
    c.drawString(margin, y, f"Employee Name: {name}")
    y -= 40

    # Earnings
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Earnings")
    y -= 20
    c.setFont("Helvetica", 12)
    c.drawString(margin + 20, y, "Basic Salary:")
    c.drawString(width - margin - 100, y, f"INR {basic:,.2f}")
    y -= 20
    c.drawString(margin + 20, y, "HRA:")
    c.drawString(width - margin - 100, y, f"INR {hra:,.2f}")
    y -= 20
    c.drawString(margin + 20, y, "Other Allowance:")
    c.drawString(width - margin - 100, y, f"INR {allowance:,.2f}")

    # Deductions
    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Deductions")
    y -= 20
    c.setFont("Helvetica", 12)
    c.drawString(margin + 20, y, f"PF Deduction ({employee['pf']}%):")
    c.drawString(width - margin - 100, y, f"INR {pf:,.2f}")
    y -= 20
    c.drawString(margin + 20, y, f"Tax Deduction ({employee['tax']}%):")
    c.drawString(width - margin - 100, y, f"INR {tax:,.2f}")

    # Net Salary
    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Net Salary")
    y -= 20
    c.setFont("Helvetica", 12)
    c.drawString(margin + 20, y, "Total Payable:")
    c.drawString(width - margin - 100, y, f"INR {net_salary:,.2f}")

    # Footer
    y -= 50
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(margin, y, "This is a system-generated payslip. No signature required.")

    c.save()
    return file_path
