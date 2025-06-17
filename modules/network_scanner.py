import nmap
import json
import os
from datetime import datetime
import platform
import re
import socket
import psutil


def get_default_gateway():
    system = platform.system()
    print(f"[DEBUG] Detected platform: {system}")
    try:
        if system == "Windows":
            output = os.popen("ipconfig").read()
            print("[DEBUG] ipconfig output:\n", output)
            matches = re.findall(r"Default Gateway[ .:]*([\d\.]+)", output)
            print(f"[DEBUG] Matches found: {matches}")
            for ip in matches:
                if ip and ip != "0.0.0.0":
                    print(f"[DEBUG] Selected Gateway IP: {ip}")
                    return ip
        elif system in ["Linux", "Darwin"]:
            output = os.popen("ip route | grep default").read()
            print("[DEBUG] ip route output:\n", output)
            gateway = output.split()[2] if output else None
            print(f"[DEBUG] Linux Gateway IP: {gateway}")
            return gateway
    except Exception as e:
        print(f"[ERROR] Failed to get gateway: {e}")
        return None
    return None

def check_router_security(gateway_ip):
    print(f"[INFO] Scanning router at {gateway_ip} ...")
    nm = nmap.PortScanner()
    try:
        nm.scan(hosts=gateway_ip, arguments='-p 21-1024')  # Wider range for router ports
    except Exception as e:
        print("[ERROR] Nmap failed to scan router:", e)
        return {
            "ip": gateway_ip,
            "open_ports": [],
            "weak_services": [],
            "error": str(e)
        }

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
    else:
        print("[WARN] No open ports found or router not responding to scan.")

    return router_result


def scan_network(subnet='192.168.1.0/24'):
    print(f"[INFO] Scanning local network: {subnet}")
    nm = nmap.PortScanner()
    try:
        nm.scan(hosts=subnet, arguments='-sS -T4')
    except Exception as e:
        print("[ERROR] Network scan failed:", e)
        return []

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


def get_local_system_info():
    info = {}

    hostname = socket.gethostname()
    try:
        ip_address = socket.gethostbyname(hostname)
    except socket.gaierror:
        ip_address = "Unavailable"

    info["hostname"] = hostname
    info["ip_address"] = ip_address
    info["os"] = platform.system()
    info["os_version"] = platform.version()
    info["architecture"] = platform.machine()

    # CPU
    info["cpu_cores"] = psutil.cpu_count(logical=False)
    info["cpu_threads"] = psutil.cpu_count(logical=True)
    info["cpu_usage_percent"] = psutil.cpu_percent(interval=1)

    # RAM
    mem = psutil.virtual_memory()
    info["memory_total_gb"] = round(mem.total / (1024 ** 3), 2)
    info["memory_used_gb"] = round(mem.used / (1024 ** 3), 2)
    info["memory_usage_percent"] = mem.percent

    # Disk
    disks = []
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            disks.append({
                "device": part.device,
                "mountpoint": part.mountpoint,
                "fstype": part.fstype,
                "total_gb": round(usage.total / (1024 ** 3), 2),
                "used_gb": round(usage.used / (1024 ** 3), 2),
                "free_gb": round(usage.free / (1024 ** 3), 2),
                "usage_percent": usage.percent
            })
        except PermissionError:
            continue
    info["disks"] = disks

    # Network interfaces
    interfaces = []
    net_if_addrs = psutil.net_if_addrs()
    net_if_stats = psutil.net_if_stats()

    for iface, addrs in net_if_addrs.items():
        iface_data = {
            "interface": iface,
            "is_up": net_if_stats[iface].isup if iface in net_if_stats else False,
            "speed_mbps": net_if_stats[iface].speed if iface in net_if_stats else None,
            "addresses": []
        }
        for addr in addrs:
            iface_data["addresses"].append({
                "family": str(addr.family),
                "address": addr.address,
                "netmask": addr.netmask,
                "broadcast": addr.broadcast
            })
        interfaces.append(iface_data)

    info["network_interfaces"] = interfaces

    return info


def save_results_to_file(data, scan_type="network"):
    save_dir = os.path.join("data", scan_type)
    os.makedirs(save_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{scan_type}_scan_{timestamp}.json"
    full_path = os.path.join(save_dir, filename)

    with open(full_path, "w") as f:
        json.dump(data, f, indent=4)

    print(f"[✔] Scan results saved to {full_path}")
    return full_path


def run_network_scan():
    output = {
        "system_info": get_local_system_info(),
        "router_scan": {},
        "network_devices": []
    }

    gateway_ip = get_default_gateway()
    print(f"[DEBUG] Detected Default Gateway: {gateway_ip}")  # ← Add this line

    if gateway_ip:
        output["router_scan"] = check_router_security(gateway_ip)

    output["network_devices"] = scan_network()
    save_results_to_file(output, scan_type="network")

    return output


if __name__ == '__main__':
    results = run_network_scan()
    print(json.dumps(results, indent=4))
