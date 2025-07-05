# 1. 🛡️ SafeSchool Cyber Toolkit

**A Cyber Awareness and Risk Scanning Dashboard for Schools**

---

## 1.1. 📌 Overview

The **SafeSchool Cyber Toolkit** is a full-stack, modular, web-based cybersecurity dashboard designed for schools and educational institutions. It helps non-technical users like school IT staff, teachers, and students:
- Detect insecure devices and router issues in local networks
- Perform basic website vulnerability assessments
- Simulate and analyze phishing emails
- Learn cybersecurity hygiene best practices
- Generate professional PDF reports with charts and visualizations

This project was built as part of a final-year internship and aims to promote cybersecurity awareness and proactive risk assessment in low-resource educational environments.

![Image Alt](https://github.com/joelj8078/SafeSchool-CyberToolkit/blob/0188f31974de421051491134f44f526dfa68b1dd/Screenshot%202025-07-05%20193244.png)

---

## 1.2. 🎯 Features

### 1.2.1. ✅ Network Scanner
- Scans local IP ranges and routers
- Detects open ports and weak services
- Displays live system information (CPU, RAM, disk, interfaces)
- Saves scan results as JSON
- Generates PDF reports

### 1.2.2. ✅ Web Scanner
- Analyzes SSL certificates, HTTP headers, technologies, sensitive files
- Detects open redirect and CMS vulnerabilities
- Performs WHOIS and performance analysis
- Visualizes results using radar charts
- Outputs JSON & PDF reports

### 1.2.3. ✅ Phishing Awareness
- **Phishing Email Generator** – Simulates real-looking phishing emails
- **Phishing Analyzer** – Detects red flags in pasted email content
- Generates phishing analysis reports in PDF

### 1.2.4. ✅ Dashboard & Reporting
- Central UI with separate pages for each scanner
- Categorized report viewer with download links
- Responsive design using Bootstrap 5

### 1.2.5. ✅ Feedback & Cyber Hygiene
- User feedback form (logs saved in `logs/feedback.txt`)
- Tips for safe browsing, strong passwords, email caution, etc.

---

## 1.3. 🖥️ Tech Stack

| Layer        | Technology                            |
|--------------|----------------------------------------|
| Frontend     | HTML, CSS, Bootstrap 5, Jinja Templates |
| Backend      | Python 3, Flask (with Blueprints)       |
| Modules      | `nmap`, `psutil`, `socket`, `platform`, `whois`, `requests`, `matplotlib`, `reportlab` |
| Reporting    | JSON files, Radar Charts, PDF generation |
| Storage      | `/data/`, `/reports/`, `/logs/` folders |

---

## 1.4. 📁 Project Structure

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

## 1.5. 🚀 Getting Started

### 1.5.1. Clone the Repository
```bash
git clone https://github.com/your-username/SafeSchoolCyberToolkit.git
cd SafeSchoolCyberToolkit
```

### 1.5.2. Create and Activate Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 1.5.3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 1.5.4. Run the App
```bash
python app.py
```
The toolkit will be available at: http://localhost:5000
---

## 1.6. 📊 Usage Instructions

### 1.6.1. 📡 Network Scanner
- Go to `/network_scanner`

- Click “Scan” to detect local devices and system info

- View results and download report

### 1.6.2. 🌐 Web Scanner
- Go to `/web_scanner`

- Enter a website URL and click “Scan”

- Review SSL info, headers, technologies, radar chart

- Download security report as PDF

### 1.6.3. 🧪 Phishing Awareness
- Go to `/phishing_awareness`

- Use the generator to simulate emails or paste suspicious content to analyze

- Generate and download phishing report

### 1.6.4. 📁 Reports
- Go to `/reports`

- Choose report type and select JSON file

- View summary and download PDF

### 1.6.5. 💡 Cyber Hygiene
- Go to `/cyber_hygiene` for safe internet practices

### 1.6.6. 📝 Submit Feedback
- Visit `/feedback` to log bugs, suggestions, or experience





