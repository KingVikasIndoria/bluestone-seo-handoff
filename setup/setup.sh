#!/usr/bin/env bash
#
# Bluestone SEO Dashboard — One-Click Setup for New Machines
# ===========================================================
# Run this once on any new laptop to get everything working.
#
# Usage:
#   chmod +x setup/setup.sh
#   ./setup/setup.sh
#

set -e

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║   Bluestone SEO Dashboard — New Machine Setup               ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Resolve project root (parent of setup/ folder)
SETUP_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SETUP_DIR")"
cd "$PROJECT_DIR"
echo "📂 Project Directory: $PROJECT_DIR"

# ──────────────────────────────────────────────────────────────────
# Step 1: Check Python 3
# ──────────────────────────────────────────────────────────────────
echo ""
echo "1️⃣  Checking Python 3..."
if command -v python3 &>/dev/null; then
    PY_VERSION=$(python3 --version)
    echo "   ✅ $PY_VERSION"
else
    echo "   ❌ Python 3 not found! Install it from https://python.org/downloads/"
    exit 1
fi

# ──────────────────────────────────────────────────────────────────
# Step 2: Install Python Dependencies
# ──────────────────────────────────────────────────────────────────
echo ""
echo "2️⃣  Installing Python dependencies..."
pip3 install -r setup/requirements.txt
echo "   ✅ All Python packages installed"

# ──────────────────────────────────────────────────────────────────
# Step 3: Check Git
# ──────────────────────────────────────────────────────────────────
echo ""
echo "3️⃣  Checking Git..."
if command -v git &>/dev/null; then
    GIT_VERSION=$(git --version)
    echo "   ✅ $GIT_VERSION"
else
    echo "   ❌ Git not found! Install it from https://git-scm.com/downloads"
    exit 1
fi

# ──────────────────────────────────────────────────────────────────
# Step 4: Check Google API Credentials
# ──────────────────────────────────────────────────────────────────
echo ""
echo "4️⃣  Checking Google API credentials..."

if [ -f "scripts/client_secret.json" ]; then
    echo "   ✅ client_secret.json found"
else
    echo "   ❌ scripts/client_secret.json MISSING"
    echo "      → Download from Google Cloud Console → APIs & Credentials"
    echo "      → Place it at: scripts/client_secret.json"
fi

if [ -f "scripts/gsc_token.json" ]; then
    echo "   ✅ gsc_token.json found (GSC Search Analytics)"
else
    echo "   ⚠️  scripts/gsc_token.json not found"
    echo "      → Will be auto-generated on first run (browser OAuth login required)"
fi

if [ -f "scripts/indexing_token.json" ]; then
    echo "   ✅ indexing_token.json found (Indexing API)"
else
    echo "   ⚠️  scripts/indexing_token.json not found"
    echo "      → Will be auto-generated on first run (browser OAuth login required)"
fi

# ──────────────────────────────────────────────────────────────────
# Step 5: Check required directories
# ──────────────────────────────────────────────────────────────────
echo ""
echo "5️⃣  Ensuring required directories exist..."
mkdir -p dashboard
mkdir -p output
echo "   ✅ dashboard/ and output/ directories ready"

# ──────────────────────────────────────────────────────────────────
# Step 6: Make scripts executable
# ──────────────────────────────────────────────────────────────────
echo ""
echo "6️⃣  Making scripts executable..."
chmod +x update.sh
chmod +x setup/setup.sh
echo "   ✅ Scripts are executable"

# ──────────────────────────────────────────────────────────────────
# Step 7: Fix update.sh to use dynamic path
# ──────────────────────────────────────────────────────────────────
echo ""
echo "7️⃣  Updating update.sh with this machine's project path..."

# Create a portable update.sh if the current one has a hardcoded path
if grep -q "vikasindoria" update.sh 2>/dev/null; then
    cat > update.sh << 'UPDATEEOF'
#!/usr/bin/env bash
#
# Bluestone SEO Dashboard Instant Updater
# =======================================
# Run this script anytime in terminal: ./update.sh

set -e

# Auto-detect project directory (where this script lives)
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
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
UPDATEEOF
    chmod +x update.sh
    echo "   ✅ update.sh updated to use dynamic path (works on any machine)"
else
    echo "   ✅ update.sh already portable"
fi

# ──────────────────────────────────────────────────────────────────
# Step 8: Verify everything
# ──────────────────────────────────────────────────────────────────
echo ""
echo "8️⃣  Running verification test..."
python3 -c "
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import requests
import pandas as pd
print('   ✅ All Python imports successful')
"

# ──────────────────────────────────────────────────────────────────
# Done!
# ──────────────────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║   ✅ SETUP COMPLETE!                                        ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║                                                              ║"
echo "║   Available Commands:                                        ║"
echo "║                                                              ║"
echo "║   📊 Update Dashboard:                                       ║"
echo "║      ./update.sh                                             ║"
echo "║                                                              ║"
echo "║   🚀 Submit URLs for Indexing:                               ║"
echo "║      python3 scripts/submit_google_indexing_api.py           ║"
echo "║                                                              ║"
echo "║   📈 Pull GSC Blog Data:                                     ║"
echo "║      python3 scripts/gsc_blog_data.py                       ║"
echo "║                                                              ║"
echo "║   📋 Batch Blog Queue:                                       ║"
echo "║      python3 scripts/batch_blog_queue.py status              ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
