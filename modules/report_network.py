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

    # === System Information ===
    system_info = data.get("system_info", {})
    if system_info:
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Local System Information", ln=True)
        pdf.set_font("Arial", "", 12)
        fields = [
            ("Hostname", "hostname"),
            ("IP Address", "ip_address"),
            ("OS", "os"),
            ("OS Version", "os_version"),
            ("Architecture", "architecture"),
            ("CPU Cores", "cpu_cores"),
            ("CPU Threads", "cpu_threads"),
            ("CPU Usage", "cpu_usage_percent"),
            ("Total RAM", "memory_total_gb"),
            ("Used RAM", "memory_used_gb"),
            ("RAM Usage", "memory_usage_percent")
        ]
        for label, key in fields:
            pdf.cell(0, 8, f"{label}: {system_info.get(key, 'N/A')}", ln=True)
        pdf.ln(2)

        # Disk Info
        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 8, "Disk Partitions:", ln=True)
        pdf.set_font("Arial", "", 12)
        for disk in system_info.get("disks", []):
            total = disk.get("total_gb", 0)
            used = disk.get("used_gb", 0)
            usage_pct = round((used / total) * 100, 1) if total else 0
            mount = f"{disk.get('device')} ({disk.get('mountpoint')})"
            pdf.cell(0, 8, f"{mount} - {used}/{total} GB ({usage_pct}%)", ln=True)

        pdf.ln(2)

        # Network Interfaces
        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 8, "Network Interfaces:", ln=True)
        pdf.set_font("Arial", "", 12)
        for iface in system_info.get("network_interfaces", []):
            name = iface.get("interface", "Unknown")
            status = "UP" if iface.get("is_up") else "DOWN"
            speed = iface.get("speed_mbps", "N/A")
            pdf.cell(0, 8, f"{name} ({status}, {speed} Mbps)", ln=True)
            for addr in iface.get("addresses", []):
                pdf.cell(0, 8, f"  {addr.get('family')}: {addr.get('address')} (Mask: {addr.get('netmask', 'None')})", ln=True)
        pdf.ln(10)

    # === Router Info ===
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

    # === Connected Devices ===
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Connected Devices", ln=True)
    pdf.set_font("Arial", "", 12)

    devices = data.get("network_devices", [])
    if devices:
        for i, device in enumerate(devices, start=1):
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, f"Device {i}", ln=True)
            pdf.set_font("Arial", "", 12)
            pdf.cell(0, 8, f"IP Address: {device.get('ip', 'N/A')}", ln=True)
            pdf.cell(0, 8, f"Hostname: {device.get('hostname', 'N/A')}", ln=True)
            pdf.cell(0, 8, f"Open Ports: {device.get('open_ports', [])}", ln=True)

            weak = device.get("weak_services", [])
            if weak:
                pdf.set_text_color(255, 0, 0)
                pdf.cell(0, 8, f"Weak Services: {weak}", ln=True)
                pdf.set_text_color(0, 0, 0)
            else:
                pdf.cell(0, 8, "Weak Services: None", ln=True)
            pdf.ln(5)
    else:
        pdf.cell(0, 8, "No connected devices found.", ln=True)

    # === Save PDF ===
    os.makedirs("reports", exist_ok=True)
    base_name = os.path.basename(json_path).replace(".json", ".pdf")
    report_path = os.path.join("reports", base_name)
    pdf.output(report_path)
    print(f"[✔] PDF report generated at: {report_path}")
