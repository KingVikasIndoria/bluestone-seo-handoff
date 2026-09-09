#!/usr/bin/env python3
"""
Generate WebEngage Journeys Executive PDF Report
=================================================
Fetches all active WebEngage journeys via API and builds a beautiful executive PDF report.
Filters out journeys with less than 100 users entered.
Adds a 5-6 word purpose/description column for each journey.
Headline: Journeys Reports
Output: Journeys_Report.pdf
"""

import json
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).parent
CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUTPUT_PDF = BASE_DIR / "Journeys_Report.pdf"

# API Request configuration
API_URL = "https://dashboard.webengage.com/api/v1/accounts/~10a5cb63c/journeys?noView=true&pageNo=1&pageSize=100&status=ACTIVE&q="
HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://dashboard.webengage.com/accounts/~10a5cb63c/journeys/campaign-list/all",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36",
    "Cookie": "_lfa=LF1.1.86fc636b932994b9.1778220821313; hubspotutk=ce07db0f90140f4008511515cbc874bd; ajs_anonymous_id=91ebbd89-e655-4bbd-9bf1-e2cbe6e99345; _fuid=ZjFiMzkyZTctMTU0ZC00ZGY0LTliMzQtNjBmODJjMGY5MGQ5; WebKlipperAuth=QJy1pmU0na64gYQhNbCN; _we_us=1786960120194; _gid=GA1.2.621184650.1788759488; _uetvid=0f6e2fe04aa511f1bb8cd18686fd48cf; _clck=luv1ot%5E2%5Eg99%5E0%5E2319; __hstc=207184332.ce07db0f90140f4008511515cbc874bd.1778220822380.1787549952178.1788759489354.14; _gcl_au=1.1.1551250581.1786004137.1590782645.1788759491.1788759492.1536530275.1788759491.1788759492; WeAuth=0; _we_a_ssid=aaarb3FUXYFtzdDXl-HbA; _ga=GA1.1.180169304.1778220821; _ga_3NGD3E18DP=GS2.1.s1788945566$o244$g0$t1788946299$j60$l0$h0; AWSALB=KgfLwKZ+Sot3DyJ5HHylsBS4i82wT8y2pJRPiPPEzxBQkN73sU7wTWvfG1a2/Dq6Or3tYYNrViuSoA2BzQU44mUeAwggFtJsPG8z9qosdHs2pfDhRKY9eMC2BT7GUFnLL6gjAY8v+Fp27tMBVDkHooreCEYH6NVbU1/+c2k6ShUhc9pH2quOMmXiYbVBZS/Xp1/S4uFkMrcpX2bHg7F5pLm2NcUK5onIXgWvCVl1CY6DwUqBuITicFMXZjTwW/A=; AWSALBCORS=KgfLwKZ+Sot3DyJ5HHylsBS4i82wT8y2pJRPiPPEzxBQkN73sU7wTWvfG1a2/Dq6Or3tYYNrViuSoA2BzQU44mUeAwggFtJsPG8z9qosdHs2pfDhRKY9eMC2BT7GUFnLL6gjAY8v+Fp27tMBVDkHooreCEYH6NVbU1/+c2k6ShUhc9pH2quOMmXiYbVBZS/Xp1/S4uFkMrcpX2bHg7F5pLm2NcUK5onIXgWvCVl1CY6DwUqBuITicFMXZjTwW/A="
}


def fetch_journeys():
    req = urllib.request.Request(API_URL, headers=HEADERS)
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
    return res.get("response", {}).get("data", {})


def get_journey_explanation(name):
    """Infers a concise 5-6 word explanation of the journey's purpose based on its title."""
    name_lower = name.lower()
    
    # Specific category guides (Post-purchase)
    if "bangles guides" in name_lower:
        return "Post-purchase guide for bangles buyers"
    if "pendants guides" in name_lower:
        return "Post-purchase guide for pendants buyers"
    if "earrings guides" in name_lower:
        return "Post-purchase guide for earrings buyers"
    if "ring guides" in name_lower:
        return "Post-purchase guide for rings buyers"
    if "mangalsutras and chains" in name_lower:
        return "Post-purchase mangalsutras & chains guide"
    if "pendants and chains" in name_lower:
        return "Post-purchase pendants & chains guide"
    if "steelbraceletcleaning" in name_lower:
        return "Post-purchase steel bracelet care guide"
    if "cleaningjewelleryguide" in name_lower:
        return "Post-purchase jewellery cleaning care guide"
    
    # GMS (Gold Savings Scheme)
    if "gms_instalment_reminder" in name_lower:
        return "GMS scheme monthly instalment payment reminder"
    if "gms_redemption_calling" in name_lower or "gmspostredemption" in name_lower:
        return "GMS plan maturity redemption calling task"
    if "gms_post_order_placed" in name_lower:
        return "GMS post-order purchase onboarding journey"
    if "gms_instalment_date_increase" in name_lower or "gms_instalment_date_populate" in name_lower:
        return "GMS instalment date update helper workflow"
        
    # Cart & Drop-off Re-engagement
    if "cart and wishlist" in name_lower and "posonly" in name_lower:
        return "Cart & wishlist drop-off re-engagement (POS)"
    if "cart and wishlist" in name_lower:
        return "Cart & wishlist drop-off re-engagement journey"
    if "pdp viewed" in name_lower:
        return "PDP product view drop-off outbound call"

    # Celebrations & Greetings
    if "spousebday calling" in name_lower:
        return "Spouse birthday upcoming wish calling task"
    if "birthday calling" in name_lower:
        return "Customer birthday upcoming wish calling task"
    if "anniversary calling" in name_lower:
        return "Customer anniversary wish calling task trigger"
    if "spouse birthday greetings" in name_lower or "spbirthday greetings" in name_lower:
        return "Automated spouse birthday greetings campaign"
    if "birthday greetings helper" in name_lower:
        return "Customer birthday workflow automated helper"
    if "birthday greetings" in name_lower:
        return "Automated customer birthday greetings campaign"
    if "anniversary greetings helper" in name_lower:
        return "Customer anniversary workflow automated helper"
    if "anniversary greetings" in name_lower:
        return "Automated customer anniversary greetings campaign"
        
    # Onboarding & Retention
    if "welcome series" in name_lower:
        return "New user welcome onboarding email series"
    if "voucher_calling" in name_lower:
        return "Voucher expiration re-engagement calling task"
    if "truecrmexperiencecall" in name_lower:
        return "Post-purchase customer feedback CRM call"
    if "order_placed_120d" in name_lower:
        return "Post-order 120-day customer engagement journey"
    if "matchingset" in name_lower:
        return "Cross-sell matching jewellery set recommendation"
    if "profile deactivation" in name_lower:
        return "Customer profile deactivation confirmation workflow"
        
    return "Automated lifecycle customer engagement workflow"


def generate_pdf():
    raw_data = fetch_journeys()
    all_contents = raw_data.get("contents", [])
    
    # Filter journeys: keep only those sent to >= 100 people
    contents = [j for j in all_contents if j.get("stats", {}).get("entered", 0) >= 100]
    total_count = len(contents)
    
    total_entered = sum(j.get("stats", {}).get("entered", 0) for j in contents)
    total_exited = sum(j.get("stats", {}).get("exited", 0) for j in contents)
    gen_time = datetime.now(timezone.utc).strftime("%B %d, %Y at %H:%M UTC")

    # CSS for Executive PDF
    pdf_css = """
    @page {
        size: A4 landscape;
        margin: 8mm 8mm 8mm 8mm;
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
        line-height: 1.3;
        font-size: 8pt;
        background-color: #FFFFFF;
        margin: 0;
        padding: 0;
    }
    .header-banner {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%);
        color: #FFFFFF;
        padding: 12px 16px;
        border-radius: 6px;
        margin-bottom: 10px;
    }
    .header-banner h1 {
        margin: 0 0 2px 0;
        font-size: 18pt;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: -0.5px;
    }
    .header-banner p {
        margin: 0;
        font-size: 8.5pt;
        opacity: 0.9;
    }
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 8px;
        margin-bottom: 10px;
    }
    .kpi-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #1E40AF;
        padding: 6px 10px;
        border-radius: 5px;
        text-align: center;
    }
    .kpi-title {
        font-size: 7pt;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        margin-bottom: 1px;
    }
    .kpi-value {
        font-size: 14pt;
        font-weight: 800;
        color: #1E3A8A;
    }
    .kpi-sub {
        font-size: 7pt;
        color: #64748B;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 6px;
        margin-bottom: 10px;
        font-size: 7.5pt;
    }
    th {
        background-color: #1E293B;
        color: #FFFFFF;
        font-weight: 600;
        text-align: left;
        padding: 5px 6px;
        border: 1px solid #334155;
    }
    td {
        padding: 4px 6px;
        border: 1px solid #E2E8F0;
        color: #1E293B;
        vertical-align: middle;
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
    .badge-active {
        background-color: #DCFCE7;
        color: #166534;
        padding: 1px 4px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 6.5pt;
    }
    .badge-tag {
        background-color: #EFF6FF;
        color: #1E40AF;
        padding: 1px 4px;
        border-radius: 3px;
        font-size: 6.5pt;
        margin-right: 2px;
        display: inline-block;
    }
    .code-id {
        font-family: monospace;
        font-weight: 600;
        color: #0F172A;
    }
    .explanation-text {
        font-style: italic;
        color: #334155;
        font-weight: 500;
    }
    """

    # Build Table Rows
    table_rows = ""
    for idx, j in enumerate(contents, 1):
        stats = j.get("stats", {})
        entered = stats.get("entered", 0)
        exited = stats.get("exited", 0)
        
        explanation = get_journey_explanation(j.get("name", ""))
        
        tags_list = j.get("tags", [])
        tags_html = "".join([f'<span class="badge-tag">{t}</span>' for t in tags_list]) if tags_list else '<span style="color:#94A3B8;">—</span>'
        
        pub_date = j.get("lastPublishedOn", "")
        if pub_date:
            try:
                pub_fmt = datetime.fromisoformat(pub_date.replace("Z", "+00:00")).strftime("%Y-%m-%d")
            except Exception:
                pub_fmt = pub_date[:10]
        else:
            pub_fmt = "—"

        table_rows += f"""
        <tr>
            <td class="text-center">{idx}</td>
            <td class="code-id">{j.get('journeyEId', '')}</td>
            <td><strong>{j.get('name', '')}</strong></td>
            <td class="explanation-text">{explanation}</td>
            <td>{j.get('createdByUser', '')}</td>
            <td>{j.get('lastModifiedByUser', '')}</td>
            <td>{tags_html}</td>
            <td class="text-right"><strong>{entered:,}</strong></td>
            <td class="text-right">{exited:,}</td>
            <td>{pub_fmt}</td>
            <td class="text-center"><span class="badge-active">{j.get('status', 'ACTIVE')}</span></td>
        </tr>
        """

    full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Journeys Reports</title>
<style>
{pdf_css}
</style>
</head>
<body>

<div class="header-banner">
    <h1>Journeys Reports</h1>
    <p>WebEngage Active Journeys & Lifecycle Automation Audit (Filtered: ≥100 Users Triggered) | Account: ~10a5cb63c | Generated: {gen_time}</p>
</div>

<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-title">Active Journeys (≥100 Users)</div>
        <div class="kpi-value">{total_count}</div>
        <div class="kpi-sub">Filtered Workflows</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">Total Users Entered</div>
        <div class="kpi-value">{total_entered:,}</div>
        <div class="kpi-sub">Total Trigger Volume</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">Total Users Exited</div>
        <div class="kpi-value">{total_exited:,}</div>
        <div class="kpi-sub">Completed Workflows</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-title">Workflow Completion Rate</div>
        <div class="kpi-value">{(total_exited/total_entered*100 if total_entered else 0):.1f}%</div>
        <div class="kpi-sub">Overall Exit Ratio</div>
    </div>
</div>

<table>
    <thead>
        <tr>
            <th class="text-center">#</th>
            <th>Journey ID</th>
            <th>Journey Name</th>
            <th>Journey Purpose / Description (5–6 words)</th>
            <th>Created By</th>
            <th>Modified By</th>
            <th>Tags</th>
            <th class="text-right">Users Entered</th>
            <th class="text-right">Users Exited</th>
            <th>Last Published</th>
            <th class="text-center">Status</th>
        </tr>
    </thead>
    <tbody>
        {table_rows}
        <tr class="total-row">
            <td class="text-center">—</td>
            <td colspan="6"><strong>Total Active Journeys Summary ({total_count} Workflows with ≥100 Users)</strong></td>
            <td class="text-right"><strong>{total_entered:,}</strong></td>
            <td class="text-right"><strong>{total_exited:,}</strong></td>
            <td>—</td>
            <td class="text-center"><span class="badge-active">ACTIVE</span></td>
        </tr>
    </tbody>
</table>

</body>
</html>
"""

    tmp_html = BASE_DIR / "Journeys_Report.tmp.html"
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
