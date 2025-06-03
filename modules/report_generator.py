from fpdf import FPDF
import json
import os
from datetime import datetime

def generate_pdf_report(data_path):
    with open(data_path, 'r') as file:
        data = json.load(file)

    report_name = f"web_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    save_path = os.path.join("reports", report_name)
    os.makedirs("reports", exist_ok=True)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_title("Web Scanner Report")
    pdf.cell(200, 10, txt="Web Vulnerability Scan Report", ln=True, align='C')

    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Scanned URL: {data['url']}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="HTTP Headers:", ln=True)
    pdf.set_font("Arial", size=11)
    for k, v in data['headers'].items():
        pdf.cell(200, 8, txt=f"{k}: {v}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="Technologies Detected:", ln=True)
    pdf.set_font("Arial", size=11)
    techs = data.get("technologies", [])
    if techs:
        for tech in techs:
            pdf.cell(200, 8, txt=f"- {tech}", ln=True)
    else:
        pdf.cell(200, 8, txt="No technologies identified.", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="SSL Info:", ln=True)
    pdf.set_font("Arial", size=11)
    ssl_info = data.get("ssl_info", {})
    for k, v in ssl_info.items():
        pdf.multi_cell(0, 8, txt=f"{k}: {v}")

    pdf.output(save_path)
    print(f"[✔] PDF report saved at: {save_path}")

# Example usage:
if __name__ == "__main__":
    latest = sorted(os.listdir("data"))[-1]
    generate_pdf_report(os.path.join("data", latest))
