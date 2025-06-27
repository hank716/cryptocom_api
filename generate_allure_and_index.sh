#!/bin/bash
set -e

timestamp=$(date +%Y%m%d_%H%M%S)
output_dir="reports/allure-results"
report_dir="docs/$timestamp"

# 1. Run behave and generate raw results
echo "🎯 Running behave..."
behave -f allure_behave.formatter:AllureFormatter -o "$output_dir"

# 2. Generate HTML report
echo "📊 Generating Allure HTML to $report_dir..."
allure generate "$output_dir" -o "$report_dir" --clean

# 3. Run Python to update docs/index.html
echo "📄 Updating index.html..."
python3 scripts/generate_report_index.py

echo "✅ Done! View: $report_dir/index.html"
