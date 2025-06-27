import os

REPORTS_DIR = "docs"
index_file_path = os.path.join(REPORTS_DIR, "index.html")

entries = [
    d for d in os.listdir(REPORTS_DIR)
    if os.path.isdir(os.path.join(REPORTS_DIR, d)) and d.startswith("202")
]
entries.sort(reverse=True)  # 最新的放上面

html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Test Report Index</title>
</head>
<body>
    <h1>Available Test Reports</h1>
    <ul>
"""

for entry in entries:
    html += f'        <li><a href="{entry}/index.html">{entry}</a></li>\n'

html += """    </ul>
</body>
</html>
"""

with open(index_file_path, "w") as f:
    f.write(html)

print(f"[✓] index.html generated at {index_file_path}")
