from flask import Flask, render_template, send_from_directory, request, redirect, url_for
import os
from modules.report_network import generate_network_report
from modules.report_web import generate_web_report

app = Flask(__name__)

REPORT_DIR = 'reports'

@app.route("/reports")
def reports_dashboard():
    # List all PDFs in reports/ folder
    reports = [f for f in os.listdir(REPORT_DIR) if f.endswith('.pdf')]
    reports.sort(reverse=True)
    return render_template("reports.html", reports=reports)

@app.route("/generate_report", methods=["POST"])
def generate_report():
    report_type = request.form.get("report_type")
    json_file = request.form.get("json_file")

    if report_type == "network":
        generate_network_report(os.path.join("data/network", json_file))
    elif report_type == "web":
        generate_web_report(os.path.join("data/web", json_file))

    return redirect(url_for('reports_dashboard'))

@app.route("/reports/<filename>")
def download_report(filename):
    return send_from_directory(REPORT_DIR, filename, as_attachment=True)
