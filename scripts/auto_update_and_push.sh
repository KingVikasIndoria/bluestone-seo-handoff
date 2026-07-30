#!/usr/bin/env bash
#
# Bluestone SEO Dashboard Auto-Update & Push Script
# ==================================================
# Runs locally or via cron to update dashboard dataset and push to GitHub.

set -e

PROJECT_DIR="/Users/vikasindoria/Documents/Geo and Seo/article generation seo codex"
cd "$PROJECT_DIR"

echo "🔄 Updating Bluestone SEO Dashboard dataset..."
python3 scripts/generate_dashboard_dataset.py

echo "📦 Committing updated dashboard dataset to Git..."
git add dashboard/

if git diff-index --quiet HEAD -- dashboard/; then
    echo "✅ No new data changes detected."
else
    git commit -m "auto: update SEO dashboard data [$(date +'%Y-%m-%d %H:%M')]"
    echo "🚀 Pushing update to GitHub..."
    git push origin main
    echo "🎉 Successfully pushed to GitHub!"
fi
