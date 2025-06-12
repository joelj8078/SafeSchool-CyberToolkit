from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory
import os
from datetime import datetime
from modules.network_scanner import scan_network, get_default_gateway, check_router_security, save_results_to_file
from modules.web_scanner import scan_website, save_web_results_to_file
from modules.report_network import generate_network_report
from modules.report_web import generate_web_report

main = Blueprint("main", __name__)

REPORTS_DIR = os.path.join(os.getcwd(), "reports")

# -------------------- HOME --------------------

@main.route("/")
def home():
    return render_template("index.html")

# -------------------- NETWORK SCANNER --------------------

@main.route("/network_scanner", methods=["GET"])
def network_scanner():
    return render_template("network_scanner.html", results=None)

@main.route("/run_network_scan", methods=["POST"])
def run_network_scan_route():
    subnet = request.form.get("target") or "192.168.1.0/24"

    gateway_ip = get_default_gateway()
    router_results = check_router_security(gateway_ip) if gateway_ip else {}

    network_devices = scan_network(subnet=subnet)
    full_results = {
        "router_scan": router_results,
        "network_devices": network_devices
    }

    save_results_to_file(full_results, scan_type="network")
    return render_template("network_scanner.html", results=full_results)

# -------------------- WEB SCANNER --------------------

@main.route("/web_scanner", methods=["GET"])
def web_scanner():
    return render_template("web_scanner.html", results=None, error=None)

@main.route("/run_web_scan", methods=["POST"])
def run_web_scan():
    url = request.form.get("url")  # match the HTML input name (not "target_url")
    
    if not url:
        return render_template("web_scanner.html", results=None, error="Please provide a target URL.")
    
    results = scan_website(url)  # your custom scanner logic
    save_web_results_to_file(results)  # if this saves to a JSON/PDF etc.
    
    return render_template("web_scanner.html", results=results, error=None)

# -------------------- REPORTS --------------------

@main.route("/reports")
def reports_dashboard():
    reports = [f for f in os.listdir(REPORT_DIR) if f.endswith(".pdf")]
    reports.sort(reverse=True)
    return render_template("reports.html", reports=reports)

@main.route("/generate_report", methods=["POST"])
def generate_report():
    report_type = request.form.get("report_type")
    json_file = request.form.get("json_file")

    if report_type == "network":
        generate_network_report(os.path.join("data/network", json_file))
    elif report_type == "web":
        generate_web_report(os.path.join("data/web", json_file))

    return redirect(url_for("main.reports_dashboard"))

@main.route("/reports/<path:filename>")
def download_report(filename):
    return send_from_directory(REPORTS_DIR, filename, as_attachment=True)
