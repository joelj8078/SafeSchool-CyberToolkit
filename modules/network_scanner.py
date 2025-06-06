import nmap
import json
import os
from datetime import datetime
import platform
import re

def scan_network(subnet='192.168.1.0/24'):
    nm = nmap.PortScanner()
    print(f"\n[+] Scanning subnet: {subnet} ...")
    
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

def get_default_gateway():
    system = platform.system()
    if system == "Windows":
        output = os.popen("ipconfig").read()
        match = re.search(r"Default Gateway . . . . . . . . . : ([\d\.]+)", output)
        if match:
            return match.group(1)
    elif system in ["Linux", "Darwin"]:
        output = os.popen("ip route | grep default").read()
        return output.split()[2] if output else None
    return None

def check_router_security(gateway_ip):
    print(f"\n[+] Scanning router at {gateway_ip} for misconfigurations...\n")
    nm = nmap.PortScanner()
    nm.scan(hosts=gateway_ip, arguments='-p 21,23,80,443,8080')

    router_result = {
        "ip": gateway_ip,
        "open_ports": [],
        "weak_services": []
    }

    if gateway_ip in nm.all_hosts():
        ports = list(nm[gateway_ip]['tcp'].keys())
        router_result["open_ports"] = ports

        for port in ports:
            service = nm[gateway_ip]['tcp'][port]['name']
            if service in ['ftp', 'telnet', 'http']:
                router_result["weak_services"].append((port, service))

        print(f"Router Open Ports: {router_result['open_ports']}")
        if router_result["weak_services"]:
            print(f"⚠️ Weak Services Found: {router_result['weak_services']}")
        else:
            print("✅ No weak services found on router.")
    else:
        print("❌ Failed to scan router IP.")
    
    return router_result

def save_results_to_file(data, scan_type="network"):
    # Create subfolder inside data/
    save_dir = os.path.join("data", scan_type)
    os.makedirs(save_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{scan_type}_scan_{timestamp}.json"
    full_path = os.path.join(save_dir, filename)

    with open(full_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"\n[✔] Scan results saved to {full_path}")

if __name__ == '__main__':
    full_scan_output = {
        "router_scan": {},
        "network_devices": []
    }

    router_ip = get_default_gateway()
    if router_ip:
        full_scan_output["router_scan"] = check_router_security(router_ip)
    else:
        print("❌ Could not detect router IP.")

    network_devices = scan_network()
    for device in network_devices:
        print(f"\n[+] IP: {device['ip']}")
        print(f"    Hostname: {device['hostname']}")
        print(f"    Open Ports: {device['open_ports']}")
        print(f"    Weak Services: {device['weak_services']}")

    full_scan_output["network_devices"] = network_devices
    save_results_to_file(full_scan_output, scan_type="network")
