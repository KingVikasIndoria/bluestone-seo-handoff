#!/usr/bin/env python3
"""
Bluestone SEO Dashboard Daily Email Summary
===========================================
Reads dashboard_data.json and sends a daily HTML email report with:
  - Key Performance Indicators (Clicks, Impressions, CTR, Avg Rank)
  - Strategy Pivot Indexing Rate (New vs Legacy)
  - 4-Week Publish Volume Breakdown
  - Top Recently Indexed Articles

Environment variables:
  SMTP_HOST: SMTP server (default: smtp.gmail.com)
  SMTP_PORT: SMTP port (default: 465)
  SMTP_USER: Sender email username / address
  SMTP_PASSWORD: App password / SMTP password
  EMAIL_TO: Recipient email address(es), comma-separated
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
          <td style='padding:6px 10px; border-bottom:1px solid #e2e8f0; font-size:13px;'>{w['label']}{badge}</td>
          <td style='padding:6px 10px; border-bottom:1px solid #e2e8f0; font-size:13px; font-weight:600; text-align:right;'>{w['count']}</td>
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
          <td style='padding:6px 10px; border-bottom:1px solid #e2e8f0; font-size:13px;'><a href='{link}' style='color:#2563eb; text-decoration:none;'>{title}</a></td>
          <td style='padding:6px 10px; border-bottom:1px solid #e2e8f0; font-size:12px; color:#64748b; white-space:nowrap;'>{f_idx}</td>
          <td style='padding:6px 10px; border-bottom:1px solid #e2e8f0; font-size:13px; text-align:right; font-weight:600;'>{imp:,}</td>
          <td style='padding:6px 10px; border-bottom:1px solid #e2e8f0; font-size:13px; text-align:right; font-weight:600; color:#16a34a;'>{clicks:,}</td>
        </tr>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>Bluestone SEO Daily Performance Report</title>
    </head>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f8fafc; margin: 0; padding: 24px; color: #1e293b;">
      <div style="max-width: 680px; margin: 0 auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.06); border: 1px solid #e2e8f0;">
        
        <!-- Header -->
        <div style="background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%); padding: 24px 30px; color: #ffffff;">
          <h1 style="margin: 0 0 6px 0; font-size: 22px; font-weight: 700; letter-spacing: -0.5px;">💎 Bluestone SEO Daily Performance</h1>
          <p style="margin: 0; font-size: 13px; color: #cbd5e1;">Live Data Sync: <strong>{generated_at}</strong></p>
        </div>

        <div style="padding: 24px 30px;">
          
          <!-- KPI Cards -->
          <div style="display: table; width: 100%; margin-bottom: 24px;">
            <div style="display: table-cell; width: 25%; padding-right: 8px;">
              <div style="background: #f1f5f9; border-radius: 8px; padding: 12px 14px; text-align: center;">
                <div style="font-size: 11px; text-transform: uppercase; color: #64748b; font-weight: 600;">Post-July 16 Clicks</div>
                <div style="font-size: 20px; font-weight: 700; color: #4f46e5; margin-top: 4px;">{new_strat.get('total_clicks', 0):,}</div>
                <div style="font-size: 10px; color: #16a34a; font-weight: 600;">{new_strat.get('avg_ctr', 0)}% CTR</div>
              </div>
            </div>
            <div style="display: table-cell; width: 25%; padding-right: 8px; padding-left: 4px;">
              <div style="background: #f1f5f9; border-radius: 8px; padding: 12px 14px; text-align: center;">
                <div style="font-size: 11px; text-transform: uppercase; color: #64748b; font-weight: 600;">Post-July 16 Imp.</div>
                <div style="font-size: 20px; font-weight: 700; color: #0284c7; margin-top: 4px;">{new_strat.get('total_impressions', 0):,}</div>
                <div style="font-size: 10px; color: #64748b;">Avg Rank: {new_strat.get('avg_position', 0)}</div>
              </div>
            </div>
            <div style="display: table-cell; width: 25%; padding-right: 8px; padding-left: 4px;">
              <div style="background: #f1f5f9; border-radius: 8px; padding: 12px 14px; text-align: center;">
                <div style="font-size: 11px; text-transform: uppercase; color: #64748b; font-weight: 600;">Strategy Indexing</div>
                <div style="font-size: 20px; font-weight: 700; color: #16a34a; margin-top: 4px;">{new_strat.get('indexing_rate', 0)}%</div>
                <div style="font-size: 10px; color: #64748b;">{new_strat.get('indexed_count', 0)} / {new_strat.get('count', 0)}</div>
              </div>
            </div>
            <div style="display: table-cell; width: 25%; padding-left: 8px;">
              <div style="background: #f1f5f9; border-radius: 8px; padding: 12px 14px; text-align: center;">
                <div style="font-size: 11px; text-transform: uppercase; color: #64748b; font-weight: 600;">Total WP Posts</div>
                <div style="font-size: 20px; font-weight: 700; color: #334155; margin-top: 4px;">{len(all_blogs):,}</div>
                <div style="font-size: 10px; color: #64748b;">Active Content</div>
              </div>
            </div>
          </div>

          <!-- Strategy Pivot Table -->
          <h2 style="font-size: 15px; font-weight: 700; margin: 0 0 10px 0; color: #0f172a; text-transform: uppercase; letter-spacing: 0.5px;">📊 Strategy Pivot Breakdown</h2>
          <table style="width: 100%; border-collapse: collapse; margin-bottom: 24px; border: 1px solid #e2e8f0; border-radius: 6px; overflow: hidden;">
            <thead>
              <tr style="background: #f8fafc;">
                <th style="padding: 8px 10px; text-align: left; font-size: 12px; color: #64748b; border-bottom: 1px solid #cbd5e1;">Cohort</th>
                <th style="padding: 8px 10px; text-align: right; font-size: 12px; color: #64748b; border-bottom: 1px solid #cbd5e1;">Published</th>
                <th style="padding: 8px 10px; text-align: right; font-size: 12px; color: #64748b; border-bottom: 1px solid #cbd5e1;">Indexed</th>
                <th style="padding: 8px 10px; text-align: right; font-size: 12px; color: #64748b; border-bottom: 1px solid #cbd5e1;">Index Rate</th>
                <th style="padding: 8px 10px; text-align: right; font-size: 12px; color: #64748b; border-bottom: 1px solid #cbd5e1;">Clicks (30d)</th>
                <th style="padding: 8px 10px; text-align: right; font-size: 12px; color: #64748b; border-bottom: 1px solid #cbd5e1;">Avg Rank</th>
              </tr>
            </thead>
            <tbody>
              <tr style="background: rgba(79, 70, 229, 0.04); font-weight: 600;">
                <td style="padding: 8px 10px; border-bottom: 1px solid #e2e8f0; font-size: 13px; color: #4338ca;">New Strategy (Post-July 16)</td>
                <td style="padding: 8px 10px; border-bottom: 1px solid #e2e8f0; font-size: 13px; text-align: right;">{new_strat.get('count', 0):,}</td>
                <td style="padding: 8px 10px; border-bottom: 1px solid #e2e8f0; font-size: 13px; text-align: right;">{new_strat.get('indexed_count', 0):,}</td>
                <td style="padding: 8px 10px; border-bottom: 1px solid #e2e8f0; font-size: 13px; text-align: right; color: #16a34a;">{new_strat.get('indexing_rate', 0)}%</td>
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
                <td style="padding: 8px 10px; font-size: 13px; text-align: right;">{overall.get('indexing_rate', 0)}%</td>
                <td style="padding: 8px 10px; font-size: 13px; text-align: right;">{overall.get('total_clicks', 0):,}</td>
                <td style="padding: 8px 10px; font-size: 13px; text-align: right;">{overall.get('avg_position', 0)}</td>
              </tr>
            </tbody>
          </table>

          <!-- 4-Week Publish Volume -->
          <h2 style="font-size: 15px; font-weight: 700; margin: 0 0 10px 0; color: #0f172a; text-transform: uppercase; letter-spacing: 0.5px;">📅 Publish Volume (Last 4 Weeks)</h2>
          <table style="width: 100%; border-collapse: collapse; margin-bottom: 24px; border: 1px solid #e2e8f0; border-radius: 6px;">
            <thead>
              <tr style="background: #f8fafc;">
                <th style="padding: 8px 10px; text-align: left; font-size: 12px; color: #64748b; border-bottom: 1px solid #cbd5e1;">Week</th>
                <th style="padding: 8px 10px; text-align: right; font-size: 12px; color: #64748b; border-bottom: 1px solid #cbd5e1;">Articles Published</th>
              </tr>
            </thead>
            <tbody>
              {w_rows}
            </tbody>
          </table>

          <!-- Recently Indexed Articles -->
          <h2 style="font-size: 15px; font-weight: 700; margin: 0 0 10px 0; color: #0f172a; text-transform: uppercase; letter-spacing: 0.5px;">🔍 Top Recently Indexed Strategy Articles</h2>
          <table style="width: 100%; border-collapse: collapse; margin-bottom: 24px; border: 1px solid #e2e8f0; border-radius: 6px;">
            <thead>
              <tr style="background: #f8fafc;">
                <th style="padding: 8px 10px; text-align: left; font-size: 12px; color: #64748b; border-bottom: 1px solid #cbd5e1;">Article Title</th>
                <th style="padding: 8px 10px; text-align: left; font-size: 12px; color: #64748b; border-bottom: 1px solid #cbd5e1;">First Indexed</th>
                <th style="padding: 8px 10px; text-align: right; font-size: 12px; color: #64748b; border-bottom: 1px solid #cbd5e1;">Impressions</th>
                <th style="padding: 8px 10px; text-align: right; font-size: 12px; color: #64748b; border-bottom: 1px solid #cbd5e1;">Clicks</th>
              </tr>
            </thead>
            <tbody>
              {idx_rows}
            </tbody>
          </table>

          <!-- Footer button -->
          <div style="text-align: center; padding: 16px 0 8px 0;">
            <a href="https://kingvikasindoria.github.io/bluestone-seo-handoff/" style="display: inline-block; background: #4f46e5; color: #ffffff; text-decoration: none; padding: 12px 28px; border-radius: 6px; font-size: 14px; font-weight: 600; box-shadow: 0 2px 4px rgba(79,70,229,0.3);">Open Live SEO Dashboard →</a>
          </div>

        </div>

        <!-- Footer -->
        <div style="background: #f1f5f9; padding: 16px 30px; text-align: center; font-size: 12px; color: #64748b; border-top: 1px solid #e2e8f0;">
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
- Post-July 16 Indexing Rate: {new_strat.get('indexing_rate', 0)}% ({new_strat.get('indexed_count', 0)}/{new_strat.get('count', 0)})
- Total WordPress Articles: {len(all_blogs):,}

Strategy Breakdown:
- New Strategy (Post-July 16): {new_strat.get('count', 0)} published, {new_strat.get('indexed_count', 0)} indexed ({new_strat.get('indexing_rate', 0)}%), {new_strat.get('total_clicks', 0):,} clicks
- Legacy Strategy (Pre-July 16): {leg_strat.get('count', 0)} published, {leg_strat.get('indexed_count', 0)} indexed ({leg_strat.get('indexing_rate', 0)}%), {leg_strat.get('total_clicks', 0):,} clicks
- Overall Portfolio: {overall.get('count', 0)} published, {overall.get('indexed_count', 0)} indexed ({overall.get('indexing_rate', 0)}%), {overall.get('total_clicks', 0):,} clicks
"""

    subject = f"📊 Bluestone SEO Daily Report — {generated_at} ({new_strat.get('total_clicks', 0):,} Clicks | {new_strat.get('indexing_rate', 0)}% Indexed)"
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
