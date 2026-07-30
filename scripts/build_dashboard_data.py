#!/usr/bin/env python3
"""
Fetch 100 Most Recent WP Blogs & Merge with Search Console Data
================================================================
Generates dashboard_data.json used by the web dashboard.
"""

import os
import json
import sys
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path
import requests

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
SITE_URL = "sc-domain:bluestone.com"

SCRIPT_DIR = Path(__file__).parent
TOKEN_FILE = SCRIPT_DIR / "gsc_token.json"
OUTPUT_DIR = SCRIPT_DIR.parent / "dashboard"
DATA_JSON_PATH = OUTPUT_DIR / "dashboard_data.json"

WP_URL = "https://blog.bluestone.com/wp-json/wp/v2/posts"
WP_AUTH = ("blogbluestone", "4lKn pjRK GUtF Yts5 VzwF jcwd")

# Date range: last 30 days
END_DATE = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
START_DATE = (datetime.now() - timedelta(days=33)).strftime("%Y-%m-%d")

def fetch_wp_posts(limit=100):
    print(f"📥 Fetching last {limit} posts from WordPress REST API...")
    posts = []
    page = 1
    per_page = 100
    while len(posts) < limit:
        r = requests.get(
            f"{WP_URL}?per_page={per_page}&page={page}&status=publish",
            auth=WP_AUTH,
            timeout=15
        )
        if r.status_code != 200:
            print(f"⚠️ Error fetching WP page {page}: {r.status_code}")
            break
        data = r.json()
        if not data:
            break
        posts.extend(data)
        if len(data) < per_page:
            break
        page += 1
    
    posts = posts[:limit]
    print(f"✅ Fetched {len(posts)} posts from WordPress.")
    return posts

def normalize_url(url):
    """Normalize URL to match GSC page format (ensure trailing slash or consistent format)."""
    url = url.strip()
    if not url.endswith('/'):
        url += '/'
    return url

def fetch_gsc_data(service):
    print("📊 Fetching Search Analytics from GSC...")
    
    # 1. Page stats
    page_req = {
        "startDate": START_DATE,
        "endDate": END_DATE,
        "dimensions": ["page"],
        "dimensionFilterGroups": [{
            "filters": [{
                "dimension": "page",
                "operator": "includingRegex",
                "expression": r"^https://blog\.bluestone\.com/"
            }]
        }],
        "rowLimit": 5000,
        "dataState": "final"
    }
    resp_page = service.searchanalytics().query(siteUrl=SITE_URL, body=page_req).execute()
    page_dict = {}
    for r in resp_page.get("rows", []):
        url = normalize_url(r["keys"][0])
        page_dict[url] = {
            "clicks": r.get("clicks", 0),
            "impressions": r.get("impressions", 0),
            "ctr": round(r.get("ctr", 0) * 100, 2),
            "position": round(r.get("position", 0), 1)
        }
        # Also store without trailing slash just in case
        page_dict[url.rstrip('/')] = page_dict[url]

    # 2. Page + Query stats
    pq_req = {
        "startDate": START_DATE,
        "endDate": END_DATE,
        "dimensions": ["page", "query"],
        "dimensionFilterGroups": [{
            "filters": [{
                "dimension": "page",
                "operator": "includingRegex",
                "expression": r"^https://blog\.bluestone\.com/"
            }]
        }],
        "rowLimit": 5000,
        "dataState": "final"
    }
    resp_pq = service.searchanalytics().query(siteUrl=SITE_URL, body=pq_req).execute()
    page_queries = {}
    for r in resp_pq.get("rows", []):
        url = normalize_url(r["keys"][0])
        q_item = {
            "query": r["keys"][1],
            "clicks": r.get("clicks", 0),
            "impressions": r.get("impressions", 0),
            "ctr": round(r.get("ctr", 0) * 100, 2),
            "position": round(r.get("position", 0), 1)
        }
        if url not in page_queries:
            page_queries[url] = []
            page_queries[url.rstrip('/')] = page_queries[url]
        page_queries[url].append(q_item)

    # Sort queries per page by clicks
    for url in page_queries:
        page_queries[url].sort(key=lambda x: (x['clicks'], x['impressions']), reverse=True)

    # 3. Daily trends
    date_req = {
        "startDate": START_DATE,
        "endDate": END_DATE,
        "dimensions": ["date"],
        "dimensionFilterGroups": [{
            "filters": [{
                "dimension": "page",
                "operator": "includingRegex",
                "expression": r"^https://blog\.bluestone\.com/"
            }]
        }],
        "rowLimit": 5000,
        "dataState": "final"
    }
    resp_date = service.searchanalytics().query(siteUrl=SITE_URL, body=date_req).execute()
    daily_trends = []
    for r in resp_date.get("rows", []):
        daily_trends.append({
            "date": r["keys"][0],
            "clicks": r.get("clicks", 0),
            "impressions": r.get("impressions", 0),
            "ctr": round(r.get("ctr", 0) * 100, 2),
            "position": round(r.get("position", 0), 1)
        })
    daily_trends.sort(key=lambda x: x["date"])

    # 4. Device breakdown
    device_req = {
        "startDate": START_DATE,
        "endDate": END_DATE,
        "dimensions": ["device"],
        "dimensionFilterGroups": [{
            "filters": [{
                "dimension": "page",
                "operator": "includingRegex",
                "expression": r"^https://blog\.bluestone\.com/"
            }]
        }],
        "rowLimit": 10,
        "dataState": "final"
    }
    resp_device = service.searchanalytics().query(siteUrl=SITE_URL, body=device_req).execute()
    devices = []
    for r in resp_device.get("rows", []):
        devices.append({
            "device": r["keys"][0],
            "clicks": r.get("clicks", 0),
            "impressions": r.get("impressions", 0),
            "ctr": round(r.get("ctr", 0) * 100, 2),
            "position": round(r.get("position", 0), 1)
        })

    return page_dict, page_queries, daily_trends, devices

def main():
    if not TOKEN_FILE.exists():
        print(f"❌ Missing token file: {TOKEN_FILE}")
        sys.exit(1)

    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    service = build("searchconsole", "v1", credentials=creds)

    wp_posts = fetch_wp_posts(limit=100)
    page_dict, page_queries, daily_trends, devices = fetch_gsc_data(service)

    blogs_data = []
    total_clicks = 0
    total_impressions = 0
    clicks_list = []
    ctr_list = []
    pos_list = []

    for post in wp_posts:
        title = post.get("title", {}).get("rendered", "Untitled")
        # Clean HTML entities in title
        import html
        title = html.unescape(title)
        
        link = normalize_url(post.get("link", ""))
        date_pub = post.get("date", "")
        if date_pub:
            formatted_date = datetime.strptime(date_pub.split("T")[0], "%Y-%m-%d").strftime("%b %d, %Y")
        else:
            formatted_date = "Unknown"

        slug = post.get("slug", "")

        # Get GSC metrics
        gsc = page_dict.get(link) or page_dict.get(link.rstrip('/')) or {
            "clicks": 0,
            "impressions": 0,
            "ctr": 0.0,
            "position": 0.0
        }

        queries = page_queries.get(link) or page_queries.get(link.rstrip('/')) or []

        clicks = gsc["clicks"]
        impressions = gsc["impressions"]
        ctr = gsc["ctr"]
        pos = gsc["position"]

        total_clicks += clicks
        total_impressions += impressions
        if impressions > 0:
            clicks_list.append(clicks)
            ctr_list.append(ctr)
            pos_list.append(pos)

        # Health tier assessment
        if pos > 0 and pos <= 3:
            health = "Top 3 Rank"
            health_color = "success"
        elif pos > 3 and pos <= 10:
            health = "Page 1 (Pos 4-10)"
            health_color = "info"
        elif pos > 10 and pos <= 20:
            health = "Striking Distance (11-20)"
            health_color = "warning"
        elif pos > 20:
            health = "Low Rank (>20)"
            health_color = "danger"
        else:
            health = "No Search Data"
            health_color = "secondary"

        blogs_data.append({
            "id": post.get("id"),
            "title": title,
            "link": link,
            "slug": slug,
            "published_date": formatted_date,
            "raw_date": date_pub,
            "clicks": clicks,
            "impressions": impressions,
            "ctr": ctr,
            "position": pos,
            "health": health,
            "health_color": health_color,
            "top_queries": queries[:10]  # top 10 queries
        })

    avg_ctr = round(sum(ctr_list) / len(ctr_list), 2) if ctr_list else 0.0
    avg_pos = round(sum(pos_list) / len(pos_list), 1) if pos_list else 0.0

    output_payload = {
        "metadata": {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "start_date": START_DATE,
            "end_date": END_DATE,
            "total_blogs": len(blogs_data),
            "total_clicks": total_clicks,
            "total_impressions": total_impressions,
            "avg_ctr": avg_ctr,
            "avg_position": avg_pos
        },
        "blogs": blogs_data,
        "daily_trends": daily_trends,
        "devices": devices
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(output_payload, f, indent=2, ensure_ascii=False)

    print(f"🎉 Successfully saved dataset to {DATA_JSON_PATH}")

if __name__ == "__main__":
    main()
