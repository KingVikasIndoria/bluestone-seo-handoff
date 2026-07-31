#!/usr/bin/env bash
#
# Bluestone SEO Dashboard Instant Updater
# =======================================
# Run this script anytime in terminal: ./update.sh

set -e

PROJECT_DIR="/Users/vikasindoria/Documents/Geo and Seo/article generation seo codex"
cd "$PROJECT_DIR"

echo "============================================================"
echo "📊 Fetching fresh WordPress posts & GSC Search Analytics..."
echo "============================================================"
python3 scripts/generate_dashboard_dataset.py

echo "🔄 Syncing dashboard data..."
cp dashboard/dashboard_data.json ./dashboard_data.json

echo "📦 Pushing live updates to GitHub Pages..."
git add .
if git diff-index --quiet HEAD --; then
    echo "✅ Dashboard is already up-to-date. No new changes to push."
else
    git commit -m "update: live SEO dashboard dataset sync [$(date +'%b %d, %Y %I:%M %p')]"
    git push origin main
    echo ""
    echo "============================================================"
    echo "🎉 SUCCESS! Dashboard updated and pushed to live site!"
    echo "🌐 View live: https://kingvikasindoria.github.io/bluestone-seo-handoff/"
    echo "============================================================"
fi
