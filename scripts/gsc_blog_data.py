#!/usr/bin/env python3
"""
Google Search Console – Blog Performance Data Extractor
========================================================
Pulls search-analytics data for blog.bluestone.com from the last 30 days.

Prerequisites:
  1. Enable "Google Search Console API" in Google Cloud Console.
  2. Create OAuth 2.0 credentials (Desktop app) and download as `client_secret.json`.
  3. Place `client_secret.json` in the same directory as this script.
  4. pip install google-api-python-client google-auth-oauthlib pandas

First run will open a browser for Google OAuth login.
Subsequent runs reuse the saved token.
"""

import os
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    import pandas as pd
except ImportError:
    print("❌ Missing dependencies. Install them with:")
    print("   pip install google-api-python-client google-auth-oauthlib pandas")
    sys.exit(1)

# ── Configuration ────────────────────────────────────────────────────────────
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

# Your Search Console property (domain property)
SITE_URL = "sc-domain:bluestone.com"

# Filter to only blog pages
BLOG_URL_PREFIX = "https://blog.bluestone.com/"

# Date range: last 30 days (GSC data has a ~3-day lag)
END_DATE = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
START_DATE = (datetime.now() - timedelta(days=33)).strftime("%Y-%m-%d")

# Paths
SCRIPT_DIR = Path(__file__).parent
CLIENT_SECRET_FILE = SCRIPT_DIR / "client_secret.json"
TOKEN_FILE = SCRIPT_DIR / "gsc_token.json"
OUTPUT_DIR = SCRIPT_DIR.parent / "output"

# ── Authentication ───────────────────────────────────────────────────────────
def authenticate():
    """Authenticate with Google OAuth2 and return credentials."""
    creds = None

    # Load existing token
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    # If no valid creds, do the OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired token...")
            creds.refresh(Request())
        else:
            if not CLIENT_SECRET_FILE.exists():
                print(f"❌ Missing '{CLIENT_SECRET_FILE.name}'!")
                print()
                print("To get this file:")
                print("  1. Go to https://console.cloud.google.com/")
                print("  2. Create a project (or select existing)")
                print("  3. Enable 'Google Search Console API'")
                print("     → APIs & Services → Library → search 'Search Console API'")
                print("  4. Create OAuth 2.0 credentials:")
                print("     → APIs & Services → Credentials → Create Credentials")
                print("     → OAuth client ID → Application type: 'Desktop app'")
                print("  5. Download the JSON and save as 'client_secret.json'")
                print(f"     in: {SCRIPT_DIR}")
                sys.exit(1)

            print("🔐 Opening browser for Google OAuth login...")
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CLIENT_SECRET_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save token for next run
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
        print("✅ Token saved for future use.")

    return creds


# ── Data Fetching ────────────────────────────────────────────────────────────
def fetch_blog_data(service, dimensions, row_limit=5000):
    """
    Query Search Console for blog.bluestone.com pages.

    Args:
        service: Google API service object
        dimensions: list of dimensions e.g. ['page', 'query', 'date']
        row_limit: max rows to return (default 5000)

    Returns:
        list of dicts with the data
    """
    request_body = {
        "startDate": START_DATE,
        "endDate": END_DATE,
        "dimensions": dimensions,
        "dimensionFilterGroups": [
            {
                "filters": [
                    {
                        "dimension": "page",
                        "operator": "includingRegex",
                        "expression": r"^https://blog\.bluestone\.com/",
                    }
                ]
            }
        ],
        "rowLimit": row_limit,
        "dataState": "final",
    }

    print(f"📊 Fetching data for dimensions: {dimensions}")
    print(f"   Date range: {START_DATE} → {END_DATE}")

    response = (
        service.searchanalytics()
        .query(siteUrl=SITE_URL, body=request_body)
        .execute()
    )

    rows = response.get("rows", [])
    print(f"   Found {len(rows)} rows")

    results = []
    for row in rows:
        record = {}
        for i, dim in enumerate(dimensions):
            record[dim] = row["keys"][i]
        record["clicks"] = row.get("clicks", 0)
        record["impressions"] = row.get("impressions", 0)
        record["ctr"] = round(row.get("ctr", 0) * 100, 2)  # Convert to %
        record["position"] = round(row.get("position", 0), 1)
        results.append(record)

    return results


# ── Reports ──────────────────────────────────────────────────────────────────
def generate_reports(service):
    """Generate multiple reports and save as CSV."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # ── Report 1: Page-level performance ─────────────────────────────────
    print("\n" + "=" * 60)
    print("📄 REPORT 1: Page-Level Performance")
    print("=" * 60)

    page_data = fetch_blog_data(service, ["page"])
    if page_data:
        df_pages = pd.DataFrame(page_data)
        df_pages = df_pages.sort_values("clicks", ascending=False)

        # Save CSV
        csv_path = OUTPUT_DIR / f"gsc_blog_pages_{timestamp}.csv"
        df_pages.to_csv(csv_path, index=False)
        print(f"\n   💾 Saved to: {csv_path}")

        # Print summary
        print(f"\n   📊 Summary:")
        print(f"   Total blog pages with data: {len(df_pages)}")
        print(f"   Total clicks:      {df_pages['clicks'].sum():,.0f}")
        print(f"   Total impressions:  {df_pages['impressions'].sum():,.0f}")
        print(f"   Avg CTR:            {df_pages['ctr'].mean():.2f}%")
        print(f"   Avg Position:       {df_pages['position'].mean():.1f}")

        print(f"\n   🏆 Top 15 Pages by Clicks:")
        print("   " + "-" * 80)
        for _, row in df_pages.head(15).iterrows():
            url_short = row["page"].replace("https://blog.bluestone.com/", "/")
            print(
                f"   {url_short[:50]:<52} "
                f"Clicks: {row['clicks']:>5.0f}  "
                f"Impr: {row['impressions']:>7.0f}  "
                f"CTR: {row['ctr']:>5.1f}%  "
                f"Pos: {row['position']:>4.1f}"
            )

    # ── Report 2: Query-level performance (what people searched) ─────────
    print("\n" + "=" * 60)
    print("🔍 REPORT 2: Top Search Queries for Blog Pages")
    print("=" * 60)

    query_data = fetch_blog_data(service, ["query"])
    if query_data:
        df_queries = pd.DataFrame(query_data)
        df_queries = df_queries.sort_values("clicks", ascending=False)

        csv_path = OUTPUT_DIR / f"gsc_blog_queries_{timestamp}.csv"
        df_queries.to_csv(csv_path, index=False)
        print(f"\n   💾 Saved to: {csv_path}")

        print(f"\n   🏆 Top 20 Queries by Clicks:")
        print("   " + "-" * 80)
        for _, row in df_queries.head(20).iterrows():
            print(
                f"   {row['query'][:50]:<52} "
                f"Clicks: {row['clicks']:>5.0f}  "
                f"Impr: {row['impressions']:>7.0f}  "
                f"CTR: {row['ctr']:>5.1f}%  "
                f"Pos: {row['position']:>4.1f}"
            )

    # ── Report 3: Page + Query combined ──────────────────────────────────
    print("\n" + "=" * 60)
    print("📄🔍 REPORT 3: Page + Query Combined (Top Queries per Page)")
    print("=" * 60)

    page_query_data = fetch_blog_data(service, ["page", "query"])
    if page_query_data:
        df_pq = pd.DataFrame(page_query_data)
        df_pq = df_pq.sort_values(["page", "clicks"], ascending=[True, False])

        csv_path = OUTPUT_DIR / f"gsc_blog_page_queries_{timestamp}.csv"
        df_pq.to_csv(csv_path, index=False)
        print(f"\n   💾 Saved to: {csv_path}")
        print(f"   Total page+query combinations: {len(df_pq)}")

    # ── Report 4: Daily trend ────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("📈 REPORT 4: Daily Performance Trend")
    print("=" * 60)

    date_data = fetch_blog_data(service, ["date"])
    if date_data:
        df_dates = pd.DataFrame(date_data)
        df_dates = df_dates.sort_values("date")

        csv_path = OUTPUT_DIR / f"gsc_blog_daily_trend_{timestamp}.csv"
        df_dates.to_csv(csv_path, index=False)
        print(f"\n   💾 Saved to: {csv_path}")

        print(f"\n   📅 Daily Breakdown:")
        print("   " + "-" * 60)
        for _, row in df_dates.iterrows():
            bar = "█" * int(row["clicks"] / max(df_dates["clicks"].max() / 30, 1))
            print(
                f"   {row['date']}  "
                f"Clicks: {row['clicks']:>5.0f}  "
                f"Impr: {row['impressions']:>7.0f}  "
                f"{bar}"
            )

    # ── Report 5: Device breakdown ───────────────────────────────────────
    print("\n" + "=" * 60)
    print("📱 REPORT 5: Device Breakdown")
    print("=" * 60)

    device_data = fetch_blog_data(service, ["device"])
    if device_data:
        df_devices = pd.DataFrame(device_data)
        df_devices = df_devices.sort_values("clicks", ascending=False)

        for _, row in df_devices.iterrows():
            print(
                f"   {row['device']:<12} "
                f"Clicks: {row['clicks']:>6.0f}  "
                f"Impr: {row['impressions']:>8.0f}  "
                f"CTR: {row['ctr']:>5.1f}%  "
                f"Pos: {row['position']:>4.1f}"
            )

    # ── Report 6: Country breakdown ──────────────────────────────────────
    print("\n" + "=" * 60)
    print("🌍 REPORT 6: Country Breakdown (Top 15)")
    print("=" * 60)

    country_data = fetch_blog_data(service, ["country"])
    if country_data:
        df_countries = pd.DataFrame(country_data)
        df_countries = df_countries.sort_values("clicks", ascending=False)

        csv_path = OUTPUT_DIR / f"gsc_blog_countries_{timestamp}.csv"
        df_countries.to_csv(csv_path, index=False)
        print(f"\n   💾 Saved to: {csv_path}")

        for _, row in df_countries.head(15).iterrows():
            print(
                f"   {row['country']:<6} "
                f"Clicks: {row['clicks']:>6.0f}  "
                f"Impr: {row['impressions']:>8.0f}  "
                f"CTR: {row['ctr']:>5.1f}%  "
                f"Pos: {row['position']:>4.1f}"
            )

    print("\n" + "=" * 60)
    print("✅ All reports generated! CSV files saved in:")
    print(f"   {OUTPUT_DIR}")
    print("=" * 60)


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    print("╔══════════════════════════════════════════════════════════╗")
    print("║   Bluestone Blog – Search Console Data Extractor        ║")
    print("╠══════════════════════════════════════════════════════════╣")
    print(f"║   Property:   {SITE_URL:<42} ║")
    print(f"║   Blog filter: {BLOG_URL_PREFIX:<41} ║")
    print(f"║   Date range:  {START_DATE} → {END_DATE}              ║")
    print("╚══════════════════════════════════════════════════════════╝")

    creds = authenticate()
    service = build("searchconsole", "v1", credentials=creds)

    generate_reports(service)


if __name__ == "__main__":
    main()
