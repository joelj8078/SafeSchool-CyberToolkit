import requests
from bs4 import BeautifulSoup
import ssl
import socket
import json
import os
from urllib.parse import urlparse
from datetime import datetime

def get_ssl_info(domain):
    context = ssl.create_default_context()
    try:
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                return {
                    "issuer": cert.get("issuer"),
                    "subject": cert.get("subject"),
                    "valid_from": cert.get("notBefore"),
                    "valid_until": cert.get("notAfter")
                }
    except Exception as e:
        return {"error": str(e)}

def detect_technologies(response_text, soup):
    tech_stack = []

    if soup.find('script', src=True):
        tech_stack.append("JavaScript")
    generator_meta = soup.find('meta', attrs={"name": "generator"})
    if generator_meta:
        tech_stack.append(generator_meta.get("content", "Unknown Generator"))
    if "wp-content" in response_text:
        tech_stack.append("WordPress")

    return tech_stack

def save_web_results_to_file(result):
    folder_path = os.path.join("data", "web")
    os.makedirs(folder_path, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"web_scan_{timestamp}.json"
    full_path = os.path.join(folder_path, filename)

    with open(full_path, "w") as f:
        json.dump(result, f, indent=4)

    print(f"[✔] Web scan saved to {full_path}")

def scan_website(url):
    parsed = urlparse(url)
    domain = parsed.netloc or parsed.path
    if not domain:
        print("[!] Invalid URL format.")
        return {"error": "Invalid URL format."}

    try:
        response = requests.get(url, timeout=10)
        headers = dict(response.headers)
        soup = BeautifulSoup(response.text, "html.parser")

        technologies = detect_technologies(response.text, soup)
        ssl_info = get_ssl_info(domain) if url.startswith("https") else {}

        result = {
            "url": url,
            "headers": headers,
            "technologies": technologies,
            "ssl_info": ssl_info
        }

        save_web_results_to_file(result)
        return result

    except Exception as e:
        print(f"[!] Failed to scan {url}: {e}")
        return {
            "url": url,
            "headers": {},
            "technologies": [],
            "ssl_info": {"error": str(e)},
            "error": str(e)
        }

# Optional CLI usage
if __name__ == "__main__":
    test_url = input("Enter a website URL to scan (e.g., https://example.com): ")
    results = scan_website(test_url)
    print(json.dumps(results, indent=2))
