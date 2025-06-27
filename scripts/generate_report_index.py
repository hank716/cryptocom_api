# scripts/generate_report_index.py
import os
from datetime import datetime

REPORTS_DIR = "docs"
entries = []

# 掃描所有 timestamp 報告資料夾
for entry in sorted(os.listdir(REPORTS_DIR)):
    full_path = os.path.join(REPORTS_DIR, entry)
    if os.path.isdir(full_path) and entry != "assets":
        entries.append(f'<li><a href="{entry}/index.html">{entry}</a></li>')

# 產生 index.html
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Allure Report Index</title>
</head>
<body>
    <h1>📊 Allure Report Index</h1>
    <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <ul>
        {''.join(entries)}
    </ul>
</body>
</html>
"""

with open(os.path.join(REPORTS_DIR, "index.html"), "w") as f:
    f.write(html_content)

print("✅ Generated docs/index.html")
