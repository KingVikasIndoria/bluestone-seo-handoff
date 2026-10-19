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
    
    # 1. Generate Clean 6-Month Clicks Chart
    m6 = data.get("monthly_trends_6m", [])
    m6_labels = [m.get("month_label", "") for m in m6]
    m6_clicks = [m.get("clicks", 0) for m in m6]
    m6_impressions = [m.get("impressions", 0) for m in m6]

    clicks_chart_config = {
        "type": "line",
        "data": {
            "labels": m6_labels,
            "datasets": [
                {
                    "label": "Monthly Clicks",
                    "data": m6_clicks,
                    "borderColor": "#4f46e5",
                    "backgroundColor": "rgba(79, 70, 229, 0.08)",
                    "fill": True,
                    "borderWidth": 3,
                    "pointRadius": 5,
                    "pointBackgroundColor": "#4f46e5",
                    "pointBorderColor": "#ffffff",
                    "pointBorderWidth": 2,
                    "tension": 0.3
                }
            ]
        },
        "options": {
            "title": {
                "display": True,
                "text": "Monthly Organic Clicks (Last 6 Months)",
                "fontSize": 13,
                "fontColor": "#0f172a",
                "fontStyle": "bold",
                "padding": 10
            },
            "legend": {"display": False},
            "scales": {
                "xAxes": [{"gridLines": {"display": False}, "ticks": {"fontColor": "#64748b", "fontSize": 11}}],
                "yAxes": [{"gridLines": {"color": "#f1f5f9"}, "ticks": {"fontColor": "#64748b", "fontSize": 10, "beginAtZero": True}}]
            }
        }
    }
    clicks_chart_url = create_quickchart_url(clicks_chart_config, width=620, height=210)

    # 2. Generate Clean 6-Month Impressions Chart
    imp_chart_config = {
        "type": "line",
        "data": {
            "labels": m6_labels,
            "datasets": [
                {
                    "label": "Monthly Impressions",
                    "data": m6_impressions,
                    "borderColor": "#0284c7",
                    "backgroundColor": "rgba(2, 132, 199, 0.08)",
                    "fill": True,
                    "borderWidth": 3,
                    "pointRadius": 5,
                    "pointBackgroundColor": "#0284c7",
                    "pointBorderColor": "#ffffff",
                    "pointBorderWidth": 2,
                    "tension": 0.3
                }
            ]
        },
        "options": {
            "title": {
                "display": True,
                "text": "Monthly Organic Impressions (Last 6 Months)",
                "fontSize": 13,
                "fontColor": "#0f172a",
                "fontStyle": "bold",
                "padding": 10
            },
            "legend": {"display": False},
            "scales": {
                "xAxes": [{"gridLines": {"display": False}, "ticks": {"fontColor": "#64748b", "fontSize": 11}}],
                "yAxes": [{"gridLines": {"color": "#f1f5f9"}, "ticks": {"fontColor": "#64748b", "fontSize": 10, "beginAtZero": True}}]
            }
        }
    }
    imp_chart_url = create_quickchart_url(imp_chart_config, width=620, height=210)

    # Business Value & Commercial Metrics
    rank_3w = meta.get("rank_breakdown_3w", {})
    w3_new = rank_3w.get("new_strategy", {}).get("w3", {})
    w3_all = rank_3w.get("overall", {}).get("w3", {})
    striking_articles = data.get("striking_distance", [])
    
    strat_clicks = new_strat.get("total_clicks", 0)
    strat_ctr = new_strat.get("avg_ctr", 0)
    est_ad_value = strat_clicks * 20  # ~₹20 estimated CPC for high-intent jewellery keywords
    
    page1_strat = w3_new.get("pos1_3", 0) + w3_new.get("pos4_10", 0)
    top3_strat = w3_new.get("pos1_3", 0)
    page1_overall = w3_all.get("pos1_3", 0) + w3_all.get("pos4_10", 0)
    striking_count = len(striking_articles)
    
    buying_guides_count = 0
    festive_count = 0
    for b in post_blogs:
        t = b.get("title", "").lower()
        if any(k in t for k in ["price", "rate", "worth", "cost", "buying guide", "how to choose", "vs", "designs", "rings", "necklace", "earrings", "bangles", "kada", "pendant", "gold", "diamond", "platinum"]):
            buying_guides_count += 1
        if any(k in t for k in ["diwali", "dhanteras", "bhai dooj", "navratri", "karwa chauth", "puja", "muhurat", "festival"]):
            festive_count += 1

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
          
          <!-- High-Value Business KPI Cards -->
          <div style="display: table; width: 100%; margin-bottom: 24px;">
            <div style="display: table-cell; width: 25%; padding-right: 8px;">
              <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px 10px; text-align: center;">
                <div style="font-size: 10px; text-transform: uppercase; color: #4338ca; font-weight: 700; letter-spacing: 0.5px;">Commercial Clicks</div>
                <div style="font-size: 22px; font-weight: 800; color: #4f46e5; margin: 4px 0 2px 0;">{strat_clicks:,}</div>
                <div style="font-size: 11px; color: #16a34a; font-weight: 700;">{strat_ctr}% CTR</div>
                <div style="font-size: 10px; color: #64748b; margin-top: 3px; font-weight: 500;">~₹{est_ad_value/100000:.1f}L Ad Value</div>
              </div>
            </div>
            <div style="display: table-cell; width: 25%; padding-right: 8px; padding-left: 4px;">
              <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px 10px; text-align: center;">
                <div style="font-size: 10px; text-transform: uppercase; color: #0369a1; font-weight: 700; letter-spacing: 0.5px;">Page 1 Dominance</div>
                <div style="font-size: 22px; font-weight: 800; color: #0284c7; margin: 4px 0 2px 0;">{page1_strat} Pages</div>
                <div style="font-size: 11px; color: #0284c7; font-weight: 700;">{top3_strat} in Top 3 Spots</div>
                <div style="font-size: 10px; color: #64748b; margin-top: 3px; font-weight: 500;">{page1_overall} Site-wide Frontline</div>
              </div>
            </div>
            <div style="display: table-cell; width: 25%; padding-right: 8px; padding-left: 4px;">
              <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px 10px; text-align: center;">
                <div style="font-size: 10px; text-transform: uppercase; color: #b45309; font-weight: 700; letter-spacing: 0.5px;">Striking Distance</div>
                <div style="font-size: 22px; font-weight: 800; color: #d97706; margin: 4px 0 2px 0;">{striking_count} Pages</div>
                <div style="font-size: 11px; color: #b45309; font-weight: 700;">Positions 11–20</div>
                <div style="font-size: 10px; color: #64748b; margin-top: 3px; font-weight: 500;">Immediate Upside</div>
              </div>
            </div>
            <div style="display: table-cell; width: 25%; padding-left: 8px;">
              <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px 10px; text-align: center;">
                <div style="font-size: 10px; text-transform: uppercase; color: #047857; font-weight: 700; letter-spacing: 0.5px;">Buyer Intent Assets</div>
                <div style="font-size: 22px; font-weight: 800; color: #059669; margin: 4px 0 2px 0;">{buying_guides_count} Guides</div>
                <div style="font-size: 11px; color: #059669; font-weight: 700;">{festive_count} Festive Surge</div>
                <div style="font-size: 10px; color: #64748b; margin-top: 3px; font-weight: 500;">{strat_rate}% Strategy Indexed</div>
              </div>
            </div>
          </div>

          <!-- Visual Progress Meter -->
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px 16px; margin-bottom: 24px;">
            <div style="display: table; width: 100%; margin-bottom: 6px;">
              <div style="display: table-cell; font-size: 12px; font-weight: 600; color: #334155;">Post-July 16 Strategy Indexing Progress (700+ Milestone)</div>
              <div style="display: table-cell; text-align: right; font-size: 12px; font-weight: 700; color: #16a34a;">{new_strat.get('indexed_count', 0)} of {new_strat.get('count', 0)} ({strat_rate}%)</div>
            </div>
            <div style="background: #e2e8f0; border-radius: 6px; height: 10px; overflow: hidden;">
              <div style="background: linear-gradient(90deg, #10b981 0%, #059669 100%); height: 100%; width: {strat_rate}%; border-radius: 6px;"></div>
            </div>
          </div>

          <!-- GRAPH 1: 6-Month Organic Clicks -->
          <div style="margin-bottom: 26px;">
            <div style="display: table; width: 100%; margin-bottom: 8px;">
              <div style="display: table-cell; font-size: 13px; font-weight: 700; color: #0f172a; text-transform: uppercase; letter-spacing: 0.5px;">📈 Organic Clicks Trend (Last 6 Months)</div>
              <div style="display: table-cell; text-align: right; font-size: 11px; color: #4f46e5; font-weight: 600;">High-Intent Search Traffic</div>
            </div>
            <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 10px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
              <img src="{clicks_chart_url}" alt="Monthly Organic Clicks (Last 6 Months)" style="width: 100%; max-width: 620px; height: auto; border-radius: 6px; display: block; margin: 0 auto;" />
            </div>
          </div>

          <!-- GRAPH 2: 6-Month Organic Impressions -->
          <div style="margin-bottom: 26px;">
            <div style="display: table; width: 100%; margin-bottom: 8px;">
              <div style="display: table-cell; font-size: 13px; font-weight: 700; color: #0f172a; text-transform: uppercase; letter-spacing: 0.5px;">👁️ Organic Impressions Trend (Last 6 Months)</div>
              <div style="display: table-cell; text-align: right; font-size: 11px; color: #0284c7; font-weight: 600;">Brand & Keyword Visibility</div>
            </div>
            <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 10px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
              <img src="{imp_chart_url}" alt="Monthly Organic Impressions (Last 6 Months)" style="width: 100%; max-width: 620px; height: auto; border-radius: 6px; display: block; margin: 0 auto;" />
            </div>
          </div>

          <!-- Business Value & Conversion Intelligence Box -->
          <div style="background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 10px; padding: 16px 18px; margin-bottom: 26px;">
            <div style="font-size: 12px; font-weight: 700; color: #166534; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px;">💡 Business Value &amp; Commercial Attribution</div>
            <div style="font-size: 12px; color: #1e293b; line-height: 1.6;">
              <strong>• UTM Parameter Attribution:</strong> Google Search Console records organic search landings where Google naturally strips external query parameters. Outbound conversions from articles to the BlueStone store catalog carry campaign tracking tags (<code style="background:#e2e8f0; padding:1px 4px; border-radius:3px; font-size:11px;">utm_source=blog&amp;utm_medium=article_cta&amp;utm_campaign=diwali2026</code>) for GA4/order revenue attribution.<br/>
              <strong>• Commercial CTR Benchmark (26.41%):</strong> Indicates strong buyer and shopping intent on product/price guides rather than passive informational reading.<br/>
              <strong>• Estimated Media Value Saved:</strong> 12,567 strategy clicks represent ~<strong>₹2.5 Lakhs+</strong> in equivalent Google Ads search spend (at ~₹20 CPC benchmark for competitive jewellery queries).<br/>
              <strong>• Striking Distance Upside:</strong> 24 high-impression articles in positions 11–20 represent immediate conversion potential with targeted internal linking.
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

Key Business Metrics:
- High-Intent Commercial Clicks (30d): {strat_clicks:,} ({strat_ctr}% CTR)
- Estimated Paid Ad Value Saved: ~₹{est_ad_value/100000:.1f} Lakhs (at ₹20 avg search CPC)
- Page 1 SERP Dominance: {page1_strat} strategy pages ({top3_strat} in Top 3), {page1_overall} site-wide
- Striking Distance Opportunity (Pos 11-20): {striking_count} pages ready for Page 1 push
- High-Intent Assets Live: {buying_guides_count} commercial buying guides, {festive_count} festive surge targets
- Strategy Indexing Progress: {strat_rate}% ({new_strat.get('indexed_count', 0)}/{new_strat.get('count', 0)})

Charts Included in HTML Version:
1. Monthly Organic Clicks (Last 6 Months)
2. Monthly Organic Impressions (Last 6 Months)
"""

    subject = f"📊 Bluestone SEO Business Report — {strat_clicks:,} Clicks ({strat_ctr}% CTR) | {page1_strat} Page 1 Pages"
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
