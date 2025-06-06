from fpdf import FPDF
import json
import os

def generate_web_report(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Web Application Scan Report", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "URL Scanned:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, data.get("url", "N/A"), ln=True)
    pdf.ln(5)

    # Headers
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "HTTP Headers:", ln=True)
    pdf.set_font("Arial", "", 12)
    headers = data.get("headers", {})
    if headers:
        for k, v in headers.items():
            pdf.cell(0, 8, f"{k}: {v}", ln=True)
    else:
        pdf.cell(0, 8, "No headers found.", ln=True)
    pdf.ln(5)

    # Technologies
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Detected Technologies:", ln=True)
    pdf.set_font("Arial", "", 12)
    techs = data.get("technologies", [])
    if techs:
        for tech in techs:
            pdf.cell(0, 8, f"- {tech}", ln=True)
    else:
        pdf.cell(0, 8, "None", ln=True)
    pdf.ln(5)

    # SSL Info
    ssl_info = data.get("ssl_info", {})
    if ssl_info:
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "SSL Certificate Info:", ln=True)
        pdf.set_font("Arial", "", 12)

        issuer = ssl_info.get("issuer", [])
        subject = ssl_info.get("subject", [])

        pdf.cell(0, 8, f"Issuer: {', '.join(['='.join(i) for i in issuer])}", ln=True)
        pdf.cell(0, 8, f"Subject: {', '.join(['='.join(s) for s in subject])}", ln=True)
        pdf.cell(0, 8, f"Valid From: {ssl_info.get('valid_from', 'N/A')}", ln=True)
        pdf.cell(0, 8, f"Valid Until: {ssl_info.get('valid_until', 'N/A')}", ln=True)
    else:
        pdf.cell(0, 8, "No SSL certificate info available.", ln=True)

    # Save Report
    os.makedirs("reports", exist_ok=True)
    base_name = os.path.basename(json_path).replace(".json", ".pdf")
    report_path = os.path.join("reports", base_name)
    pdf.output(report_path)
    print(f"[✔] Web PDF report generated at: {report_path}")
