# 🛡️ SafeSchool Cyber Toolkit

**A Cyber Awareness and Risk Scanning Dashboard for Schools**

---

## 📌 Overview

The **SafeSchool Cyber Toolkit** is a full-stack, modular, web-based cybersecurity dashboard designed for schools and educational institutions. It helps non-technical users like school IT staff, teachers, and students:
- Detect insecure devices and router issues in local networks
- Perform basic website vulnerability assessments
- Simulate and analyze phishing emails
- Learn cybersecurity hygiene best practices
- Generate professional PDF reports with charts and visualizations

This project was built as part of a final-year internship and aims to promote cybersecurity awareness and proactive risk assessment in low-resource educational environments.

---

## 🎯 Features

### ✅ Network Scanner
- Scans local IP ranges and routers
- Detects open ports and weak services
- Displays live system information (CPU, RAM, disk, interfaces)
- Saves scan results as JSON
- Generates PDF reports

### ✅ Web Scanner
- Analyzes SSL certificates, HTTP headers, technologies, sensitive files
- Detects open redirect and CMS vulnerabilities
- Performs WHOIS and performance analysis
- Visualizes results using radar charts
- Outputs JSON & PDF reports

### ✅ Phishing Awareness
- **Phishing Email Generator** – Simulates real-looking phishing emails
- **Phishing Analyzer** – Detects red flags in pasted email content
- Generates phishing analysis reports in PDF

### ✅ Dashboard & Reporting
- Central UI with separate pages for each scanner
- Categorized report viewer with download links
- Responsive design using Bootstrap 5

### ✅ Feedback & Cyber Hygiene
- User feedback form (logs saved in `logs/feedback.txt`)
- Tips for safe browsing, strong passwords, email caution, etc.

---

## 🖥️ Tech Stack

| Layer        | Technology                            |
|--------------|----------------------------------------|
| Frontend     | HTML, CSS, Bootstrap 5, Jinja Templates |
| Backend      | Python 3, Flask (with Blueprints)       |
| Modules      | `nmap`, `psutil`, `socket`, `platform`, `whois`, `requests`, `matplotlib`, `reportlab` |
| Reporting    | JSON files, Radar Charts, PDF generation |
| Storage      | `/data/`, `/reports/`, `/logs/` folders |

---

## 📁 Project Structure

SafeSchoolToolkit/
│
├── app.py
├── requirements.txt
├── README.md
│
├── app/
│ ├── init.py
│ ├── routes.py
│ └── templates/
│   ├── index.html
│   ├── network_scanner.html
│   ├── web_scanner.html
│   ├── phishing_awareness.html
│   ├── reports.html
│   ├── feedback.html
│   └── cyber_hygiene.html
│
├── modules/
│ ├── network_scanner.py
│ ├── web_scanner.py
│ ├── phishing_module.py
│ ├── report_network.py
│ ├── report_web.py
│ └── report_phishing.py
│
├── data/
│ ├── network/
│ ├── web/
│ └── phishing/
│
├── reports/
│ ├── network/
│ ├── web/
│ └── phishing/
│
├── logs/
│ └── feedback.txt
│
└── static/
└── images/


---

🚀 Getting Started
Follow these steps to install and run the project:

1. Clone the Repository
git clone https://github.com/your-username/SafeSchoolCyberToolkit.git
cd SafeSchoolCyberToolkit

2. Create and Activate a Virtual Environment (Recommended)
On macOS/Linux:
python3 -m venv venv
source venv/bin/activate




