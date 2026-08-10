# Bluestone SEO Dashboard — Setup Guide

## Quick Start (New Machine)

```bash
# 1. Clone the repo
git clone https://github.com/KingVikasIndoria/bluestone-seo-handoff.git
cd bluestone-seo-handoff

# 2. Run the one-click setup
chmod +x setup/setup.sh
./setup/setup.sh

# 3. Update the dashboard
./update.sh
```

---

## What the Setup Does

| Step | Action |
|------|--------|
| 1 | Checks Python 3 is installed |
| 2 | Installs all Python dependencies from `requirements.txt` |
| 3 | Checks Git is available |
| 4 | Verifies Google API credential files exist |
| 5 | Creates required directories (`dashboard/`, `output/`) |
| 6 | Makes shell scripts executable |
| 7 | Fixes `update.sh` to use dynamic paths (no hardcoded machine paths) |
| 8 | Runs an import verification test |

---

## Credential Files Required

These files contain Google OAuth tokens and **must be copied manually** from the current machine (they are in `.gitignore` for security):

| File | Purpose | Location |
|------|---------|----------|
| `client_secret.json` | Google Cloud OAuth 2.0 client ID | `scripts/client_secret.json` |
| `gsc_token.json` | Google Search Console API token | `scripts/gsc_token.json` |
| `indexing_token.json` | Google Indexing API token | `scripts/indexing_token.json` |

### How to Transfer Credentials

**Option A — Copy from current machine:**
```bash
# On the current machine, copy these 3 files:
scripts/client_secret.json
scripts/gsc_token.json
scripts/indexing_token.json
```

**Option B — Re-authenticate on the new machine:**
1. Copy only `scripts/client_secret.json` (download from [Google Cloud Console](https://console.cloud.google.com/apis/credentials))
2. The token files will be auto-generated on first run — a browser window will open for Google OAuth login

---

## Available Scripts

### 📊 Dashboard Update
```bash
./update.sh
```
Fetches fresh WordPress posts + Google Search Console data, rebuilds `dashboard_data.json`, and pushes to GitHub Pages.

### 🚀 Google Indexing API
```bash
python3 scripts/submit_google_indexing_api.py
```
Submits unindexed blog URLs to Google's Indexing API (200 URLs/day limit).

### 📈 GSC Blog Data Export
```bash
python3 scripts/gsc_blog_data.py
```
Pulls search analytics data from Google Search Console and exports to CSV.

### 📋 Batch Blog Queue
```bash
python3 scripts/batch_blog_queue.py status    # Check queue status
python3 scripts/batch_blog_queue.py init --start 25 --count 10  # Initialize queue
python3 scripts/batch_blog_queue.py watch     # Watch live progress
```
Manages the blog publishing queue from the SEO Strategy spreadsheet.

### 📊 Dashboard Data Generator
```bash
python3 scripts/generate_dashboard_dataset.py
```
Core script that fetches all data and generates `dashboard/dashboard_data.json`.

---

## WordPress Credentials

The WordPress API credentials are stored inside `scripts/generate_dashboard_dataset.py`:
```
URL:  https://blog.bluestone.com/wp-json/wp/v2/posts
Auth: (username, application_password)
```

If these change, update them in the script directly.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError` | Run `pip3 install -r setup/requirements.txt` |
| GSC token expired | Delete `scripts/gsc_token.json` and re-run — browser OAuth will re-authenticate |
| Indexing token expired | Delete `scripts/indexing_token.json` and re-run |
| `update.sh: Permission denied` | Run `chmod +x update.sh` |
| Git push fails | Ensure SSH keys or GitHub token are configured on the new machine |
