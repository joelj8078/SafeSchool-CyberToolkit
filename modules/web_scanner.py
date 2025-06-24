import requests
from bs4 import BeautifulSoup
import ssl
import socket
import json
import os
import time
from urllib.parse import urlparse, urljoin, urlencode
from datetime import datetime
import whois
from modules.utils import generate_radar_chart

# === Constants ===
COMMON_PATHS = [
    "/admin", "/login", "/robots.txt", "/.env", "/config",
    "/phpinfo.php", "/sitemap.xml", "/backup.zip", "/.git"
]

SECURITY_HEADERS = [
    "Content-Security-Policy", "Strict-Transport-Security", "X-Frame-Options",
    "X-Content-Type-Options", "Referrer-Policy", "Permissions-Policy"
]

# === SSL Certificate Info ===
def get_ssl_info(domain):
    context = ssl.create_default_context()
    try:
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                expires_on = datetime.strptime(cert.get('notAfter'), "%b %d %H:%M:%S %Y %Z")
                days_left = (expires_on - datetime.utcnow()).days
                return {
                    "issuer": dict(x[0] for x in cert.get("issuer")),
                    "subject": dict(x[0] for x in cert.get("subject")),
                    "valid_from": cert.get("notBefore"),
                    "valid_until": cert.get("notAfter"),
                    "expires_in_days": days_left
                }
    except Exception as e:
        return {"error": str(e)}

# === Technology Detection ===
def detect_technologies(response_text, soup):
    tech_stack = []

    if soup.find('script', src=True): tech_stack.append("JavaScript")
    if soup.find('link', href=True): tech_stack.append("CSS Frameworks")
    if "wp-content" in response_text: tech_stack.append("WordPress")
    if "Drupal" in response_text: tech_stack.append("Drupal")
    if "react" in response_text.lower(): tech_stack.append("React")
    if "vue" in response_text.lower(): tech_stack.append("Vue.js")

    generator = soup.find('meta', attrs={"name": "generator"})
    if generator:
        tech_stack.append(generator.get("content", "Unknown Generator"))

    return list(set(tech_stack))

# === Security Headers Check ===
def check_security_headers(headers):
    present, missing = [], []
    for header in SECURITY_HEADERS:
        if header in headers:
            present.append(header)
        else:
            missing.append(header)
    return {"present": present, "missing": missing}

# === Common Sensitive Paths Check ===
def check_common_paths(base_url):
    discovered = []
    for path in COMMON_PATHS:
        full_url = urljoin(base_url, path)
        try:
            res = requests.get(full_url, timeout=5)
            if res.status_code in [200, 301, 302]:
                discovered.append(path)
        except:
            continue
    return discovered

# === Open Redirect Check ===
def check_open_redirect(base_url):
    try:
        test_paths = ["/redirect-test", "/login", "/auth"]
        for path in test_paths:
            test_url = urljoin(base_url, path)
            for param in ["next", "url", "redirect"]:
                payload = {param: "https://evil.com"}
                redirect_url = f"{test_url}?{urlencode(payload)}"
                res = requests.get(redirect_url, allow_redirects=False, timeout=5)
                if res.status_code in [301, 302] and "evil.com" in res.headers.get("Location", ""):
                    return {"vulnerable": True, "location": res.headers.get("Location")}
    except Exception as e:
        return {"error": str(e)}
    return {"vulnerable": False}

# === WHOIS Lookup ===
def get_domain_whois(domain):
    try:
        w = whois.whois(domain)
        return {
            "domain_name": str(w.domain_name),
            "registrar": w.registrar,
            "creation_date": str(w.creation_date),
            "expiration_date": str(w.expiration_date)
        }
    except Exception as e:
        return {"error": str(e)}

# === Security Score Calculation ===
def calculate_security_score(security_headers, ssl_info, sensitive_paths):
    score = 10
    score -= len(security_headers["missing"])
    if ssl_info.get("expires_in_days", 365) < 30:
        score -= 1
    score -= min(len(sensitive_paths), 3)  # Cap penalty for sensitive paths
    return max(score, 0)

# === Save to JSON ===
def save_web_results_to_file(result):
    folder_path = os.path.join("data", "web")
    os.makedirs(folder_path, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"web_scan_{timestamp}.json"
    full_path = os.path.join(folder_path, filename)
    with open(full_path, "w") as f:
        json.dump(result, f, indent=4)
    print(f"[✔] Web scan saved to {full_path}")

# === Web Scanner Orchestrator ===
def scan_website(url):
    parsed = urlparse(url)
    domain = parsed.netloc or parsed.path
    if not domain:
        return {"error": "Invalid URL format."}

    try:
        start_time = time.time()
        response = requests.get(url, timeout=10)
        elapsed = round((time.time() - start_time) * 1000, 2)  # ms

        headers = dict(response.headers)
        soup = BeautifulSoup(response.text, "html.parser")

        result = {
            "url": url,
            "status_code": response.status_code,
            "headers": headers,
            "technologies": detect_technologies(response.text, soup),
            "ssl_info": get_ssl_info(domain) if url.startswith("https") else {},
            "security_headers": check_security_headers(headers),
            "sensitive_paths_found": check_common_paths(url),
            "open_redirect_test": check_open_redirect(url),
            "whois_info": get_domain_whois(domain),
            "performance": {
                "response_time_ms": elapsed,
                "content_length_kb": round(len(response.content) / 1024, 2)
            }
        }

        result["security_score"] = calculate_security_score(
            result["security_headers"],
            result["ssl_info"],
            result["sensitive_paths_found"]
        )

        save_web_results_to_file(result)
        chart_filename = generate_radar_chart(result)
        result["radar_chart"] = chart_filename
        return result

    except Exception as e:
        return {
            "url": url,
            "error": str(e),
            "status_code": None,
            "headers": {},
            "technologies": [],
            "ssl_info": {"error": str(e)},
            "security_headers": {"present": [], "missing": SECURITY_HEADERS},
            "sensitive_paths_found": [],
            "open_redirect_test": {"error": str(e)},
            "whois_info": {"error": str(e)},
            "performance": {},
            "security_score": 0
        }

# === CLI Entrypoint ===
if __name__ == "__main__":
    test_url = input("Enter a website URL to scan (e.g., https://example.com): ")
    result = scan_website(test_url)
    print(json.dumps(result, indent=2))
