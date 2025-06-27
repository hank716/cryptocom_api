import os

REPORTS_DIR = "docs"
index_file_path = os.path.join(REPORTS_DIR, "index.html")

entries = [
    d for d in os.listdir(REPORTS_DIR)
    if os.path.isdir(os.path.join(REPORTS_DIR, d)) and d.startswith("202")
]
entries.sort(reverse=True)  # 最新的放最上面

html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Test Report Index</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container mt-5">
        <h1 class="mb-4">📊 Available Test Reports</h1>
        <ul class="list-group">
"""

for i, entry in enumerate(entries):
    badge = ' <span class="badge bg-success">Latest</span>' if i == 0 else ""
    html += f'  <li class="list-group-item d-flex justify-content-between align-items-center">\n'
    html += f'    <a href="{entry}/index.html">{entry}</a>{badge}\n'
    html += f'  </li>\n'

html += """        </ul>
    </div>
</body>
</html>
"""

with open(index_file_path, "w") as f:
    f.write(html)

print(f"[✓] Pretty index.html generated at {index_file_path}")
