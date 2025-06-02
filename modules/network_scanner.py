import nmap
import json
import os
from datetime import datetime

def scan_network(subnet='192.168.1.0/24'):
    nm = nmap.PortScanner()
    print(f"Scanning subnet: {subnet} ...")
    
    nm.scan(hosts=subnet, arguments='-sS -T4')
    results = []

    for host in nm.all_hosts():
        if 'tcp' in nm[host]:
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

def save_results_to_file(results):
    # Create 'data' directory if it doesn't exist
    os.makedirs("data", exist_ok=True)

    # Generate a timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/scan_results_{timestamp}.json"

    # Save as JSON
    with open(filename, "w") as f:
        json.dump(results, f, indent=4)
    
    print(f"\n[✔] Scan results saved to {filename}")

if __name__ == '__main__':
    scan_results = scan_network()
    for device in scan_results:
        print(f"\n[+] IP: {device['ip']}")
        print(f"    Hostname: {device['hostname']}")
        print(f"    Open Ports: {device['open_ports']}")
        print(f"    Weak Services: {device['weak_services']}")

        save_results_to_file(scan_results)
