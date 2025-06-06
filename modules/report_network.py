from fpdf import FPDF
import json
import os

def generate_network_report(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Network Scan Report", ln=True, align='C')
    pdf.ln(10)

    # Router Scan
    router = data.get("router_scan", {})
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Router Security Check", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Router IP: {router.get('ip', 'N/A')}", ln=True)
    pdf.cell(0, 8, f"Open Ports: {router.get('open_ports', [])}", ln=True)
    weak_services = router.get("weak_services", [])
    if weak_services:
        pdf.set_text_color(255, 0, 0)
        pdf.cell(0, 8, f"Weak Services: {weak_services}", ln=True)
        pdf.set_text_color(0, 0, 0)
    else:
        pdf.set_text_color(0, 128, 0)
        pdf.cell(0, 8, "No weak services detected on the router.", ln=True)
        pdf.set_text_color(0, 0, 0)

    pdf.ln(10)

    # Network Devices
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Connected Devices", ln=True)
    pdf.set_font("Arial", "", 12)

    for device in data.get("network_devices", []):
        pdf.cell(0, 8, f"IP: {device.get('ip', 'N/A')}", ln=True)
        pdf.cell(0, 8, f"Hostname: {device.get('hostname', '')}", ln=True)
        pdf.cell(0, 8, f"Open Ports: {device.get('open_ports', [])}", ln=True)
        if device.get("weak_services"):
            pdf.set_text_color(255, 0, 0)
            pdf.cell(0, 8, f"Weak Services: {device['weak_services']}", ln=True)
            pdf.set_text_color(0, 0, 0)
        else:
            pdf.cell(0, 8, "Weak Services: None", ln=True)
        pdf.ln(5)

    # Save PDF
    os.makedirs("reports", exist_ok=True)
    base_name = os.path.basename(json_path).replace(".json", ".pdf")
    report_path = os.path.join("reports", base_name)
    pdf.output(report_path)
    print(f"[✔] PDF report generated at: {report_path}")
