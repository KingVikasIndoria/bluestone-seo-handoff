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
INDEXED_HISTORY_PATH = SCRIPT_DIR / "indexed_urls_history.json"

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

    # 4. Daily trends (Date + Page dimensions)
    dt_req = {
        "startDate": START_DATE,
        "endDate": END_DATE,
        "dimensions": ["date", "page"],
        "dimensionFilterGroups": [{
            "filters": [{
                "dimension": "page",
                "operator": "includingRegex",
                "expression": r"^https://blog\.bluestone\.com/"
            }]
        }],
        "rowLimit": 25000,
        "dataState": "all"
    }
    dt_res = service.searchanalytics().query(siteUrl=SITE_URL, body=dt_req).execute()
    raw_daily_rows = dt_res.get("rows", [])
    # 5. Devices
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

    # 6. Weekly 7-day windows for 3-week rank breakdown progress
    w3_end = datetime.strptime(END_DATE, "%Y-%m-%d")
    w3_start = w3_end - timedelta(days=6)
    w2_end = w3_start - timedelta(days=1)
    w2_start = w2_end - timedelta(days=6)
    w1_end = w2_start - timedelta(days=1)
    w1_start = w1_end - timedelta(days=6)

    week_labels = [
        f"{w1_start.strftime('%d %b')} - {w1_end.strftime('%d %b')}",
        f"{w2_start.strftime('%d %b')} - {w2_end.strftime('%d %b')}",
        f"{w3_start.strftime('%d %b')} - {w3_end.strftime('%d %b')}"
    ]

    def fetch_weekly_page_map(s_date, e_date):
        req = {
            "startDate": s_date.strftime("%Y-%m-%d"),
            "endDate": e_date.strftime("%Y-%m-%d"),
            "dimensions": ["page"],
            "dimensionFilterGroups": [{
                "filters": [{
                    "dimension": "page",
                    "operator": "includingRegex",
                    "expression": r"^https://blog\.bluestone\.com/"
                }]
            }],
            "rowLimit": 10000,
            "dataState": "all"
        }
        res = service.searchanalytics().query(siteUrl=SITE_URL, body=req).execute()
        p_map = {}
        for r in res.get("rows", []):
            raw_url = r["keys"][0]
            norm_url = normalize_url(raw_url)
            slug = extract_slug(raw_url)
            item = {
                "clicks": int(r.get("clicks", 0)),
                "impressions": int(r.get("impressions", 0)),
                "position": round(r.get("position", 0), 1)
            }
            for k in (norm_url, norm_url.rstrip('/'), slug):
                p_map[k] = item
        return p_map

    print("📊 Querying GSC 3-week rank progress data...")
    w1_page_map = fetch_weekly_page_map(w1_start, w1_end)
    w2_page_map = fetch_weekly_page_map(w2_start, w2_end)
    w3_page_map = fetch_weekly_page_map(w3_start, w3_end)

    return gsc_page_map, queries_by_page, raw_daily_rows, devices, first_indexed_map, w1_page_map, w2_page_map, w3_page_map, week_labels

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

def load_indexed_history():
    """Load persistent set of URLs ever seen as indexed."""
    if INDEXED_HISTORY_PATH.exists():
        try:
            with open(INDEXED_HISTORY_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return set(data.get("indexed_urls", []))
        except Exception:
            pass
    return set()

def save_indexed_history(indexed_set):
    """Save persistent set of indexed URLs."""
    with open(INDEXED_HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump({"indexed_urls": sorted(indexed_set), "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M")}, f, indent=2)

def compute_group_stats(group_list, persistent_indexed_urls=None):
    clicks = sum(b["clicks"] for b in group_list)
    impressions = sum(b["impressions"] for b in group_list)
    ctrs = [b["ctr"] for b in group_list if b["impressions"] > 0]
    positions = [b["position"] for b in group_list if b["position"] > 0]
    
    # Use persistent indexed count if available (never goes down)
    if persistent_indexed_urls is not None:
        indexed_count = len([b for b in group_list if normalize_url(b.get("link", "")) in persistent_indexed_urls or b.get("slug", "") in persistent_indexed_urls])
    else:
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

    # Load persistent indexed URL history
    indexed_history = load_indexed_history()

    wp_posts = fetch_wp_posts_parallel(max_pages=15)
    gsc_page_map, queries_by_page, raw_daily_rows, devices, first_indexed_map, w1_page_map, w2_page_map, w3_page_map, week_labels = fetch_gsc_data(service)

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

        w1_gsc = w1_page_map.get(link) or w1_page_map.get(link.rstrip('/')) or w1_page_map.get(slug) or {"position": 0.0, "impressions": 0}
        w2_gsc = w2_page_map.get(link) or w2_page_map.get(link.rstrip('/')) or w2_page_map.get(slug) or {"position": 0.0, "impressions": 0}
        w3_gsc = w3_page_map.get(link) or w3_page_map.get(link.rstrip('/')) or w3_page_map.get(slug) or {"position": 0.0, "impressions": 0}

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
            "weekly_rank": {
                "w1_pos": w1_gsc["position"],
                "w1_imp": w1_gsc["impressions"],
                "w2_pos": w2_gsc["position"],
                "w2_imp": w2_gsc["impressions"],
                "w3_pos": w3_gsc["position"],
                "w3_imp": w3_gsc["impressions"],
            },
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

        w1_gsc = w1_page_map.get(norm_url) or w1_page_map.get(slug) or {"position": 0.0, "impressions": 0}
        w2_gsc = w2_page_map.get(norm_url) or w2_page_map.get(slug) or {"position": 0.0, "impressions": 0}
        w3_gsc = w3_page_map.get(norm_url) or w3_page_map.get(slug) or {"position": 0.0, "impressions": 0}

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
            "weekly_rank": {
                "w1_pos": w1_gsc["position"],
                "w1_imp": w1_gsc["impressions"],
                "w2_pos": w2_gsc["position"],
                "w2_imp": w2_gsc["impressions"],
                "w3_pos": w3_gsc["position"],
                "w3_imp": w3_gsc["impressions"],
            },
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

    # Update persistent indexed history — add any URL that has impressions > 0 or has a detected first_indexed_date
    for b in processed_blogs:
        idx_str = b.get("first_indexed_date")
        if b.get("impressions", 0) > 0 or (idx_str and idx_str not in ["Not Indexed Yet", "Indexed (Date Pending)"]):
            indexed_history.add(normalize_url(b.get("link", "")))
            if b.get("slug"):
                indexed_history.add(b["slug"])
    save_indexed_history(indexed_history)

    # Flag explicit is_indexed boolean on every blog object
    for b in processed_blogs:
        norm = normalize_url(b.get("link", ""))
        slug = b.get("slug", "")
        b["is_indexed"] = (norm in indexed_history or slug in indexed_history or b.get("impressions", 0) > 0)

    # Build bifurcated daily_trends (New Strategy vs Old Strategy)
    post_slugs = set(b["slug"] for b in post_july16_blogs)
    post_links = set(normalize_url(b["link"]) for b in post_july16_blogs)

    daily_map = {}
    for r in raw_daily_rows:
        dt = r["keys"][0]
        page = r["keys"][1]
        norm_page = normalize_url(page)
        slug = norm_page.rstrip('/').split('/')[-1]
        c = int(r.get("clicks", 0))
        imp = int(r.get("impressions", 0))
        
        if dt not in daily_map:
            daily_map[dt] = {
                "date": dt,
                "new_clicks": 0,
                "new_impressions": 0,
                "old_clicks": 0,
                "old_impressions": 0,
                "clicks": 0,
                "impressions": 0
            }
        
        if slug in post_slugs or norm_page in post_links:
            daily_map[dt]["new_clicks"] += c
            daily_map[dt]["new_impressions"] += imp
        else:
            daily_map[dt]["old_clicks"] += c
            daily_map[dt]["old_impressions"] += imp
        
        daily_map[dt]["clicks"] += c
        daily_map[dt]["impressions"] += imp

    daily_trends = sorted(daily_map.values(), key=lambda x: x["date"])
    for d in daily_trends:
        try:
            d["date_formatted"] = datetime.strptime(d["date"], "%Y-%m-%d").strftime("%d %b")
        except Exception:
            d["date_formatted"] = d["date"]

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
        "new_strategy": compute_group_stats(post_july16_blogs, indexed_history),
        "legacy_strategy": compute_group_stats(pre_july16_blogs, indexed_history),
        "overall": compute_group_stats(processed_blogs, indexed_history)
    }

    # Build Post-July 16 Indexing Speed Trend (Daily & Cumulative from July 16 to Today)
    indexing_by_date = {}
    for b in post_july16_blogs:
        idx_str = b.get("first_indexed_date")
        if idx_str and idx_str not in ["Not Indexed Yet", "Indexed (Date Pending)"]:
            try:
                dt = datetime.strptime(idx_str, "%b %d, %Y")
                d_key = dt.strftime("%Y-%m-%d")
                indexing_by_date[d_key] = indexing_by_date.get(d_key, 0) + 1
            except Exception:
                pass

    start_dt = datetime(2026, 7, 16)
    end_dt = datetime.now()
    curr_dt = start_dt

    post_july16_indexing_trend = []
    cumulative = 0
    while curr_dt <= end_dt:
        d_key = curr_dt.strftime("%Y-%m-%d")
        daily_count = indexing_by_date.get(d_key, 0)
        cumulative += daily_count
        is_api_phase = (curr_dt >= datetime(2026, 7, 30))
        
        post_july16_indexing_trend.append({
            "date": d_key,
            "date_formatted": curr_dt.strftime("%d %b"),
            "daily_indexed": daily_count,
            "cumulative_indexed": cumulative,
            "is_api_phase": is_api_phase,
            "phase_label": "🚀 Indexing API Active" if is_api_phase else "Standard Search Crawl"
        })
        curr_dt += timedelta(days=1)

    def compute_3w_breakdown(blog_list):
        def empty_b():
            return {"pos1_3": 0, "pos4_10": 0, "pos11_20": 0, "pos21_plus": 0, "unindexed": 0}
        b1, b2, b3 = empty_b(), empty_b(), empty_b()
        for b in blog_list:
            w = b.get("weekly_rank", {})
            # W1
            w1_pos, w1_imp = w.get("w1_pos", 0), w.get("w1_imp", 0)
            if w1_imp == 0: b1["unindexed"] += 1
            elif 0 < w1_pos <= 3: b1["pos1_3"] += 1
            elif 3 < w1_pos <= 10: b1["pos4_10"] += 1
            elif 10 < w1_pos <= 20: b1["pos11_20"] += 1
            else: b1["pos21_plus"] += 1

            # W2
            w2_pos, w2_imp = w.get("w2_pos", 0), w.get("w2_imp", 0)
            if w2_imp == 0: b2["unindexed"] += 1
            elif 0 < w2_pos <= 3: b2["pos1_3"] += 1
            elif 3 < w2_pos <= 10: b2["pos4_10"] += 1
            elif 10 < w2_pos <= 20: b2["pos11_20"] += 1
            else: b2["pos21_plus"] += 1

            # W3
            w3_pos, w3_imp = w.get("w3_pos", 0), w.get("w3_imp", 0)
            if w3_imp == 0: b3["unindexed"] += 1
            elif 0 < w3_pos <= 3: b3["pos1_3"] += 1
            elif 3 < w3_pos <= 10: b3["pos4_10"] += 1
            elif 10 < w3_pos <= 20: b3["pos11_20"] += 1
            else: b3["pos21_plus"] += 1
        return {"w1": b1, "w2": b2, "w3": b3}

    rank_breakdown_3w = {
        "week_labels": week_labels,
        "new_strategy": compute_3w_breakdown(post_july16_blogs),
        "legacy_strategy": compute_3w_breakdown(pre_july16_blogs),
        "overall": compute_3w_breakdown(processed_blogs),
        "top100": compute_3w_breakdown(top_100_performing),
        "striking": compute_3w_breakdown(striking_distance)
    }

    payload = {
        "metadata": {
            "generated_at": datetime.now().strftime("%b %d, %Y %I:%M %p"),
            "start_date": START_DATE,
            "end_date": END_DATE,
            "strategy_pivot_date": "2026-07-16",
            "total_wp_posts_fetched": len(wp_posts),
            "total_all_blogs": len(processed_blogs),
            "strategy_comparison": strategy_comparison,
            "rank_breakdown_3w": rank_breakdown_3w
        },
        "post_july16_blogs": post_july16_blogs,
        "pre_july16_blogs": pre_july16_blogs,
        "top_100_performing": top_100_performing,
        "striking_distance": striking_distance,
        "all_blogs": processed_blogs,
        "daily_trends": daily_trends,
        "post_july16_indexing_trend": post_july16_indexing_trend,
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
