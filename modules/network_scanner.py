import nmap
import json
import os
from datetime import datetime
import platform
import re

def get_default_gateway():
    """Detect the default gateway IP based on OS."""
    system = platform.system()
    try:
        if system == "Windows":
            output = os.popen("ipconfig").read()
            match = re.search(r"Default Gateway[ .:]*([\d\.]+)", output)
            return match.group(1) if match else None
        elif system in ["Linux", "Darwin"]:
            output = os.popen("ip route | grep default").read()
            return output.split()[2] if output else None
    except Exception:
        return None
    return None

def check_router_security(gateway_ip):
    """Scan router IP for open ports and weak services."""
    nm = nmap.PortScanner()
    nm.scan(hosts=gateway_ip, arguments='-p 21,23,80,443,8080')

    router_result = {
        "ip": gateway_ip,
        "open_ports": [],
        "weak_services": []
    }

    if gateway_ip in nm.all_hosts() and 'tcp' in nm[gateway_ip]:
        for port, details in nm[gateway_ip]['tcp'].items():
            router_result["open_ports"].append(port)
            if details["name"] in ['ftp', 'telnet', 'http']:
                router_result["weak_services"].append((port, details["name"]))

    return router_result

def scan_network(subnet='192.168.1.0/24'):
    """Perform a TCP SYN scan on the given subnet."""
    nm = nmap.PortScanner()
    nm.scan(hosts=subnet, arguments='-sS -T4')
    
    results = []
    for host in nm.all_hosts():
        if 'tcp' not in nm[host]:
            continue

        open_ports = [port for port in nm[host]['tcp'] if nm[host]['tcp'][port]['state'] == 'open']
        weak_services = []
        for port in open_ports:
            service = nm[host]['tcp'][port]['name']
            if service in ['ftp', 'telnet', 'smb', 'rdp']:
                weak_services.append((port, service))
        
        results.append({
            'ip': host,
            'hostname': nm[host].hostname(),
            'open_ports': open_ports,
            'weak_services': weak_services
        })

    return results

def save_results_to_file(data, scan_type="network"):
    """Save scan results to a JSON file in data/network/"""
    save_dir = os.path.join("data", scan_type)
    os.makedirs(save_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{scan_type}_scan_{timestamp}.json"
    full_path = os.path.join(save_dir, filename)

    with open(full_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"[✔] Scan results saved to {full_path}")
    return full_path

def run_network_scan(subnet='192.168.1.0/24'):
    """Main function to run the full network scan pipeline."""
    output = {
        "router_scan": {},
        "network_devices": []
    }

    gateway_ip = get_default_gateway()
    if gateway_ip:
        output["router_scan"] = check_router_security(gateway_ip)

    output["network_devices"] = scan_network(subnet=subnet)
    save_results_to_file(output, scan_type="network")

    return output  # Dict returned for use in Flask view

# Prevent running scans on import
if __name__ == '__main__':
    scan_data = run_network_scan()
    print(json.dumps(scan_data, indent=4))
