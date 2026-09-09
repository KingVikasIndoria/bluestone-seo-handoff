#!/usr/bin/env python3
"""
Generate Trustpilot Service Reviews Executive PDF Report
==========================================================
Fetches Trustpilot service reviews via API and builds a beautiful executive PDF report.
Headline: Trustpilot Service Reviews Report
Output: Trustpilot_Service_Reviews_Report.pdf
"""

import json
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).parent
CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUTPUT_PDF = BASE_DIR / "Trustpilot_Service_Reviews_Report.pdf"

# API Request configuration
API_URL = "https://api.trustpilot.com/v1/private/business-units/6848335357d508c38201008f/servicereviews/search?limit=50&offset=0"
HEADERS = {
    "accept": "application/json, text/plain, */*",
    "authorization": "Bearer tpa-5bbbd0cc4f14f41eceaaf096a79d",
    "origin": "https://businessapp.b2b.trustpilot.com",
    "referer": "https://businessapp.b2b.trustpilot.com/",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36",
}


def fetch_reviews():
    req = urllib.request.Request(API_URL, headers=HEADERS)
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
    return res


def generate_pdf():
    data = fetch_reviews()
    reviews = data.get("results", [])
    total_count = data.get("count", len(reviews))
    
    avg_rating = sum(r.get("stars", 0) for r in reviews) / len(reviews) if reviews else 0
    five_star_count = sum(1 for r in reviews if r.get("stars") == 5)
    critical_count = sum(1 for r in reviews if r.get("stars") <= 2)
    
    gen_time = datetime.now(timezone.utc).strftime("%B %d, %Y at %H:%M UTC")

    # CSS for Executive PDF
    pdf_css = """
    @page {
        size: A4 portrait;
        margin: 12mm 12mm 12mm 12mm;
    }
    @media print {
        body {
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }
    }
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #0F172A;
        line-height: 1.45;
        font-size: 9.5pt;
        background-color: #FFFFFF;
        margin: 0;
        padding: 0;
    }
    .header-banner {
        background: linear-gradient(135deg, #00B67A 0%, #005138 100%);
        color: #FFFFFF;
        padding: 16px 20px;
        border-radius: 6px;
        margin-bottom: 16px;
    }
    .header-banner h1 {
        margin: 0 0 4px 0;
        font-size: 20pt;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: -0.5px;
    }
    .header-banner p {
        margin: 0;
        font-size: 9.5pt;
        opacity: 0.95;
    }
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        margin-bottom: 16px;
    }
    .kpi-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #00B67A;
        padding: 10px 14px;
        border-radius: 6px;
        text-align: center;
    }
    .kpi-title {
        font-size: 8pt;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .kpi-value {
        font-size: 16pt;
        font-weight: 800;
        color: #0F172A;
    }
    .kpi-sub {
        font-size: 8pt;
        color: #64748B;
        margin-top: 2px;
    }
    .section-title {
        font-size: 13pt;
        font-weight: 700;
        color: #0F172A;
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 4px;
        margin-top: 18px;
        margin-bottom: 12px;
    }
    .review-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        padding: 12px 14px;
        margin-bottom: 12px;
        page-break-inside: avoid;
    }
    .review-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
        border-bottom: 1px solid #F1F5F9;
        padding-bottom: 6px;
    }
    .review-author {
        font-weight: 700;
        font-size: 10pt;
        color: #0F172A;
    }
    .review-meta {
        font-size: 8.5pt;
        color: #64748B;
    }
    .stars-5 { color: #00B67A; font-weight: 800; font-size: 10pt; }
    .stars-1, .stars-2 { color: #DC2626; font-weight: 800; font-size: 10pt; }
    .review-title {
        font-weight: 700;
        font-size: 10pt;
        color: #1E293B;
        margin-bottom: 4px;
    }
    .review-body {
        font-size: 9pt;
        color: #334155;
        white-space: pre-line;
    }
    .badge-source {
        background-color: #F1F5F9;
        color: #475569;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 7.5pt;
        font-weight: 600;
    }
    """

    # Build Review Cards HTML
    review_cards_html = ""
    for idx, r in enumerate(reviews, 1):
        stars = r.get("stars", 0)
        stars_class = f"stars-{stars}" if stars in [1, 2, 5] else "stars-5"
        stars_display = "★" * stars + "☆" * (5 - stars)
        
        consumer = r.get("consumer", {})
        name = consumer.get("displayName", "Anonymous")
        country = consumer.get("country", "")
        country_str = f" ({country})" if country else ""
        
        date_str = r.get("createdAt", "")[:10]
        title = r.get("title", "").strip()
        text = r.get("text", "").strip()
        source = r.get("source", "Organic")

        review_cards_html += f"""
        <div class="review-card">
            <div class="review-header">
                <div>
                    <span class="{stars_class}">{stars_display} ({stars}/5)</span>
                    <span class="review-author" style="margin-left: 8px;">{name}{country_str}</span>
                </div>
                <div class="review-meta">
                    <span class="badge-source">{source}</span> &nbsp;|&nbsp; {date_str}
                </div>
            </div>
            <div class="review-title">{title}</div>
            <div class="review-body">{text}</div>
        </div>
        """

    full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Trustpilot Service Reviews Report</title>
<style>
{pdf_css}
</style>
</head>
<body>

<div class="header-banner">
    <h1>Trustpilot Service Reviews Report</h1>
    <p>BlueStone Jewellery & Lifestyle Ltd. | Business Unit ID: 6848335357d508c38201008f | Generated: {gen_time}</p>
</div>

<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-title">Total Reviews</div>
        <div class="kpi-value">{total_count:,}</div>
        <div class="kpi-sub">Service Reviews</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">Average Rating</div>
        <div class="kpi-value">{avg_rating:.2f} / 5.0</div>
        <div class="kpi-sub">TrustScore Metric</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">5-Star Positive</div>
        <div class="kpi-value">{five_star_count}</div>
        <div class="kpi-sub">{(five_star_count/total_count*100 if total_count else 0):.1f}% Positive</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">1–2 Star Critical</div>
        <div class="kpi-value">{critical_count}</div>
        <div class="kpi-sub">{(critical_count/total_count*100 if total_count else 0):.1f}% Escalated</div>
    </div>
</div>

<div class="section-title">Customer Reviews Feedback Log ({total_count} Reviews)</div>

{review_cards_html}

</body>
</html>
"""

    tmp_html = BASE_DIR / "Trustpilot_Service_Reviews_Report.tmp.html"
    with open(tmp_html, "w", encoding="utf-8") as f:
        f.write(full_html)

    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--no-pdf-header-footer",
        f"--print-to-pdf={OUTPUT_PDF}",
        str(tmp_html),
    ]

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if tmp_html.exists():
        tmp_html.unlink()

    if OUTPUT_PDF.exists():
        print(f"✅ Generated PDF: {OUTPUT_PDF.name} ({OUTPUT_PDF.stat().st_size:,} bytes)")
    else:
        print(f"❌ Failed to generate PDF: {OUTPUT_PDF.name}\nError: {res.stderr}")


if __name__ == "__main__":
    generate_pdf()
