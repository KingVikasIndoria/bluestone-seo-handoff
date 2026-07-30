#!/usr/bin/env python3
"""
Sitemap Submission & Unindexed URLs Exporter
=============================================
1. Submits post-sitemap.xml to Google Search Console API
2. Exports all 172 unindexed Post-July 16 URLs to CSV for indexing submission
"""

import json
import csv
from datetime import datetime
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/webmasters"]
SITE_URL = "sc-domain:bluestone.com"
SITEMAP_URL = "https://blog.bluestone.com/post-sitemap.xml"

SCRIPT_DIR = Path(__file__).parent
TOKEN_FILE = SCRIPT_DIR / "gsc_token.json"
OUTPUT_DIR = SCRIPT_DIR.parent / "output"
CSV_PATH = OUTPUT_DIR / "unindexed_post_july16_blogs.csv"

def main():
    if not TOKEN_FILE.exists():
        print(f"❌ Token missing: {TOKEN_FILE}")
        return

    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    service = build("searchconsole", "v1", credentials=creds)

    # 1. Submit sitemap
    print(f"📡 Submitting sitemap to Google Search Console: {SITEMAP_URL}...")
    try:
        service.sitemaps().submit(siteUrl=SITE_URL, feedpath=SITEMAP_URL).execute()
        print("✅ Sitemap submitted successfully to Google!")
    except Exception as e:
        print(f"⚠️ Sitemap submission result: {e}")

    # 2. Load unindexed URLs
    json_path = SCRIPT_DIR.parent / "dashboard" / "dashboard_data.json"
    with open(json_path) as f:
        data = json.load(f)

    unindexed_blogs = [b for b in data.get("post_july16_blogs", []) if b.get("impressions", 0) == 0]
    
    print(f"\n📋 Found {len(unindexed_blogs)} unindexed Post-July 16 blog URLs.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["title", "link", "published_date", "slug"])
        for b in unindexed_blogs:
            writer.writerow([b["title"], b["link"], b["published_date"], b["slug"]])

    print(f"💾 Exported unindexed URLs to: {CSV_PATH}")

if __name__ == "__main__":
    main()
