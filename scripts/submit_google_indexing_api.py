#!/usr/bin/env python3
"""
Google Indexing API Batch URL Submitter
========================================
Submits unindexed URLs to Google Indexing API (`indexing.googleapis.com`)
Rate limit: 200 URLs / day

Prerequisite:
  1. Enable "Indexing API" in Google Cloud Console
     → https://console.cloud.google.com/apis/library/indexing.googleapis.com
  2. Scope: https://www.googleapis.com/auth/indexing
"""

import os
import sys
import json
import time
from pathlib import Path
import csv

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
except ImportError:
    print("❌ Missing google libraries. Run: pip install google-api-python-client google-auth-oauthlib")
    sys.exit(1)

SCOPES = ["https://www.googleapis.com/auth/indexing"]
SCRIPT_DIR = Path(__file__).parent
CLIENT_SECRET_FILE = SCRIPT_DIR / "client_secret.json"
INDEXING_TOKEN_FILE = SCRIPT_DIR / "indexing_token.json"
CSV_PATH = SCRIPT_DIR.parent / "output" / "unindexed_post_july16_blogs.csv"

def authenticate_indexing():
    creds = None
    if INDEXING_TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(INDEXING_TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CLIENT_SECRET_FILE.exists():
                print(f"❌ Missing {CLIENT_SECRET_FILE.name}")
                sys.exit(1)

            print("🔐 Opening browser for Google Indexing API authorization...")
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CLIENT_SECRET_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(INDEXING_TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
        print("✅ Indexing token saved.")

    return creds

def submit_url(service, url):
    body = {
        "url": url,
        "type": "URL_UPDATED"
    }
    try:
        res = service.urlNotifications().publish(body=body).execute()
        time_notified = res.get("urlNotificationMetadata", {}).get("latestUpdate", {}).get("notifyTime", "Done")
        print(f"  ✅ Submitted: {url[:55]:<57} | Time: {time_notified}")
        return True
    except Exception as e:
        print(f"  ❌ Failed: {url[:55]:<57} | Error: {e}")
        return False

def main():
    if not CSV_PATH.exists():
        print(f"❌ Missing CSV file: {CSV_PATH}")
        sys.exit(1)

    urls_to_submit = []
    with open(CSV_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("link"):
                urls_to_submit.append(row["link"].strip())

    print(f"🚀 Found {len(urls_to_submit)} unindexed URLs to submit to Google Indexing API.")
    
    # Cap at 200 per day limit
    batch = urls_to_submit[:200]
    print(f"📦 Submitting batch of {len(batch)} URLs (Daily quota limit is 200 URLs)...")

    creds = authenticate_indexing()
    service = build("indexing", "v3", credentials=creds)

    success_count = 0
    for idx, url in enumerate(batch, 1):
        print(f"[{idx}/{len(batch)}]", end=" ")
        if submit_url(service, url):
            success_count += 1
        time.sleep(0.2)  # rate limit pause

    print("\n" + "=" * 60)
    print(f"🎉 Submitted {success_count} / {len(batch)} URLs to Google Indexing API!")
    print("   Googlebot will crawl these URLs within minutes to hours.")
    print("=" * 60)

if __name__ == "__main__":
    main()
