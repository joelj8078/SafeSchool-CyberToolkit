from flask import Blueprint, render_template, request
import json
import os
from datetime import datetime
from modules.web_scanner import scan_website  # ← import scanner

main = Blueprint('main', __name__)

@main.route('/', methods=["GET", "POST"])
def index():
    scan_result = None

    if request.method == "POST":
        url = request.form.get("url")
        if url:
            scan_result = scan_website(url)

            # Save to JSON
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join("data", f"web_scan_{timestamp}.json")
            with open(save_path, "w") as f:
                json.dump(scan_result, f, indent=4)

    return render_template("index.html", scan_result=scan_result)
