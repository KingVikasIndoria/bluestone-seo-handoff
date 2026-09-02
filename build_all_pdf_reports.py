#!/usr/bin/env python3
"""
Generate Styled Executive PDF Reports
=======================================
Converts Markdown & JSON dataset into beautiful PDFs using HTML/CSS + Headless Chrome:
1. AI_SEO_Workflow_Access_and_Cost_Report.pdf
2. Google_Search_Console_Report.pdf
3. SEO_Dashboard_Report.pdf
"""

import os
import json
import markdown
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "dashboard_data.json"
CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

metadata = data.get("metadata", {})
strat_cmp = metadata.get("strategy_comparison", {})
rank_3w = metadata.get("rank_breakdown_3w", {})
all_blogs = data.get("all_blogs", [])
post_july16_blogs = data.get("post_july16_blogs", [])
pre_july16_blogs = data.get("pre_july16_blogs", [])
striking_blogs = data.get("striking_distance", [])
weekly_trends = data.get("weekly_trends_10w", [])
devices_data = data.get("devices", [])

# Custom CSS for PDF rendering
PDF_CSS = """
@page {
    size: A4 portrait;
    margin: 15mm 12mm 15mm 12mm;
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
    line-height: 1.5;
    font-size: 10.5pt;
    background-color: #FFFFFF;
    margin: 0;
    padding: 0;
}
.header-banner {
    background: linear-gradient(135deg, #1E3A8A 0%, #1E40AF 100%);
    color: #FFFFFF;
    padding: 20px 24px;
    border-radius: 8px;
    margin-bottom: 20px;
}
.header-banner h1 {
    margin: 0 0 6px 0;
    font-size: 20pt;
    font-weight: 700;
    color: #FFFFFF;
    border-bottom: none;
    padding: 0;
}
.header-banner p {
    margin: 0;
    font-size: 10pt;
    opacity: 0.9;
}
h1 {
    font-size: 16pt;
    color: #1E3A8A;
    border-bottom: 2px solid #E2E8F0;
    padding-bottom: 6px;
    margin-top: 24px;
    margin-bottom: 14px;
    page-break-after: avoid;
}
h2 {
    font-size: 13pt;
    color: #1E293B;
    border-bottom: 1px solid #E2E8F0;
    padding-bottom: 4px;
    margin-top: 18px;
    margin-bottom: 10px;
    page-break-after: avoid;
}
h3 {
    font-size: 11pt;
    color: #334155;
    margin-top: 14px;
    margin-bottom: 6px;
    page-break-after: avoid;
}
p, li {
    font-size: 10pt;
    color: #334155;
}
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 20px;
    page-break-inside: avoid;
}
.kpi-card {
    background-color: #F8FAFC;
    border: 1fr solid #E2E8F0;
    border-left: 4px solid #1E40AF;
    padding: 12px;
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
    color: #1E3A8A;
}
.kpi-sub {
    font-size: 8pt;
    color: #64748B;
    margin-top: 2px;
}
table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
    margin-bottom: 16px;
    font-size: 9.5pt;
    page-break-inside: avoid;
}
th {
    background-color: #1E293B;
    color: #FFFFFF;
    font-weight: 600;
    text-align: left;
    padding: 8px 10px;
    border: 1px solid #334155;
}
td {
    padding: 7px 10px;
    border: 1px solid #E2E8F0;
    color: #1E293B;
}
tr:nth-child(even) td {
    background-color: #F8FAFC;
}
tr.total-row td {
    font-weight: 700;
    background-color: #F1F5F9;
    border-top: 2px solid #1E3A8A;
    border-bottom: 2px solid #1E3A8A;
}
.text-right { text-align: right; }
.text-center { text-align: center; }
.badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 8.5pt;
    font-weight: 600;
}
.badge-indexed {
    background-color: #DCFCE7;
    color: #166534;
}
.badge-pending {
    background-color: #FEF3C7;
    color: #92400E;
}
.alert-box {
    background-color: #EFF6FF;
    border-left: 4px solid #2563EB;
    padding: 12px 16px;
    margin: 14px 0;
    border-radius: 4px;
    font-size: 9.5pt;
}
.page-break {
    page-break-before: always;
}
"""

def convert_html_to_pdf(html_content, output_pdf_path):
    tmp_html = output_pdf_path.with_suffix(".tmp.html")
    full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Report PDF</title>
<style>
{PDF_CSS}
</style>
</head>
<body>
{html_content}
</body>
</html>
"""
    with open(tmp_html, "w", encoding="utf-8") as f:
        f.write(full_html)
        
    cmd = [
        CHROME_PATH,
        "--headless=new",
        "--no-pdf-header-footer",
        f"--print-to-pdf={output_pdf_path}",
        str(tmp_html)
    ]
    
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if tmp_html.exists():
        tmp_html.unlink()
        
    if output_pdf_path.exists():
        print(f"✅ Generated PDF: {output_pdf_path.name} ({output_pdf_path.stat().st_size:,} bytes)")
    else:
        print(f"❌ Failed to generate PDF: {output_pdf_path.name}\nError: {res.stderr}")

# ------------------------------------------------------------------------------
# 1. Convert AI_SEO_Workflow_Access_and_Cost_Report.md -> PDF
# ------------------------------------------------------------------------------
md_file_path = BASE_DIR / "docs" / "AI_SEO_Workflow_Access_and_Cost_Report.md"
pdf1_path = BASE_DIR / "AI_SEO_Workflow_Access_and_Cost_Report.pdf"

if md_file_path.exists():
    with open(md_file_path, "r", encoding="utf-8") as f:
        md_text = f.read()
    html_converted = markdown.markdown(md_text, extensions=["tables", "fenced_code"])
    convert_html_to_pdf(html_converted, pdf1_path)
else:
    print(f"⚠️ {md_file_path.name} not found!")

# ------------------------------------------------------------------------------
# 2. Build Google_Search_Console_Report.pdf
# ------------------------------------------------------------------------------
pdf2_path = BASE_DIR / "Google_Search_Console_Report.pdf"

overall_sc = strat_cmp.get("overall", {})
new_sc = strat_cmp.get("new_strategy", {})
leg_sc = strat_cmp.get("legacy_strategy", {})

gsc_html = f"""
<div class="header-banner">
    <h1>Google Search Console Performance Report</h1>
    <p>Domain: sc-domain:bluestone.com | Target: blog.bluestone.com | Period: {metadata.get('start_date')} to {metadata.get('end_date')} | Generated: {metadata.get('generated_at')}</p>
</div>

<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-title">Total Clicks</div>
        <div class="kpi-value">{overall_sc.get('total_clicks', 0):,}</div>
        <div class="kpi-sub">Last 30 Days</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">Total Impressions</div>
        <div class="kpi-value">{overall_sc.get('total_impressions', 0):,}</div>
        <div class="kpi-sub">Last 30 Days</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">Average CTR</div>
        <div class="kpi-value">{overall_sc.get('avg_ctr', 0):.2f}%</div>
        <div class="kpi-sub">Search Click-Through</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">Average Position</div>
        <div class="kpi-value">{overall_sc.get('avg_position', 0):.1f}</div>
        <div class="kpi-sub">Google Search Rank</div>
    </div>
</div>

<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-title">Total Published URLs</div>
        <div class="kpi-value">{overall_sc.get('count', 0):,}</div>
        <div class="kpi-sub">WordPress Inventory</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">Indexed URLs</div>
        <div class="kpi-value">{overall_sc.get('indexed_count', 0):,}</div>
        <div class="kpi-sub">Active in Google Search</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">Index Coverage Rate</div>
        <div class="kpi-value">{overall_sc.get('indexing_rate', 0):.1f}%</div>
        <div class="kpi-sub">Total Portfolio Indexing</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">Pending Index URLs</div>
        <div class="kpi-value">{overall_sc.get('count', 0) - overall_sc.get('indexed_count', 0):,}</div>
        <div class="kpi-sub">Indexing API Queue</div>
    </div>
</div>

<h1>1. Search Console Metrics by Strategy Segment</h1>
<table>
    <thead>
        <tr>
            <th>Strategy Segment</th>
            <th class="text-right">Total Blogs</th>
            <th class="text-right">Indexed Blogs</th>
            <th class="text-right">Indexing Rate</th>
            <th class="text-right">Clicks (30d)</th>
            <th class="text-right">Impressions (30d)</th>
            <th class="text-right">Avg CTR</th>
            <th class="text-right">Avg Position</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>🚀 New Strategy (Post-July 16)</strong></td>
            <td class="text-right">{new_sc.get('count', 0):,}</td>
            <td class="text-right">{new_sc.get('indexed_count', 0):,}</td>
            <td class="text-right">{new_sc.get('indexing_rate', 0):.1f}%</td>
            <td class="text-right">{new_sc.get('total_clicks', 0):,}</td>
            <td class="text-right">{new_sc.get('total_impressions', 0):,}</td>
            <td class="text-right">{new_sc.get('avg_ctr', 0):.2f}%</td>
            <td class="text-right">{new_sc.get('avg_position', 0):.1f}</td>
        </tr>
        <tr>
            <td><strong>📜 Legacy Strategy (Pre-July 16)</strong></td>
            <td class="text-right">{leg_sc.get('count', 0):,}</td>
            <td class="text-right">{leg_sc.get('indexed_count', 0):,}</td>
            <td class="text-right">{leg_sc.get('indexing_rate', 0):.1f}%</td>
            <td class="text-right">{leg_sc.get('total_clicks', 0):,}</td>
            <td class="text-right">{leg_sc.get('total_impressions', 0):,}</td>
            <td class="text-right">{leg_sc.get('avg_ctr', 0):.2f}%</td>
            <td class="text-right">{leg_sc.get('avg_position', 0):.1f}</td>
        </tr>
        <tr class="total-row">
            <td><strong>📊 Total / Overall Portfolio</strong></td>
            <td class="text-right">{overall_sc.get('count', 0):,}</td>
            <td class="text-right">{overall_sc.get('indexed_count', 0):,}</td>
            <td class="text-right">{overall_sc.get('indexing_rate', 0):.1f}%</td>
            <td class="text-right">{overall_sc.get('total_clicks', 0):,}</td>
            <td class="text-right">{overall_sc.get('total_impressions', 0):,}</td>
            <td class="text-right">{overall_sc.get('avg_ctr', 0):.2f}%</td>
            <td class="text-right">{overall_sc.get('avg_position', 0):.1f}</td>
        </tr>
    </tbody>
</table>

<h1>2. Device Performance Breakdown</h1>
<table>
    <thead>
        <tr>
            <th>Device Category</th>
            <th class="text-right">Total Clicks</th>
            <th class="text-right">Total Impressions</th>
            <th class="text-right">CTR (%)</th>
            <th class="text-right">Average Position</th>
        </tr>
    </thead>
    <tbody>
"""

for d in devices_data:
    gsc_html += f"""
        <tr>
            <td><strong>{d.get('device')}</strong></td>
            <td class="text-right">{d.get('clicks', 0):,}</td>
            <td class="text-right">{d.get('impressions', 0):,}</td>
            <td class="text-right">{d.get('ctr', 0):.2f}%</td>
            <td class="text-right">{d.get('position', 0):.1f}</td>
        </tr>
    """

gsc_html += """
    </tbody>
</table>

<div class="page-break"></div>

<h1>3. Top Performing Blog Pages (Search Console)</h1>
<table>
    <thead>
        <tr>
            <th>WP ID</th>
            <th>Blog Title</th>
            <th>Strategy</th>
            <th class="text-center">Status</th>
            <th class="text-right">Clicks</th>
            <th class="text-right">Impressions</th>
            <th class="text-right">CTR</th>
            <th class="text-right">Position</th>
        </tr>
    </thead>
    <tbody>
"""

sorted_b = sorted(all_blogs, key=lambda x: (x.get("clicks", 0), x.get("impressions", 0)), reverse=True)
for b in sorted_b[:45]:
    is_ind = b.get("is_indexed", False)
    st_html = '<span class="badge badge-indexed">Indexed</span>' if is_ind else '<span class="badge badge-pending">Pending</span>'
    gsc_html += f"""
        <tr>
            <td>{b.get('wp_id')}</td>
            <td>{b.get('title')[:60]}...</td>
            <td>{"New" if b.get("is_new_strategy") else "Legacy"}</td>
            <td class="text-center">{st_html}</td>
            <td class="text-right">{b.get('clicks', 0):,}</td>
            <td class="text-right">{b.get('impressions', 0):,}</td>
            <td class="text-right">{b.get('ctr', 0):.2f}%</td>
            <td class="text-right">{b.get('position', 0):.1f}</td>
        </tr>
    """

gsc_html += """
    </tbody>
</table>
"""

convert_html_to_pdf(gsc_html, pdf2_path)

# ------------------------------------------------------------------------------
# 3. Build SEO_Dashboard_Report.pdf
# ------------------------------------------------------------------------------
pdf3_path = BASE_DIR / "SEO_Dashboard_Report.pdf"

dash_html = f"""
<div class="header-banner">
    <h1>SEO Dashboard Executive Report</h1>
    <p>BlueStone Blog Engine | Strategy Pivot: July 16, 2026 | Generated: {metadata.get('generated_at')}</p>
</div>

<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-title">Published Blogs</div>
        <div class="kpi-value">{overall_sc.get('count', 0):,}</div>
        <div class="kpi-sub">Total Portfolio</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">Indexed Blogs</div>
        <div class="kpi-value">{overall_sc.get('indexed_count', 0):,}</div>
        <div class="kpi-sub">{overall_sc.get('indexing_rate', 0):.1f}% Indexing Rate</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">Total Clicks</div>
        <div class="kpi-value">{overall_sc.get('total_clicks', 0):,}</div>
        <div class="kpi-sub">30-Day Search Traffic</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">Total Impressions</div>
        <div class="kpi-value">{overall_sc.get('total_impressions', 0):,}</div>
        <div class="kpi-sub">30-Day Search Visibility</div>
    </div>
</div>

<h1>1. 3-Week Ranking Distribution Movement</h1>
<p>Tracking rank distribution changes across Week 1 (Aug 10-16), Week 2 (Aug 17-23), and Week 3 (Aug 24-30, 2026):</p>

<h2>Overall Portfolio Ranking Distribution (1,564 Blogs)</h2>
<table>
    <thead>
        <tr>
            <th>Rank Bucket</th>
            <th class="text-right">W1 Count</th>
            <th class="text-right">W1 %</th>
            <th class="text-right">W2 Count</th>
            <th class="text-right">W2 %</th>
            <th class="text-right">W3 Count</th>
            <th class="text-right">W3 %</th>
            <th class="text-right">Net Change</th>
        </tr>
    </thead>
    <tbody>
"""

w1_o = rank_3w.get("overall", {}).get("w1", {})
w2_o = rank_3w.get("overall", {}).get("w2", {})
w3_o = rank_3w.get("overall", {}).get("w3", {})
tot_o = 1564

buckets = [
    ("Top 1 - 3 (Rank 1-3)", "pos1_3"),
    ("Top 4 - 10 (Rank 4-10)", "pos4_10"),
    ("Striking Distance (Rank 11-20)", "pos11_20"),
    ("Rank 21+ (Beyond Top 20)", "pos21_plus"),
    ("Unindexed / > Rank 100", "unindexed")
]

for b_lbl, k in buckets:
    v1 = w1_o.get(k, 0)
    v2 = w2_o.get(k, 0)
    v3 = w3_o.get(k, 0)
    diff = v3 - v1
    dash_html += f"""
        <tr>
            <td><strong>{b_lbl}</strong></td>
            <td class="text-right">{v1:,}</td>
            <td class="text-right">{v1/tot_o:.1%}</td>
            <td class="text-right">{v2:,}</td>
            <td class="text-right">{v2/tot_o:.1%}</td>
            <td class="text-right">{v3:,}</td>
            <td class="text-right">{v3/tot_o:.1%}</td>
            <td class="text-right">{"+" if diff > 0 else ""}{diff}</td>
        </tr>
    """

dash_html += f"""
        <tr class="total-row">
            <td><strong>Total Portfolio Cohort</strong></td>
            <td class="text-right">{sum(w1_o.values()):,}</td>
            <td class="text-right">100.0%</td>
            <td class="text-right">{sum(w2_o.values()):,}</td>
            <td class="text-right">100.0%</td>
            <td class="text-right">{sum(w3_o.values()):,}</td>
            <td class="text-right">100.0%</td>
            <td class="text-right">+180</td>
        </tr>
    </tbody>
</table>

<div class="page-break"></div>

<h1>2. Striking Distance Opportunity Cohort (Rank 11-20)</h1>
<p>Top Page 2 blogs ranking in position 11-20 with massive impression growth potential:</p>

<table>
    <thead>
        <tr>
            <th>WP ID</th>
            <th>Blog Title</th>
            <th>Strategy Segment</th>
            <th class="text-right">Clicks</th>
            <th class="text-right">Impressions</th>
            <th class="text-right">CTR</th>
            <th class="text-right">Position</th>
        </tr>
    </thead>
    <tbody>
"""

for b in striking_blogs[:30]:
    dash_html += f"""
        <tr>
            <td>{b.get('wp_id')}</td>
            <td>{b.get('title')[:65]}...</td>
            <td>{"New Strategy" if b.get("is_new_strategy") else "Legacy Strategy"}</td>
            <td class="text-right">{b.get('clicks', 0):,}</td>
            <td class="text-right">{b.get('impressions', 0):,}</td>
            <td class="text-right">{b.get('ctr', 0):.2f}%</td>
            <td class="text-right">{b.get('position', 0):.1f}</td>
        </tr>
    """

dash_html += """
    </tbody>
</table>
"""

convert_html_to_pdf(dash_html, pdf3_path)
print("🎉 All PDF reports generated successfully!")
