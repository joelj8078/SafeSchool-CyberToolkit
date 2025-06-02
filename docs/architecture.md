# docs/generate_architecture_doc.py
content = """
# SafeSchool Cyber Hygiene Toolkit – Architecture Plan

## 📁 Folder Structure
SafeSchool-CyberToolkit/
├── modules/                  # Core scanner scripts (network/web)
│   └── network_scanner.py
├── data/                     # Scan results, checklist JSON files
│   ├── scan_results_*.json
│   └── network_checklist.json
├── templates/                # Flask HTML templates (later)
├── static/                   # CSS/JS/images (later)
├── app.py                    # Main Flask app (to be built)
├── requirements.txt          # Python dependencies
└── docs/
    └── architecture.md       # This documentation file

## 🔧 Components
- Network scanner: Detects devices, ports, weak services using Nmap
- JSON Output: Saves device/port data to file
- Checklist: JSON tips for school admins
- Web app (Flask): To be integrated for usability

## 🧠 Data Flow
User → [Scanner] → [JSON Output] → [Flask Display / Report]
"""

# Save to file
with open("docs/architecture.md", "w") as f:
    f.write(content.strip())

print("[✔] Saved architecture plan to docs/architecture.md")
