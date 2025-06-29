from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory, flash
import os
from datetime import datetime
from modules.network_scanner import run_network_scan, get_local_system_info, save_results_to_file
from modules.web_scanner import scan_website, save_web_results_to_file
from modules.report_network import generate_network_report
from modules.report_web import generate_web_report
from modules.phishing_module import generate_phishing_email
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from modules.report_phishing import generate_phishing_analysis_pdf

main = Blueprint(
    "main",
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

REPORTS_DIR = os.path.join(os.getcwd(), "reports")
LOG_FILE = os.path.join("logs", "feedback.txt")

# Utility to log to feedback.txt
def log_feedback(entry):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} {entry}\n\n")

# ---------------- HOME ----------------
@main.route("/")
def home():
    return render_template("index.html")

# ------------- NETWORK SCANNER -------------
@main.route("/network_scanner", methods=["GET"])
def network_scanner():
    return render_template("network_scanner.html", results=None)

@main.route("/run_network_scan", methods=["POST"])
def run_network_scan_route():
    try:
        scan_results = run_network_scan()
        return render_template("network_scanner.html", results=scan_results)
    except Exception as e:
        log_feedback(f"[ERROR] Network Scan Failed: {str(e)}")
        return render_template("network_scanner.html", results=None)

# ---------------- WEB SCANNER ----------------
@main.route("/web_scanner", methods=["GET"])
def web_scanner():
    return render_template("web_scanner.html", results=None, error=None)

@main.route("/run_web_scan", methods=["POST"])
def run_web_scan():
    url = request.form.get("url")

    if not url:
        return render_template("web_scanner.html", results=None, error="Please provide a valid URL.")

    results = scan_website(url)

    if "error" in results:
        log_feedback(f"[ERROR] Web Scan for {url} failed: {results['error']}")

    return render_template("web_scanner.html", results=results, error=results.get("error"))

# ---------------- REPORTS ----------------
@main.route("/reports")
def reports_dashboard():
    report_dir = os.path.join("reports")
    all_reports = os.listdir(report_dir)

    network_reports = [r for r in all_reports if r.startswith("network_")]
    web_reports = [r for r in all_reports if r.startswith("web_")]
    phishing_reports = [r for r in all_reports if r.startswith("phishing_analysis_")]

    return render_template(
        "reports.html",
        network_reports=network_reports,
        web_reports=web_reports,
        phishing_reports=phishing_reports
    )

@main.route("/generate_report", methods=["POST"])
def generate_report():
    report_type = request.form.get("report_type")
    json_file = request.form.get("json_file")

    try:
        if report_type == "network":
            generate_network_report(os.path.join("data/network", json_file))
        elif report_type == "web":
            generate_web_report(os.path.join("data/web", json_file))
        elif report_type == "phishing":
            generate_phishing_analysis_pdf(
                json_path=os.path.join("data/phishing", json_file)
            )
    except Exception as e:
        log_feedback(f"[ERROR] Report generation failed for {report_type}: {str(e)}")

    return redirect(url_for("main.reports_dashboard"))

@main.route("/reports/<path:filename>")
def download_report(filename):
    return send_from_directory(REPORTS_DIR, filename, as_attachment=True)

# -------------- FEEDBACK FORM --------------
@main.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        if name and message:
            log_feedback(f"[FEEDBACK] From: {name} ({email})\nMessage: {message}")
            flash("Thank you for your feedback!", "success")
        else:
            flash("Name and message are required.", "error")

        return redirect(url_for("main.feedback"))

    return render_template("feedback.html")

# ---------------- PHISHING EMAIL GENERATOR ----------------
@main.route("/phishing_awareness", methods=["GET", "POST"])
def phishing_awareness():
    email = None
    if request.method == "POST":
        email = generate_phishing_email()
    return render_template("phishing_awareness.html", email=email)

# ---------------- PHISHING EMAIL ANALYZER ----------------
@main.route("/analyze_email", methods=["POST"])
def analyze_email():
    content = request.form.get("email_content")
    findings = []

    if not content:
        findings.append("No content provided.")
        content = "[No content provided]"
    else:
        lower_content = content.lower()

        if "click here" in lower_content or "login" in lower_content:
            findings.append("Suspicious links or login prompts detected.")
        if "urgent" in lower_content or "immediately" in lower_content:
            findings.append("Urgency or pressure tactics used.")
        if "verify your account" in lower_content:
            findings.append("Request for account verification is common in phishing.")
        if "password" in lower_content:
            findings.append("Mentions of password changes or resets.")
        if "attachment" in lower_content:
            findings.append("Mentions of attachments—beware of malware.")
        if "unsubscribe" not in lower_content and ("marketing" in lower_content or "promotion" in lower_content):
            findings.append("No unsubscribe link in a marketing-style message.")
        if "http://" in lower_content and "https://" not in lower_content:
            findings.append("Insecure HTTP link detected.")

        try:
            analyzer = SentimentIntensityAnalyzer()
            scores = analyzer.polarity_scores(content)

            if scores["neg"] > 0.4:
                findings.append("Strong negative tone — potential fear/scare tactic.")
            if scores["pos"] > 0.4 and any(word in lower_content for word in ["congratulations", "winner", "prize", "offer"]):
                findings.append("Positive tone with tempting words — could be bait.")
            if scores["compound"] < -0.5:
                findings.append("Overall threatening or hostile tone.")
        except Exception as e:
            findings.append("Sentiment analysis failed.")
            log_feedback(f"[ERROR] VADER analysis failed: {str(e)}")

    if not findings:
        findings = ["No obvious phishing indicators found — but stay cautious."]

    try:
        generate_phishing_analysis_pdf(content, findings)
    except Exception as e:
        log_feedback(f"[ERROR] PDF generation failed: {str(e)}")

    return render_template(
        "phishing_awareness.html",
        analysis={"findings": findings},
        email=None
    )

# ---------------- CYBER HYGIENE ----------------
@main.route("/cyber_hygiene")
def cyber_hygiene():
    return render_template("cyber_hygiene.html")
