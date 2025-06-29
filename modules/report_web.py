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

    # URL
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Scanned URL:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, data.get("url", "N/A"), ln=True)
    pdf.ln(5)

    # Performance
    perf = data.get("performance", {})
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Performance Metrics:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Response Time: {perf.get('response_time_ms', 'N/A')} ms", ln=True)
    pdf.cell(0, 8, f"Content Length: {perf.get('content_length_kb', 'N/A')} KB", ln=True)
    pdf.ln(5)

    # HTTP Headers
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "HTTP Headers:", ln=True)
    pdf.set_font("Arial", "", 12)
    headers = data.get("headers", {})
    if headers:
        for k, v in headers.items():
            pdf.multi_cell(0, 8, f"{k}: {v}")
    else:
        pdf.cell(0, 8, "No headers found.", ln=True)
    pdf.ln(5)

    # Security Headers
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Security Headers:", ln=True)
    pdf.set_font("Arial", "", 12)
    sec = data.get("security_headers", {})
    present = sec.get("present", [])
    missing = sec.get("missing", [])
    pdf.cell(0, 8, f"Present: {', '.join(present) if present else 'None'}", ln=True)
    pdf.cell(0, 8, f"Missing: {', '.join(missing) if missing else 'None'}", ln=True)
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
        pdf.cell(0, 8, "None detected.", ln=True)
    pdf.ln(5)

    # SSL Info
    ssl_info = data.get("ssl_info", {})
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "SSL Certificate Info:", ln=True)
    pdf.set_font("Arial", "", 12)
    if ssl_info and not ssl_info.get("error"):
        issuer = ssl_info.get("issuer", {})
        subject = ssl_info.get("subject", {})
        pdf.multi_cell(0, 8, f"Issuer: {', '.join([f'{k}={v}' for k,v in issuer.items()])}")
        pdf.multi_cell(0, 8, f"Subject: {', '.join([f'{k}={v}' for k,v in subject.items()])}")
        pdf.cell(0, 8, f"Valid From: {ssl_info.get('valid_from', 'N/A')}", ln=True)
        pdf.cell(0, 8, f"Valid Until: {ssl_info.get('valid_until', 'N/A')}", ln=True)
        pdf.cell(0, 8, f"Days Until Expiry: {ssl_info.get('expires_in_days', 'N/A')}", ln=True)
    else:
        pdf.cell(0, 8, f"Error: {ssl_info.get('error', 'No SSL info found.')}", ln=True)
    pdf.ln(5)

    # Sensitive Paths
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Sensitive Paths Found:", ln=True)
    pdf.set_font("Arial", "", 12)
    paths = data.get("sensitive_paths_found", [])
    if paths:
        for path in paths:
            pdf.cell(0, 8, f"- {path}", ln=True)
    else:
        pdf.cell(0, 8, "None discovered.", ln=True)
    pdf.ln(5)

    # Open Redirect
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Open Redirect Test:", ln=True)
    pdf.set_font("Arial", "", 12)
    redir = data.get("open_redirect_test", {})
    if redir.get("vulnerable"):
        pdf.cell(0, 8, f"Vulnerable! Redirects to: {redir.get('location', 'unknown')}", ln=True)
    elif redir.get("error"):
        pdf.cell(0, 8, f"Error: {redir['error']}", ln=True)
    else:
        pdf.cell(0, 8, "Not vulnerable.", ln=True)
    pdf.ln(5)

    # WHOIS Info
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Domain WHOIS Info:", ln=True)
    pdf.set_font("Arial", "", 12)
    whois_info = data.get("whois_info", {})
    if whois_info and not whois_info.get("error"):
        pdf.cell(0, 8, f"Domain: {whois_info.get('domain_name', 'N/A')}", ln=True)
        pdf.cell(0, 8, f"Registrar: {whois_info.get('registrar', 'N/A')}", ln=True)
        pdf.cell(0, 8, f"Created On: {whois_info.get('creation_date', 'N/A')}", ln=True)
        pdf.cell(0, 8, f"Expires On: {whois_info.get('expiration_date', 'N/A')}", ln=True)
    else:
        pdf.cell(0, 8, f"Error: {whois_info.get('error', 'WHOIS lookup failed')}", ln=True)
    pdf.ln(5)

    # Security Score
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Security Score:", ln=True)
    pdf.set_font("Arial", "", 12)
    score = data.get("security_score", "N/A")
    pdf.cell(0, 8, f"{score}/10", ln=True)
    pdf.ln(5)

    # Radar Chart (optional)
    radar_path = data.get("radar_chart")
    if radar_path and os.path.exists(radar_path):
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Security Radar Chart:", ln=True)
        pdf.image(radar_path, w=100)
        pdf.ln(10)

    # Save Report
    os.makedirs("reports", exist_ok=True)
    base_name = os.path.basename(json_path).replace(".json", ".pdf")
    report_path = os.path.join("reports", base_name)
    pdf.output(report_path)
    print(f"[✔] Web PDF report generated at: {report_path}")
