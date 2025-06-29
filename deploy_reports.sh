#!/bin/bash

set -e
timestamp=$(date +%Y%m%d_%H%M%S)

# Run the local report generation script first
bash generate_allure_and_index.sh

# Switch to the gh-pages branch
echo "🚚 Deploying to gh-pages..."
git checkout gh-pages

# Retrieve the latest docs/ report from the main branch
git checkout main -- docs/

# Add and push the updated report
git add docs/
git commit -m "📊 Update test reports at $timestamp"
git push origin gh-pages

# Switch back to main
git checkout main
