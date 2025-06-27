#!/bin/bash

set -e
timestamp=$(date +%Y%m%d_%H%M%S)

# 先執行本地報告產生腳本
bash generate_allure_and_index.sh

# 切換到 gh-pages 分支
echo "🚚 Deploying to gh-pages..."
git checkout gh-pages

# 從 main 取出 docs/ 最新報告
git checkout main -- docs/

# 加入並推送報告
git add docs/
git commit -m "📊 Update test reports at $timestamp"
git push origin gh-pages

# 切回 main
git checkout main
