#!/usr/bin/env python3
"""
Bluestone SEO Dashboard Generator with Strategy Pivot (July 16, 2026)
====================================================================
Partitions blogs into:
  - New Strategy (Published >= July 16, 2026)
  - Legacy Strategy (Published < July 16, 2026)
"""

import os
import json
import sys
import html
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from pathlib import Path
import requests

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
SITE_URL = "sc-domain:bluestone.com"

SCRIPT_DIR = Path(__file__).parent
TOKEN_FILE = SCRIPT_DIR / "gsc_token.json"
DASHBOARD_DIR = SCRIPT_DIR.parent / "dashboard"
DATA_JSON_PATH = DASHBOARD_DIR / "dashboard_data.json"

WP_URL = "https://blog.bluestone.com/wp-json/wp/v2/posts"
WP_AUTH = ("blogbluestone", "4lKn pjRK GUtF Yts5 VzwF jcwd")

STRATEGY_PIVOT_DATE = datetime(2026, 7, 16)

END_DATE = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
START_DATE = (datetime.now() - timedelta(days=32)).strftime("%Y-%m-%d")

def normalize_url(url):
    if not url:
        return ""
    url = url.strip()
    if not url.endswith('/'):
        url += '/'
    return url

def extract_slug(url):
    return url.strip().rstrip('/').split('/')[-1]

def fetch_wp_page(page):
    try:
        r = requests.get(
            f"{WP_URL}?per_page=100&page={page}&status=publish",
            auth=WP_AUTH,
            timeout=15
        )
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list):
                return page, data
    except Exception as e:
        pass
    return page, []

def fetch_wp_posts_parallel(max_pages=20):
    print(f"📥 Fetching WordPress posts (up to {max_pages * 100} posts)...")
    all_posts_map = {}
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(fetch_wp_page, p) for p in range(1, max_pages + 1)]
        for f in as_completed(futures):
            page_num, posts = f.result()
            if posts:
                all_posts_map[page_num] = posts
    
    all_posts = []
    for p in sorted(all_posts_map.keys()):
        all_posts.extend(all_posts_map[p])
    
    print(f"✅ Total fetched WP posts: {len(all_posts)}")
    return all_posts

def fetch_gsc_data(service):
    print("📊 Querying Google Search Console API...")
    
    # 1. Page metrics (paginated)
    p_rows = []
    start_row = 0
    row_limit = 25000
    while True:
        p_req = {
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
            "rowLimit": row_limit,
            "startRow": start_row,
            "dataState": "all"
        }
        p_res = service.searchanalytics().query(siteUrl=SITE_URL, body=p_req).execute()
        batch = p_res.get("rows", [])
        p_rows.extend(batch)
        if len(batch) < row_limit:
            break
        start_row += len(batch)

    print(f"   Fetched {len(p_rows)} blog pages from GSC.")

    gsc_page_map = {}
    for r in p_rows:
        raw_url = r["keys"][0]
        norm_url = normalize_url(raw_url)
        slug = extract_slug(raw_url)
        item = {
            "page": norm_url,
            "clicks": int(r.get("clicks", 0)),
            "impressions": int(r.get("impressions", 0)),
            "ctr": round(r.get("ctr", 0) * 100, 2),
            "position": round(r.get("position", 0), 1)
        }
        gsc_page_map[norm_url] = item
        gsc_page_map[norm_url.rstrip('/')] = item
        gsc_page_map[slug] = item

    # 2. Page + Query metrics (paginated to fetch all 16,800+ rows)
    pq_rows = []
    start_row = 0
    while True:
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
            "rowLimit": row_limit,
            "startRow": start_row,
            "dataState": "all"
        }
        pq_res = service.searchanalytics().query(siteUrl=SITE_URL, body=pq_req).execute()
        batch = pq_res.get("rows", [])
        pq_rows.extend(batch)
        if len(batch) < row_limit:
            break
        start_row += len(batch)

    print(f"   Fetched {len(pq_rows)} page+query pairs from GSC.")

    queries_by_page = {}
    for r in pq_rows:
        raw_url = r["keys"][0]
        norm_url = normalize_url(raw_url)
        slug = extract_slug(raw_url)
        q_item = {
            "query": r["keys"][1],
            "clicks": int(r.get("clicks", 0)),
            "impressions": int(r.get("impressions", 0)),
            "ctr": round(r.get("ctr", 0) * 100, 2),
            "position": round(r.get("position", 0), 1)
        }
        for key in (norm_url, norm_url.rstrip('/'), slug):
            if key not in queries_by_page:
                queries_by_page[key] = []
            queries_by_page[key].append(q_item)

    for k in queries_by_page:
        queries_by_page[k].sort(key=lambda x: (x['clicks'], x['impressions']), reverse=True)

    # 3. Page + Date metrics (to extract exact First Indexed Date per page)
    pd_rows = []
    start_row = 0
    while True:
        pd_req = {
            "startDate": START_DATE,
            "endDate": END_DATE,
            "dimensions": ["page", "date"],
            "dimensionFilterGroups": [{
                "filters": [{
                    "dimension": "page",
                    "operator": "includingRegex",
                    "expression": r"^https://blog\.bluestone\.com/"
                }]
            }],
            "rowLimit": row_limit,
            "startRow": start_row,
            "dataState": "all"
        }
        pd_res = service.searchanalytics().query(siteUrl=SITE_URL, body=pd_req).execute()
        batch = pd_res.get("rows", [])
        pd_rows.extend(batch)
        if len(batch) < row_limit:
            break
        start_row += len(batch)

    first_indexed_map = {}
    for r in pd_rows:
        raw_url = r["keys"][0]
        date_str = r["keys"][1]
        impressions = int(r.get("impressions", 0))
        if impressions > 0:
            norm_url = normalize_url(raw_url)
            slug = extract_slug(raw_url)
            for key in (norm_url, norm_url.rstrip('/'), slug):
                if key not in first_indexed_map or date_str < first_indexed_map[key]:
                    first_indexed_map[key] = date_str

    print(f"   Detected First Indexed Date for {len(first_indexed_map)} blog pages.")

    # 4. Daily trends
    dt_req = {
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
        "dataState": "all"
    }
    dt_res = service.searchanalytics().query(siteUrl=SITE_URL, body=dt_req).execute()
    daily_trends = []
    for r in dt_res.get("rows", []):
        daily_trends.append({
            "date": r["keys"][0],
            "clicks": int(r.get("clicks", 0)),
            "impressions": int(r.get("impressions", 0)),
            "ctr": round(r.get("ctr", 0) * 100, 2),
            "position": round(r.get("position", 0), 1)
        })
    daily_trends.sort(key=lambda x: x["date"])

    # 4. Devices
    dev_req = {
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
        "dataState": "all"
    }
    dev_res = service.searchanalytics().query(siteUrl=SITE_URL, body=dev_req).execute()
    devices = []
    for r in dev_res.get("rows", []):
        devices.append({
            "device": r["keys"][0].upper(),
            "clicks": int(r.get("clicks", 0)),
            "impressions": int(r.get("impressions", 0)),
            "ctr": round(r.get("ctr", 0) * 100, 2),
            "position": round(r.get("position", 0), 1)
        })

    return gsc_page_map, queries_by_page, daily_trends, devices, first_indexed_map

def get_health_tier(pos, impressions):
    if pos > 0 and pos <= 3:
        return "Top 3 Rank", "success", "🟢"
    elif pos > 3 and pos <= 10:
        return "Page 1 (Pos 4-10)", "info", "🔵"
    elif pos > 10 and pos <= 20:
        return "Striking Distance (11-20)", "warning", "🟡"
    elif pos > 20:
        return "Low Rank (>20)", "danger", "🔴"
    elif impressions > 0:
        return "Indexed (No Rank)", "neutral", "⚪"
    else:
        return "New / Pending Index", "secondary", "⏳"

def compute_group_stats(group_list):
    clicks = sum(b["clicks"] for b in group_list)
    impressions = sum(b["impressions"] for b in group_list)
    ctrs = [b["ctr"] for b in group_list if b["impressions"] > 0]
    positions = [b["position"] for b in group_list if b["position"] > 0]
    indexed_count = len([b for b in group_list if b["impressions"] > 0])
    
    return {
        "count": len(group_list),
        "total_clicks": clicks,
        "total_impressions": impressions,
        "avg_ctr": round(sum(ctrs)/len(ctrs), 2) if ctrs else 0.0,
        "avg_position": round(sum(positions)/len(positions), 1) if positions else 0.0,
        "indexed_count": indexed_count,
        "indexing_rate": round(indexed_count / len(group_list) * 100, 1) if group_list else 0.0
    }

def main():
    if not TOKEN_FILE.exists():
        print(f"❌ Token file missing: {TOKEN_FILE}")
        sys.exit(1)

    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    service = build("searchconsole", "v1", credentials=creds)

    # Read previous dataset for BEFORE vs AFTER comparison
    prev_data = {}
    if DATA_JSON_PATH.exists():
        try:
            with open(DATA_JSON_PATH, "r", encoding="utf-8") as f:
                prev_data = json.load(f)
        except Exception:
            pass

    wp_posts = fetch_wp_posts_parallel(max_pages=15)
    gsc_page_map, queries_by_page, daily_trends, devices, first_indexed_map = fetch_gsc_data(service)

    processed_blogs = []
    seen_urls = set()

    for index, post in enumerate(wp_posts):
        title = html.unescape(post.get("title", {}).get("rendered", "Untitled"))
        link = normalize_url(post.get("link", ""))
        slug = post.get("slug", "") or extract_slug(link)
        date_raw = post.get("date", "")
        
        is_new_strategy = False
        if date_raw:
            try:
                dt = datetime.strptime(date_raw.split("T")[0], "%Y-%m-%d")
                formatted_date = dt.strftime("%b %d, %Y")
                if dt >= STRATEGY_PIVOT_DATE:
                    is_new_strategy = True
            except Exception:
                formatted_date = date_raw
        else:
            formatted_date = "N/A"

        gsc = gsc_page_map.get(link) or gsc_page_map.get(link.rstrip('/')) or gsc_page_map.get(slug) or {
            "clicks": 0,
            "impressions": 0,
            "ctr": 0.0,
            "position": 0.0
        }

        # Detect First Indexed Date
        idx_raw = first_indexed_map.get(link) or first_indexed_map.get(link.rstrip('/')) or first_indexed_map.get(slug)
        first_indexed_date = "Not Indexed Yet"
        indexing_lag_days = None
        if idx_raw:
            try:
                idx_dt = datetime.strptime(idx_raw, "%Y-%m-%d")
                first_indexed_date = idx_dt.strftime("%b %d, %Y")
                if date_raw:
                    pub_dt = datetime.strptime(date_raw.split("T")[0], "%Y-%m-%d")
                    indexing_lag_days = max(0, (idx_dt - pub_dt).days)
            except Exception:
                first_indexed_date = idx_raw
        elif gsc["impressions"] > 0:
            first_indexed_date = "Indexed (Date Pending)"

        q_list = queries_by_page.get(link) or queries_by_page.get(link.rstrip('/')) or queries_by_page.get(slug) or []
        unique_q = []
        seen_q = set()
        for q in q_list:
            if q["query"] not in seen_q:
                seen_q.add(q["query"])
                unique_q.append(q)

        health, health_color, health_icon = get_health_tier(gsc["position"], gsc["impressions"])

        blog_obj = {
            "wp_id": post.get("id"),
            "title": title,
            "link": link,
            "slug": slug,
            "published_date": formatted_date,
            "raw_date": date_raw,
            "first_indexed_date": first_indexed_date,
            "indexing_lag_days": indexing_lag_days,
            "is_new_strategy": is_new_strategy,
            "strategy_label": "🚀 New Strategy (Post-July 16)" if is_new_strategy else "📜 Pre-July 16",
            "strategy_badge": "new-strategy" if is_new_strategy else "legacy-strategy",
            "clicks": gsc["clicks"],
            "impressions": gsc["impressions"],
            "ctr": gsc["ctr"],
            "position": gsc["position"],
            "health": health,
            "health_color": health_color,
            "health_icon": health_icon,
            "wp_index": index + 1,
            "top_queries": unique_q[:10]
        }
        processed_blogs.append(blog_obj)
        seen_urls.add(link)
        seen_urls.add(link.rstrip('/'))
        seen_urls.add(slug)

    for url_key, gsc in gsc_page_map.items():
        if url_key in seen_urls or not url_key.startswith("https://"):
            continue
        norm_url = normalize_url(url_key)
        slug = extract_slug(norm_url)
        if slug in seen_urls or norm_url in seen_urls:
            continue

        q_list = queries_by_page.get(norm_url) or []
        unique_q = []
        seen_q = set()
        for q in q_list:
            if q["query"] not in seen_q:
                seen_q.add(q["query"])
                unique_q.append(q)

        title_from_slug = slug.replace("-", " ").title()
        health, health_color, health_icon = get_health_tier(gsc["position"], gsc["impressions"])

        idx_raw = first_indexed_map.get(norm_url) or first_indexed_map.get(slug)
        first_indexed_date = "Earlier"
        if idx_raw:
            try:
                first_indexed_date = datetime.strptime(idx_raw, "%Y-%m-%d").strftime("%b %d, %Y")
            except Exception:
                first_indexed_date = idx_raw

        blog_obj = {
            "wp_id": None,
            "title": title_from_slug,
            "link": norm_url,
            "slug": slug,
            "published_date": "Earlier",
            "raw_date": "2025-01-01T00:00:00",
            "first_indexed_date": first_indexed_date,
            "indexing_lag_days": None,
            "is_new_strategy": False,
            "strategy_label": "📜 Pre-July 16",
            "strategy_badge": "legacy-strategy",
            "clicks": gsc["clicks"],
            "impressions": gsc["impressions"],
            "ctr": gsc["ctr"],
            "position": gsc["position"],
            "health": health,
            "health_color": health_color,
            "health_icon": health_icon,
            "wp_index": 9999,
            "top_queries": unique_q[:10]
        }
        processed_blogs.append(blog_obj)
        seen_urls.add(norm_url)

    # Filter Strategy Groups
    post_july16_blogs = sorted([b for b in processed_blogs if b["is_new_strategy"]], key=lambda x: x["raw_date"], reverse=True)
    pre_july16_blogs = sorted([b for b in processed_blogs if not b["is_new_strategy"]], key=lambda x: (x["clicks"], x["impressions"]), reverse=True)
    top_100_performing = sorted(processed_blogs, key=lambda x: (x["clicks"], x["impressions"]), reverse=True)[:100]
    striking_distance = [b for b in processed_blogs if 10.0 < b["position"] <= 20.0 and b["impressions"] > 500]
    striking_distance = sorted(striking_distance, key=lambda x: x["impressions"], reverse=True)[:100]

    # Compute Calendar Week publish volumes (Monday to Today vs Prev Monday to Sunday)
    now = datetime.now()
    # Monday of current week
    current_mon = datetime(now.year, now.month, now.day) - timedelta(days=now.weekday())
    prev_mon = current_mon - timedelta(days=7)
    prev_sun = current_mon - timedelta(days=1)

    published_this_week = 0   # Mon to Today
    published_last_week = 0   # Prev Mon to Prev Sun
    published_30d = 0

    for b in processed_blogs:
        date_raw = b.get("raw_date", "")
        if date_raw and "T" in date_raw:
            try:
                dt = datetime.strptime(date_raw.split("T")[0], "%Y-%m-%d")
                if current_mon <= dt <= now:
                    published_this_week += 1
                elif prev_mon <= dt <= prev_sun:
                    published_last_week += 1
                if (now - dt).days <= 30:
                    published_30d += 1
            except Exception:
                pass

    strategy_comparison = {
        "pivot_date": "July 16, 2026",
        "published_this_week": published_this_week,
        "published_last_week": published_last_week,
        "published_last_30_days": published_30d,
        "new_strategy": compute_group_stats(post_july16_blogs),
        "legacy_strategy": compute_group_stats(pre_july16_blogs),
        "overall": compute_group_stats(processed_blogs)
    }

    payload = {
        "metadata": {
            "generated_at": datetime.now().strftime("%b %d, %Y %I:%M %p"),
            "start_date": START_DATE,
            "end_date": END_DATE,
            "strategy_pivot_date": "2026-07-16",
            "total_wp_posts_fetched": len(wp_posts),
            "total_all_blogs": len(processed_blogs),
            "strategy_comparison": strategy_comparison
        },
        "post_july16_blogs": post_july16_blogs,
        "pre_july16_blogs": pre_july16_blogs,
        "top_100_performing": top_100_performing,
        "striking_distance": striking_distance,
        "all_blogs": processed_blogs,
        "daily_trends": daily_trends,
        "devices": devices
    }

    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    # Print BEFORE vs AFTER Comparison Summary
    prev_meta = prev_data.get("metadata", {})
    prev_strat = prev_meta.get("strategy_comparison", {})
    prev_new = prev_strat.get("new_strategy", {})

    prev_total_wp = prev_meta.get("total_wp_posts_fetched", 0)
    prev_post_cnt = prev_new.get("count", 0)
    prev_post_idx = prev_new.get("indexed_count", 0)
    prev_post_clk = prev_new.get("total_clicks", 0)
    prev_post_imp = prev_new.get("total_impressions", 0)

    curr_total_wp = len(wp_posts)
    curr_post_cnt = len(post_july16_blogs)
    curr_post_idx = strategy_comparison["new_strategy"]["indexed_count"]
    curr_post_clk = strategy_comparison["new_strategy"]["total_clicks"]
    curr_post_imp = strategy_comparison["new_strategy"]["total_impressions"]

    def format_diff(curr, prev):
        if not prev:
            return f"{curr:,}"
        diff = curr - prev
        if diff > 0:
            return f"{prev:,} ➔ {curr:,}  (▲ +{diff:,})"
        elif diff < 0:
            return f"{prev:,} ➔ {curr:,}  (▼ {abs(diff):,})"
        else:
            return f"{curr:,}  (No change)"

    print("\n" + "=" * 62)
    print("📊 DASHBOARD UPDATE SUMMARY (BEFORE vs AFTER):")
    print("=" * 62)
    print(f" • Total WP Posts Published : {format_diff(curr_total_wp, prev_total_wp)}")
    print(f" • Post-July 16 Articles    : {format_diff(curr_post_cnt, prev_post_cnt)}")
    print(f" • Post-July 16 Indexed URLs: {format_diff(curr_post_idx, prev_post_idx)}")
    print(f" • Post-July 16 Search Clicks: {format_diff(curr_post_clk, prev_post_clk)}")
    print(f" • Post-July 16 Impressions  : {format_diff(curr_post_imp, prev_post_imp)}")
    print("=" * 62 + "\n")

if __name__ == "__main__":
    main()
