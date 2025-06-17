from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory
import os
from modules.network_scanner import (
    run_network_scan,
    get_local_system_info,
    save_results_to_file
)
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
    scan_results = run_network_scan()
    return render_template("network_scanner.html", results=scan_results)

# -------------------- WEB SCANNER --------------------

@main.route("/web_scanner", methods=["GET"])
def web_scanner():
    return render_template("web_scanner.html", results=None, error=None)

@main.route("/run_web_scan", methods=["POST"])
def run_web_scan():
    url = request.form.get("url")

    if not url:
        return render_template("web_scanner.html", results=None, error="Please provide a valid URL.")

    results = scan_website(url)

    # Save results only if scan succeeded
    if "error" not in results:
        save_web_results_to_file(results)

    return render_template("web_scanner.html", results=results, error=results.get("error"))

# -------------------- REPORTS --------------------

@main.route("/reports")
def reports_dashboard():
    reports = [f for f in os.listdir(REPORTS_DIR) if f.endswith(".pdf")]
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
