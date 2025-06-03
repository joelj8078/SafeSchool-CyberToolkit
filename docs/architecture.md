# SafeSchool Cyber Toolkit - Architecture Plan (Week 1)

## 📁 Project Structure
SafeSchool-CyberToolkit/
│
├── modules/
│ └── network_scanner.py # Contains scanner logic using nmap, socket, and subprocess
│
├── data/
│ └── scan_results_<timestamp>.json # Auto-saved scan outputs in structured format
│
├── docs/
│ └── architecture.md # This architecture documentation
│
├── README.md # Project overview and usage instructions


## 🧱 Module Description

- **`network_scanner.py`**: Scans the local network (`192.168.x.0/24`) and router for:
  - Active devices
  - Open ports
  - Weak services (FTP, Telnet, HTTP, etc.)
  - Router-specific misconfigurations
  - Saves results to `data/` with timestamps

## 🧾 Output Format

All scan results are saved in a structured `.json` format like:

```json
{
  "router_ip": "192.168.1.1",
  "router_ports": [21, 23, 80, 443],
  "weak_services": [
    [21, "ftp"],
    [23, "telnet"]
  ],
  "devices": [
    {
      "ip": "192.168.1.1",
      "ports": [21, 80],
      "weak_services": [[21, "ftp"]]
    }
  ]
}


