import matplotlib
matplotlib.use('Agg')  # Non-GUI backend suitable for server-side rendering

import matplotlib.pyplot as plt
import numpy as np
import os
import glob

def generate_radar_chart(result):
    # Labels for each metric
    labels = ['SSL', 'Security Headers', 'Sensitive Paths', 'Open Redirect']
    scores = []

    # Compute individual metric scores
    ssl_score = 1 if result['ssl_info'].get('expires_in_days', 0) > 30 else 0
    scores.append(ssl_score)

    total_headers = len(result['security_headers']['present']) + len(result['security_headers']['missing'])
    header_score = len(result['security_headers']['present']) / total_headers if total_headers else 0
    scores.append(round(header_score, 2))

    sensitive_score = max(0, 1 - (len(result['sensitive_paths_found']) / 10))
    scores.append(round(min(sensitive_score, 1), 2))

    redirect_score = 0 if result['open_redirect_test'].get('vulnerable') else 1
    scores.append(redirect_score)

    # Loop back to the first point for a closed radar shape
    scores += scores[:1]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    # Determine color based on average score
    avg_score = sum(scores[:-1]) / 4
    if avg_score >= 0.75:
        chart_color = 'green'
    elif avg_score >= 0.4:
        chart_color = 'orange'
    else:
        chart_color = 'red'

    # Create radar chart
    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
    ax.plot(angles, scores, color=chart_color, linewidth=2)
    ax.fill(angles, scores, color=chart_color, alpha=0.25)

    # Format radar chart
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_title("Web Security Radar", size=14, color=chart_color, pad=20)

    # Save chart to static path
    output_dir = os.path.join("static", "images")
    os.makedirs(output_dir, exist_ok=True)

    # Delete previous radar charts
    for old in glob.glob(os.path.join(output_dir, "web_radar*.png")):
        os.remove(old)

    chart_path = os.path.join(output_dir, "web_radar.png")
    plt.savefig(chart_path, bbox_inches='tight')
    plt.close()
