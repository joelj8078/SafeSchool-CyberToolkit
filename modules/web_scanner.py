import requests
from bs4 import BeautifulSoup
import ssl
import socket
import json
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

def scan_website(url):
    parsed = urlparse(url)
    domain = parsed.netloc or parsed.path
    if not domain:
        return {"error": "Invalid URL"}

    try:
        response = requests.get(url, timeout=10)
        headers = dict(response.headers)
        soup = BeautifulSoup(response.text, "html.parser")

        # Naive tech fingerprinting
        tech_stack = []
        if soup.find('script', src=True): tech_stack.append("JavaScript")
        if soup.find('meta', attrs={"name": "generator"}):
            tech_stack.append(soup.find('meta', attrs={"name": "generator"})["content"])

        if "wp-content" in response.text:
            tech_stack.append("WordPress")

        ssl_info = get_ssl_info(domain) if url.startswith("https") else {}

        result = {
            "url": url,
            "headers": headers,
            "technologies": tech_stack,
            "ssl_info": ssl_info,
        }

        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/webscan_{timestamp}.json"
        with open(filename, "w") as f:
            json.dump(result, f, indent=4)

        print(f"[✔] Web scan saved to {filename}")
        return result

    except Exception as e:
        print(f"[!] Failed to scan: {e}")
        return {"error": str(e)}

# Run test
if __name__ == "__main__":
    test_url = input("Enter a website URL to scan (e.g., https://example.com): ")
    scan_website(test_url)
