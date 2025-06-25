# modules/report_phishing.py

from fpdf import FPDF
from datetime import datetime
import os

def generate_phishing_analysis_pdf(email_content, findings):
    # Validate inputs
    if not email_content:
        email_content = "[No email content provided]"
    if not findings or not isinstance(findings, list):
        findings = ["No findings available."]

    # Setup filename and path
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"phishing_analysis_{timestamp}.pdf"
    report_dir = os.path.join("reports")
    os.makedirs(report_dir, exist_ok=True)
    filepath = os.path.join(report_dir, filename)

    try:
        # Create PDF
        pdf = FPDF()
        pdf.add_page()

        # Use only ASCII-safe Arial font
        font_family = "Arial"

        # Title
        pdf.set_font(font_family, size=16)
        pdf.cell(0, 10, "Phishing Email Analysis Report", ln=True, align="C")

        # Metadata
        pdf.set_font(font_family, size=12)
        pdf.ln(10)
        pdf.cell(0, 10, f"Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)

        # Email Content
        pdf.ln(8)
        pdf.set_font(font_family, size=14)
        pdf.cell(0, 10, "Email Content:", ln=True)
        pdf.set_font(font_family, size=12)
        pdf.multi_cell(0, 8, email_content)

        # Analysis Findings
        pdf.ln(6)
        pdf.set_font(font_family, size=14)
        pdf.cell(0, 10, "Analysis Findings:", ln=True)
        pdf.set_font(font_family, size=12)
        for finding in findings:
            # Remove any non-ASCII characters to avoid errors
            clean_finding = ''.join(c for c in finding if ord(c) < 128)
            pdf.multi_cell(0, 8, f"- {clean_finding}")

        # Save PDF
        pdf.output(filepath)
        print(f"[INFO] PDF successfully saved at {filepath}")
        return filename

    except Exception as e:
        print(f"[ERROR] Failed to save PDF: {e}")
        raise e
