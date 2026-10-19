#!/usr/bin/env python3
"""
Bluestone SEO Dashboard Daily Email Summary with Embedded Visual Graphs
=======================================================================
Reads dashboard_data.json and sends a daily HTML email report with:
  - Key Performance Indicators (Clicks, Impressions, CTR, Avg Rank)
  - Interactive/Static Embedded Chart Images (via QuickChart.io):
      1. Weekly Search Traffic Breakdown (Last 10 Weeks) [Dual-axis line chart]
      2. Cumulative Strategy Indexing Growth (Published vs Indexed) [Area line chart]
  - Visual CSS Progress Meters for Indexing & Portfolio Status
  - Strategy Pivot Indexing Breakdown Table
  - 4-Week Publish Volume Breakdown
  - Top Recently Indexed Articles with Impression Counts

Supported delivery providers:
  1. Resend API (via RESEND_API_KEY)
  2. Standard SMTP (via SMTP_USER, SMTP_PASSWORD, SMTP_HOST, SMTP_PORT)
"""

import os
import sys
import json
import smtplib
import requests
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DATA_JSON_PATH = SCRIPT_DIR.parent / "dashboard_data.json"
if not DATA_JSON_PATH.exists():
    DATA_JSON_PATH = SCRIPT_DIR.parent / "dashboard" / "dashboard_data.json"

# Load local .env if present
ENV_FILE = SCRIPT_DIR.parent / ".env"
if ENV_FILE.exists():
    with open(ENV_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

def get_4w_publish_volume(all_blogs):
    now = datetime.now()
    dist_to_mon = now.weekday()
    current_mon = datetime(now.year, now.month, now.day) - timedelta(days=dist_to_mon)
    
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    weeks = []
    for i in range(4):
        w_start = current_mon - timedelta(days=(3 - i) * 7)
        w_end = w_start + timedelta(days=6)
        label = f"{w_start.day} {months[w_start.month - 1]} - {w_end.day} {months[w_end.month - 1]}"
        weeks.append({
            "start": w_start.date(),
            "end": w_end.date(),
            "label": label,
            "is_current": (i == 3),
            "count": 0
        })
    
    for b in all_blogs:
        raw = b.get("raw_date", "")
        if raw:
            try:
                dt = datetime.strptime(raw.split("T")[0], "%Y-%m-%d").date()
                for w in weeks:
                    if w["start"] <= dt <= w["end"]:
                        w["count"] += 1
            except Exception:
                pass
    
    return list(reversed(weeks))

def create_quickchart_url(chart_config, width=620, height=260):
    """Generates a high-res QuickChart image URL for email embedding."""
    try:
        res = requests.post(
            "https://quickchart.io/chart/create",
            json={
                "chart": chart_config,
                "width": width,
                "height": height,
                "backgroundColor": "#ffffff"
            },
            timeout=10
        )
        if res.status_code == 200 and res.json().get("success"):
            return res.json().get("url")
    except Exception as e:
        print(f"⚠️ QuickChart API error: {e}")
    # Fallback to direct GET URL
    return f"https://quickchart.io/chart?c={requests.utils.quote(json.dumps(chart_config))}&w={width}&h={height}&bkg=white"

def generate_report():
    if not DATA_JSON_PATH.exists():
        print(f"❌ Cannot find dashboard_data.json at {DATA_JSON_PATH}")
        sys.exit(1)
        
    with open(DATA_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    meta = data.get("metadata", {})
    generated_at = meta.get("generated_at", datetime.now().strftime("%b %d, %Y %I:%M %p"))
    sc = meta.get("strategy_comparison", {})
    new_strat = sc.get("new_strategy", {})
    leg_strat = sc.get("legacy_strategy", {})
    overall = sc.get("overall", {})
    
    all_blogs = data.get("all_blogs", [])
    post_blogs = data.get("post_july16_blogs", [])
    
    # 1. Generate 10-Week Traffic Chart
    w10 = data.get("weekly_trends_10w", [])
    t_labels = [w["week_label"] for w in w10]
    t_clicks = [w["clicks"] for w in w10]
    t_impressions = [w["impressions"] for w in w10]

    traffic_chart_config = {
        "type": "line",
        "data": {
            "labels": t_labels,
            "datasets": [
                {
                    "label": "Clicks",
                    "data": t_clicks,
                    "borderColor": "#4f46e5",
                    "backgroundColor": "rgba(79, 70, 229, 0.12)",
                    "yAxisID": "y-clicks",
                    "fill": True,
                    "borderWidth": 3,
                    "pointRadius": 4,
                    "pointBackgroundColor": "#4f46e5"
                },
                {
                    "label": "Impressions",
                    "data": t_impressions,
                    "borderColor": "#0284c7",
                    "backgroundColor": "rgba(2, 132, 199, 0.05)",
                    "yAxisID": "y-imp",
                    "fill": False,
                    "borderDash": [5, 5],
                    "borderWidth": 2,
                    "pointRadius": 4,
                    "pointBackgroundColor": "#0284c7"
                }
            ]
        },
        "options": {
            "title": {
                "display": True,
                "text": "Weekly Traffic Breakdown (Last 10 Weeks)",
                "fontSize": 13,
                "fontColor": "#1e293b",
                "fontStyle": "bold"
            },
            "legend": {"position": "top"},
            "scales": {
                "yAxes": [
                    {"id": "y-clicks", "type": "linear", "position": "left", "ticks": {"beginAtZero": True}},
                    {"id": "y-imp", "type": "linear", "position": "right", "gridLines": {"drawOnChartArea": False}, "ticks": {"beginAtZero": True}}
                ]
            }
        }
    }
    traffic_chart_url = create_quickchart_url(traffic_chart_config, width=620, height=260)

    # 2. Generate Indexing Growth Trajectory Chart
    w_idx = data.get("weekly_indexing_trend", [])
    idx_labels = [w["week_label"] for w in w_idx]
    cum_pub = [w.get("cumulative_published", 0) for w in w_idx]
    cum_idx = [w.get("cumulative_indexed", 0) for w in w_idx]

    indexing_chart_config = {
        "type": "line",
        "data": {
            "labels": idx_labels,
            "datasets": [
                {
                    "label": "Cumulative Published",
                    "data": cum_pub,
                    "borderColor": "#94a3b8",
                    "backgroundColor": "rgba(148, 163, 184, 0.08)",
                    "fill": True,
                    "borderWidth": 2,
                    "pointRadius": 3
                },
                {
                    "label": "Cumulative Indexed (700+ Milestone)",
                    "data": cum_idx,
                    "borderColor": "#16a34a",
                    "backgroundColor": "rgba(22, 163, 74, 0.18)",
                    "fill": True,
                    "borderWidth": 3,
                    "pointRadius": 3,
                    "pointBackgroundColor": "#16a34a"
                }
            ]
        },
        "options": {
            "title": {
                "display": True,
                "text": "Strategy Indexing Growth Trajectory (Post-July 16)",
                "fontSize": 13,
                "fontColor": "#1e293b",
                "fontStyle": "bold"
            },
            "legend": {"position": "top"},
            "scales": {
                "yAxes": [{"ticks": {"beginAtZero": True}}]
            }
        }
    }
    indexing_chart_url = create_quickchart_url(indexing_chart_config, width=620, height=260)

    # 4-week publish breakdown
    weeks_4w = get_4w_publish_volume(all_blogs)
    
    # Recently indexed articles
    recent_indexed = []
    for b in post_blogs:
        f_idx = b.get("first_indexed_date")
        if f_idx and f_idx not in ["Not Indexed Yet", "Indexed (Date Pending)"]:
            recent_indexed.append(b)
    recent_indexed.sort(key=lambda x: x.get("raw_date", ""), reverse=True)
    top_indexed = recent_indexed[:8]
    
    # HTML Table for 4W volume
    w_rows = ""
    for w in weeks_4w:
        badge = " <span style='background:#4f46e5; color:#fff; font-size:10px; padding:1px 5px; border-radius:3px;'>Now</span>" if w["is_current"] else ""
        w_rows += f"""
        <tr>
          <td style='padding:8px 10px; border-bottom:1px solid #e2e8f0; font-size:13px;'>{w['label']}{badge}</td>
          <td style='padding:8px 10px; border-bottom:1px solid #e2e8f0; font-size:13px; font-weight:600; text-align:right;'>{w['count']} blogs</td>
        </tr>
        """
        
    # HTML Table for top recently indexed
    idx_rows = ""
    for b in top_indexed:
        title = b.get("title", "")[:50]
        link = b.get("link", "#")
        f_idx = b.get("first_indexed_date", "")
        imp = b.get("impressions", 0)
        clicks = b.get("clicks", 0)
        idx_rows += f"""
        <tr>
          <td style='padding:8px 10px; border-bottom:1px solid #e2e8f0; font-size:13px;'><a href='{link}' style='color:#2563eb; text-decoration:none; font-weight:500;'>{title}</a></td>
          <td style='padding:8px 10px; border-bottom:1px solid #e2e8f0; font-size:12px; color:#64748b; white-space:nowrap;'>{f_idx}</td>
          <td style='padding:8px 10px; border-bottom:1px solid #e2e8f0; font-size:13px; text-align:right; font-weight:600;'>{imp:,}</td>
          <td style='padding:8px 10px; border-bottom:1px solid #e2e8f0; font-size:13px; text-align:right; font-weight:600; color:#16a34a;'>{clicks:,}</td>
        </tr>
        """

    strat_rate = new_strat.get("indexing_rate", 0)
    overall_rate = overall.get("indexing_rate", 0)

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>Bluestone SEO Daily Performance Report</title>
    </head>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f1f5f9; margin: 0; padding: 24px; color: #1e293b;">
      <div style="max-width: 680px; margin: 0 auto; background: #ffffff; border-radius: 14px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.08); border: 1px solid #e2e8f0;">
        
        <!-- Header -->
        <div style="background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #312e81 100%); padding: 26px 32px; color: #ffffff;">
          <div style="font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; color: #a5b4fc; font-weight: 700; margin-bottom: 4px;">Automated Executive Report</div>
          <h1 style="margin: 0 0 6px 0; font-size: 24px; font-weight: 800; letter-spacing: -0.5px;">💎 Bluestone SEO Daily Performance</h1>
          <p style="margin: 0; font-size: 13px; color: #cbd5e1;">Live Data Sync: <strong>{generated_at}</strong></p>
        </div>

        <div style="padding: 24px 30px;">
          
          <!-- KPI Cards -->
          <div style="display: table; width: 100%; margin-bottom: 24px;">
            <div style="display: table-cell; width: 25%; padding-right: 8px;">
              <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px 12px; text-align: center;">
                <div style="font-size: 10px; text-transform: uppercase; color: #64748b; font-weight: 700;">Strategy Clicks</div>
                <div style="font-size: 22px; font-weight: 800; color: #4f46e5; margin: 4px 0 2px 0;">{new_strat.get('total_clicks', 0):,}</div>
                <div style="font-size: 11px; color: #16a34a; font-weight: 600;">{new_strat.get('avg_ctr', 0)}% CTR</div>
              </div>
            </div>
            <div style="display: table-cell; width: 25%; padding-right: 8px; padding-left: 4px;">
              <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px 12px; text-align: center;">
                <div style="font-size: 10px; text-transform: uppercase; color: #64748b; font-weight: 700;">Strategy Imp.</div>
                <div style="font-size: 22px; font-weight: 800; color: #0284c7; margin: 4px 0 2px 0;">{new_strat.get('total_impressions', 0):,}</div>
                <div style="font-size: 11px; color: #64748b;">Avg Pos: {new_strat.get('avg_position', 0)}</div>
              </div>
            </div>
            <div style="display: table-cell; width: 25%; padding-right: 8px; padding-left: 4px;">
              <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px 12px; text-align: center;">
                <div style="font-size: 10px; text-transform: uppercase; color: #64748b; font-weight: 700;">Strategy Indexing</div>
                <div style="font-size: 22px; font-weight: 800; color: #16a34a; margin: 4px 0 2px 0;">{strat_rate}%</div>
                <div style="font-size: 11px; color: #64748b; font-weight: 600;">{new_strat.get('indexed_count', 0)} / {new_strat.get('count', 0)}</div>
              </div>
            </div>
            <div style="display: table-cell; width: 25%; padding-left: 8px;">
              <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px 12px; text-align: center;">
                <div style="font-size: 10px; text-transform: uppercase; color: #64748b; font-weight: 700;">Total Active Posts</div>
                <div style="font-size: 22px; font-weight: 800; color: #334155; margin: 4px 0 2px 0;">{len(all_blogs):,}</div>
                <div style="font-size: 11px; color: #16a34a; font-weight: 600;">{overall_rate}% Overall</div>
              </div>
            </div>
          </div>

          <!-- Visual Progress Meter -->
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px 16px; margin-bottom: 24px;">
            <div style="display: table; width: 100%; margin-bottom: 6px;">
              <div style="display: table-cell; font-size: 12px; font-weight: 600; color: #334155;">Post-July 16 Strategy Indexing Progress</div>
              <div style="display: table-cell; text-align: right; font-size: 12px; font-weight: 700; color: #16a34a;">{new_strat.get('indexed_count', 0)} of {new_strat.get('count', 0)} ({strat_rate}%)</div>
            </div>
            <div style="background: #e2e8f0; border-radius: 6px; height: 10px; overflow: hidden;">
              <div style="background: linear-gradient(90deg, #10b981 0%, #059669 100%); height: 100%; width: {strat_rate}%; border-radius: 6px;"></div>
            </div>
          </div>

          <!-- GRAPH 1: Weekly Search Traffic Breakdown -->
          <div style="margin-bottom: 26px;">
            <div style="display: table; width: 100%; margin-bottom: 8px;">
              <div style="display: table-cell; font-size: 14px; font-weight: 700; color: #0f172a; text-transform: uppercase; letter-spacing: 0.5px;">📈 Weekly Traffic Breakdown (Last 10 Weeks)</div>
            </div>
            <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 10px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
              <img src="{traffic_chart_url}" alt="Weekly Traffic Breakdown (10W)" style="width: 100%; max-width: 620px; height: auto; border-radius: 6px; display: block; margin: 0 auto;" />
            </div>
          </div>

          <!-- GRAPH 2: Cumulative Indexing Trajectory -->
          <div style="margin-bottom: 26px;">
            <div style="display: table; width: 100%; margin-bottom: 8px;">
              <div style="display: table-cell; font-size: 14px; font-weight: 700; color: #0f172a; text-transform: uppercase; letter-spacing: 0.5px;">🎯 Strategy Indexing Growth Trajectory (700+ Milestone)</div>
            </div>
            <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 10px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
              <img src="{indexing_chart_url}" alt="Strategy Indexing Growth Trajectory" style="width: 100%; max-width: 620px; height: auto; border-radius: 6px; display: block; margin: 0 auto;" />
            </div>
          </div>

          <!-- Strategy Pivot Table -->
          <h2 style="font-size: 14px; font-weight: 700; margin: 0 0 10px 0; color: #0f172a; text-transform: uppercase; letter-spacing: 0.5px;">📊 Strategy Pivot Performance Breakdown</h2>
          <table style="width: 100%; border-collapse: collapse; margin-bottom: 24px; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden;">
            <thead>
              <tr style="background: #f8fafc;">
                <th style="padding: 8px 10px; text-align: left; font-size: 11px; text-transform: uppercase; color: #64748b; border-bottom: 1px solid #cbd5e1;">Cohort</th>
                <th style="padding: 8px 10px; text-align: right; font-size: 11px; text-transform: uppercase; color: #64748b; border-bottom: 1px solid #cbd5e1;">Published</th>
                <th style="padding: 8px 10px; text-align: right; font-size: 11px; text-transform: uppercase; color: #64748b; border-bottom: 1px solid #cbd5e1;">Indexed</th>
                <th style="padding: 8px 10px; text-align: right; font-size: 11px; text-transform: uppercase; color: #64748b; border-bottom: 1px solid #cbd5e1;">Index Rate</th>
                <th style="padding: 8px 10px; text-align: right; font-size: 11px; text-transform: uppercase; color: #64748b; border-bottom: 1px solid #cbd5e1;">Clicks (30d)</th>
                <th style="padding: 8px 10px; text-align: right; font-size: 11px; text-transform: uppercase; color: #64748b; border-bottom: 1px solid #cbd5e1;">Avg Rank</th>
              </tr>
            </thead>
            <tbody>
              <tr style="background: rgba(79, 70, 229, 0.04); font-weight: 600;">
                <td style="padding: 8px 10px; border-bottom: 1px solid #e2e8f0; font-size: 13px; color: #4338ca;">New Strategy (Post-July 16)</td>
                <td style="padding: 8px 10px; border-bottom: 1px solid #e2e8f0; font-size: 13px; text-align: right;">{new_strat.get('count', 0):,}</td>
                <td style="padding: 8px 10px; border-bottom: 1px solid #e2e8f0; font-size: 13px; text-align: right;">{new_strat.get('indexed_count', 0):,}</td>
                <td style="padding: 8px 10px; border-bottom: 1px solid #e2e8f0; font-size: 13px; text-align: right; color: #16a34a;">{strat_rate}%</td>
                <td style="padding: 8px 10px; border-bottom: 1px solid #e2e8f0; font-size: 13px; text-align: right; color: #4f46e5;">{new_strat.get('total_clicks', 0):,}</td>
                <td style="padding: 8px 10px; border-bottom: 1px solid #e2e8f0; font-size: 13px; text-align: right;">{new_strat.get('avg_position', 0)}</td>
              </tr>
              <tr>
                <td style="padding: 8px 10px; border-bottom: 1px solid #e2e8f0; font-size: 13px; color: #64748b;">Legacy Strategy (Pre-July 16)</td>
                <td style="padding: 8px 10px; border-bottom: 1px solid #e2e8f0; font-size: 13px; text-align: right;">{leg_strat.get('count', 0):,}</td>
                <td style="padding: 8px 10px; border-bottom: 1px solid #e2e8f0; font-size: 13px; text-align: right;">{leg_strat.get('indexed_count', 0):,}</td>
                <td style="padding: 8px 10px; border-bottom: 1px solid #e2e8f0; font-size: 13px; text-align: right;">{leg_strat.get('indexing_rate', 0)}%</td>
                <td style="padding: 8px 10px; border-bottom: 1px solid #e2e8f0; font-size: 13px; text-align: right;">{leg_strat.get('total_clicks', 0):,}</td>
                <td style="padding: 8px 10px; border-bottom: 1px solid #e2e8f0; font-size: 13px; text-align: right;">{leg_strat.get('avg_position', 0)}</td>
              </tr>
              <tr style="background: #f8fafc; font-weight: 700;">
                <td style="padding: 8px 10px; font-size: 13px;">Total Site Portfolio</td>
                <td style="padding: 8px 10px; font-size: 13px; text-align: right;">{overall.get('count', 0):,}</td>
                <td style="padding: 8px 10px; font-size: 13px; text-align: right;">{overall.get('indexed_count', 0):,}</td>
                <td style="padding: 8px 10px; font-size: 13px; text-align: right;">{overall_rate}%</td>
                <td style="padding: 8px 10px; font-size: 13px; text-align: right;">{overall.get('total_clicks', 0):,}</td>
                <td style="padding: 8px 10px; font-size: 13px; text-align: right;">{overall.get('avg_position', 0)}</td>
              </tr>
            </tbody>
          </table>

          <!-- 4-Week Publish Volume -->
          <h2 style="font-size: 14px; font-weight: 700; margin: 0 0 10px 0; color: #0f172a; text-transform: uppercase; letter-spacing: 0.5px;">📅 Publish Volume (Last 4 Weeks)</h2>
          <table style="width: 100%; border-collapse: collapse; margin-bottom: 24px; border: 1px solid #e2e8f0; border-radius: 8px;">
            <thead>
              <tr style="background: #f8fafc;">
                <th style="padding: 8px 10px; text-align: left; font-size: 11px; text-transform: uppercase; color: #64748b; border-bottom: 1px solid #cbd5e1;">Week Range</th>
                <th style="padding: 8px 10px; text-align: right; font-size: 11px; text-transform: uppercase; color: #64748b; border-bottom: 1px solid #cbd5e1;">Articles Published</th>
              </tr>
            </thead>
            <tbody>
              {w_rows}
            </tbody>
          </table>

          <!-- Recently Indexed Articles -->
          <h2 style="font-size: 14px; font-weight: 700; margin: 0 0 10px 0; color: #0f172a; text-transform: uppercase; letter-spacing: 0.5px;">🔍 Top Recently Indexed Strategy Articles</h2>
          <table style="width: 100%; border-collapse: collapse; margin-bottom: 24px; border: 1px solid #e2e8f0; border-radius: 8px;">
            <thead>
              <tr style="background: #f8fafc;">
                <th style="padding: 8px 10px; text-align: left; font-size: 11px; text-transform: uppercase; color: #64748b; border-bottom: 1px solid #cbd5e1;">Article Title</th>
                <th style="padding: 8px 10px; text-align: left; font-size: 11px; text-transform: uppercase; color: #64748b; border-bottom: 1px solid #cbd5e1;">First Indexed</th>
                <th style="padding: 8px 10px; text-align: right; font-size: 11px; text-transform: uppercase; color: #64748b; border-bottom: 1px solid #cbd5e1;">Impressions</th>
                <th style="padding: 8px 10px; text-align: right; font-size: 11px; text-transform: uppercase; color: #64748b; border-bottom: 1px solid #cbd5e1;">Clicks</th>
              </tr>
            </thead>
            <tbody>
              {idx_rows}
            </tbody>
          </table>

          <!-- Footer button -->
          <div style="text-align: center; padding: 18px 0 8px 0;">
            <a href="https://kingvikasindoria.github.io/bluestone-seo-handoff/" style="display: inline-block; background: #4f46e5; color: #ffffff; text-decoration: none; padding: 12px 28px; border-radius: 8px; font-size: 14px; font-weight: 700; box-shadow: 0 4px 10px rgba(79,70,229,0.35);">Open Live SEO Dashboard →</a>
          </div>

        </div>

        <!-- Footer -->
        <div style="background: #f8fafc; padding: 16px 30px; text-align: center; font-size: 12px; color: #64748b; border-top: 1px solid #e2e8f0;">
          Bluestone SEO Automation Pipeline • Generated automatically from Google Search Console & WordPress API
        </div>

      </div>
    </body>
    </html>
    """

    plain_content = f"""
Bluestone SEO Daily Performance Report
Generated: {generated_at}
Live Dashboard: https://kingvikasindoria.github.io/bluestone-seo-handoff/

Key Metrics:
- Post-July 16 Clicks (30d): {new_strat.get('total_clicks', 0):,}
- Post-July 16 Impressions (30d): {new_strat.get('total_impressions', 0):,}
- Post-July 16 Indexing Rate: {strat_rate}% ({new_strat.get('indexed_count', 0)}/{new_strat.get('count', 0)})
- Total WordPress Articles: {len(all_blogs):,}

Charts Included in HTML Version:
1. Weekly Search Traffic Breakdown (Last 10 Weeks)
2. Cumulative Indexing Growth Trajectory (Post-July 16)
"""

    subject = f"📊 Bluestone SEO Daily Report — {generated_at} ({new_strat.get('total_clicks', 0):,} Clicks | {strat_rate}% Indexed)"
    return subject, html_content, plain_content

def send_email():
    subject, html_content, plain_content = generate_report()
    
    email_to = os.environ.get("EMAIL_TO", "vikas.indoria@bluestone.com").strip()
    recipients = [e.strip() for e in email_to.split(",") if e.strip()]
    if not recipients:
        print("⚠️ No valid recipient email addresses specified.")
        return False

    resend_api_key = os.environ.get("RESEND_API_KEY", "").strip()
    if resend_api_key:
        print("📡 Sending daily report via Resend API...")
        try:
            res = requests.post(
                "https://api.resend.com/emails",
                headers={
                    "Authorization": f"Bearer {resend_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "from": "Bluestone SEO Bot <onboarding@resend.dev>",
                    "to": recipients,
                    "subject": subject,
                    "html": html_content,
                    "text": plain_content
                },
                timeout=15
            )
            if res.status_code in [200, 201]:
                print(f"✅ Daily SEO performance email successfully sent via Resend to: {', '.join(recipients)}")
                return True
            else:
                print(f"❌ Resend API returned status {res.status_code}: {res.text}")
        except Exception as e:
            print(f"❌ Failed to send via Resend API: {e}")

    # Fallback to standard SMTP
    smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", 465))
    smtp_user = os.environ.get("SMTP_USER", "").strip()
    smtp_pass = os.environ.get("SMTP_PASSWORD", "").strip()
    
    if smtp_user and smtp_pass:
        print("📡 Sending daily report via SMTP...")
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"Bluestone SEO Bot <{smtp_user}>"
        msg["To"] = ", ".join(recipients)
        
        part1 = MIMEText(plain_content, "plain", "utf-8")
        part2 = MIMEText(html_content, "html", "utf-8")
        msg.attach(part1)
        msg.attach(part2)
        
        try:
            if smtp_port == 465:
                with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=30) as server:
                    server.login(smtp_user, smtp_pass)
                    server.sendmail(smtp_user, recipients, msg.as_string())
            else:
                with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
                    server.starttls()
                    server.login(smtp_user, smtp_pass)
                    server.sendmail(smtp_user, recipients, msg.as_string())
            print(f"✅ Daily SEO performance email successfully sent via SMTP to: {', '.join(recipients)}")
            return True
        except Exception as e:
            print(f"❌ Failed to send email via SMTP ({smtp_host}:{smtp_port}): {e}")
            return False

    print("⚠️ No email delivery service configured (neither RESEND_API_KEY nor SMTP_USER/SMTP_PASSWORD provided).")
    print(f"\nSubject: {subject}\n")
    print(plain_content)
    return False

if __name__ == "__main__":
    send_email()
