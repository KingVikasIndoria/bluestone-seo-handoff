#!/usr/bin/env python3
"""Patch all Type 3 images on Engagement post WP #29985."""
import base64
import json
import os
import re
import urllib.request
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
POST_ID = 29985
SLUG = "engagement-quotes"

PROMPTS = json.loads((ROOT / "output/Week1_Rank7_EngagementQuotes_type3_prompts.json").read_text())

# Use already uploaded media IDs to avoid duplicate uploads
UPLOADED_MEDIA = {
    "hero": {
        "id": 29986,
        "src": "https://blog.bluestone.com/wp-content/uploads/2026/07/engagement-hero-2026.webp",
        "alt": "Congratulations wishes for engagement 2026 hero, couple with The Malibu Ring",
        "w": 1400,
        "h": 787,
    },
    "flatlay": {
        "id": 29987,
        "src": "https://blog.bluestone.com/wp-content/uploads/2026/07/engagement-flatlay-2026.webp",
        "alt": "Engagement quotes and wishes card flatlay with The Gigi Ring",
        "w": 1400,
        "h": 787,
    },
    "lifestyle": {
        "id": 29988,
        "src": "https://blog.bluestone.com/wp-content/uploads/2026/07/engagement-lifestyle-2026.webp",
        "alt": "Happy engagement wishes 2026 lifestyle with The Anya Ring",
        "w": 1400,
        "h": 787,
    },
}


def load_env():
    for line in (ROOT / ".env").read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip("'\""))


def api(method, path, data=None, raw_body=None, headers=None):
    token = base64.b64encode(f"{os.environ['WP_USER']}:{os.environ['WP_APP_PASSWORD']}".encode()).decode()
    h = {"Authorization": f"Basic {token}", "User-Agent": "BluestoneSEO/1.0"}
    if headers:
        h.update(headers)
    body = json.dumps(data).encode() if data is not None else raw_body
    if data is not None:
        h["Content-Type"] = "application/json"
    req = urllib.request.Request(f"https://blog.bluestone.com/wp-json/wp/v2/{path}", data=body, headers=h, method=method)
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read().decode())


def image_block(mid, src, alt, w, h):
    clean_alt = re.sub(r"[^A-Za-z0-9\s,\.\-\'\!\(\)\?]", "", alt)
    return (
        f'<!-- wp:image {{"id":{mid},"sizeSlug":"full","linkDestination":"none"}} -->\n'
        f'<figure class="wp-block-image size-full">'
        f'<img src="{src}" alt="{clean_alt}" class="wp-image-{mid}"/>'
        f"</figure>\n<!-- /wp:image -->"
    )


def validate_content(content):
    article_content = content.split('<script type="application/ld+json" id="bs-faq-schema">', 1)[0]
    visible = re.sub(r"<(style|script)\b[^>]*>[\s\S]*?</\1>", " ", article_content, flags=re.I)
    visible = re.sub(r"<[^>]+>", " ", visible)
    rules = {
        "no_em_dash": "—" not in visible,
        "no_en_dash": "–" not in visible,
        "no_spaced_hyphen": re.search(r"\s-\s", visible) is None,
        "no_prices": not re.search(r"(?:₹|Rs\.?\s*\d|INR\s*\d)", visible, re.I),
        "no_last_updated": "Last updated" not in visible,
        "year_2025_body_gone": "2025" not in visible,
        "carousel_mid_article": content.index("bs-cf-engagement") < content.index("Frequently Asked Questions"),
        "six_buy_links": content.count(">Buy now<") == 6,
        "faq_schema": '"@type": "FAQPage"' in content,
        "blog_schema": '"@type": "BlogPosting"' in content,
        "no_content_h1": "<h1" not in content.lower(),
        "flatlay_inserted": "engagement-flatlay-2026.webp" in content,
        "lifestyle_inserted": "engagement-lifestyle-2026.webp" in content,
    }
    failed = [name for name, passed in rules.items() if not passed]
    if failed:
        raise SystemExit(f"Content validation failed: {failed}")
    return rules


def main():
    load_env()

    print("Fetching post...")
    post = api("GET", f"posts/{POST_ID}?context=edit")
    content = post["content"]["raw"]

    featured_id = UPLOADED_MEDIA["hero"]["id"]

    # 1. Clean up existing schema block if present
    print("Stripping old schema block...")
    content_clean = re.sub(
        r'<!-- wp:html -->\s*<script type="application/ld\+json" id="bs-faq-schema">.*?</script>\s*<script type="application/ld\+json" id="bs-blogposting-schema">.*?</script>\s*<!-- /wp:html -->',
        '',
        content,
        flags=re.DOTALL
    ).strip()

    # 2. Insert flatlay image block
    print("Inserting Flatlay image...")
    # Escape character & is represented as &amp; in WP content
    flatlay_target = '<!-- wp:heading -->\n<h2 class="wp-block-heading">Ring Ceremony Wishes &amp; Messages</h2>'
    flatlay_block = image_block(
        UPLOADED_MEDIA["flatlay"]["id"],
        UPLOADED_MEDIA["flatlay"]["src"],
        UPLOADED_MEDIA["flatlay"]["alt"],
        UPLOADED_MEDIA["flatlay"]["w"],
        UPLOADED_MEDIA["flatlay"]["h"]
    )
    if flatlay_target not in content_clean:
        flatlay_target_alt = '<h2 class="wp-block-heading">Ring Ceremony Wishes &amp; Messages</h2>'
        if flatlay_target_alt in content_clean:
            content_clean = content_clean.replace(flatlay_target_alt, f"{flatlay_block}\n\n{flatlay_target_alt}")
        else:
            raise SystemExit("Could not find insertion point for Flatlay image.")
    else:
        content_clean = content_clean.replace(flatlay_target, f"{flatlay_block}\n\n{flatlay_target}")

    # 3. Insert lifestyle image block
    print("Inserting Lifestyle image...")
    lifestyle_target = '<!-- wp:heading -->\n<h2 class="wp-block-heading">Happy Engagement Anniversary Wishes</h2>'
    lifestyle_block = image_block(
        UPLOADED_MEDIA["lifestyle"]["id"],
        UPLOADED_MEDIA["lifestyle"]["src"],
        UPLOADED_MEDIA["lifestyle"]["alt"],
        UPLOADED_MEDIA["lifestyle"]["w"],
        UPLOADED_MEDIA["lifestyle"]["h"]
    )
    if lifestyle_target not in content_clean:
        lifestyle_target_alt = '<h2 class="wp-block-heading">Happy Engagement Anniversary Wishes</h2>'
        if lifestyle_target_alt in content_clean:
            content_clean = content_clean.replace(lifestyle_target_alt, f"{lifestyle_block}\n\n{lifestyle_target_alt}")
        else:
            raise SystemExit("Could not find insertion point for Lifestyle image.")
    else:
        content_clean = content_clean.replace(lifestyle_target, f"{lifestyle_block}\n\n{lifestyle_target}")

    # 4. Extract existing schema and update images
    product_media_file = ROOT / "output/Week1_Rank7_EngagementQuotes_product_media.json"
    product_media = json.loads(product_media_file.read_text())
    product_images = [p["src"] for p in product_media]

    # Re-build schemas
    import sys
    sys.path.append(str(ROOT / "scripts"))
    from publish_engagement_article import build_faqs, TITLE, META_DESC, FOCUS_KW, YOAST_TITLE
    _, faq_schema = build_faqs()
    
    faq_page = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_schema}
    
    all_images = [UPLOADED_MEDIA["hero"]["src"], UPLOADED_MEDIA["flatlay"]["src"], UPLOADED_MEDIA["lifestyle"]["src"]] + product_images
    
    blog_posting = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": TITLE,
        "description": META_DESC,
        "datePublished": "2026-07-16",
        "dateModified": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "author": {"@type": "Person", "name": "Vikas"},
        "publisher": {"@type": "Organization", "name": "BlueStone", "url": "https://www.bluestone.com/"},
        "image": all_images,
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"https://blog.bluestone.com/{SLUG}/"},
        "keywords": [
            "engagement quotes",
            "happy engagement anniversary",
            "happy engagement wishes",
            "happy engagement",
            "ring ceremony wishes",
            "congratulations wishes for engagement",
        ],
    }

    schema_block = (
        "\n\n<!-- wp:html -->\n"
        f'<script type="application/ld+json" id="bs-faq-schema">{json.dumps(faq_page, ensure_ascii=False)}</script>\n'
        f'<script type="application/ld+json" id="bs-blogposting-schema">{json.dumps(blog_posting, ensure_ascii=False)}</script>\n'
        "<!-- /wp:html -->\n"
    )
    final_content = content_clean + schema_block

    print("Running validation checks...")
    rules = validate_content(final_content)
    print("Validation checks passed!")

    print("Updating post content and featured image...")
    payload = {
        "content": final_content,
        "featured_media": featured_id
    }
    updated_post = api("POST", f"posts/{POST_ID}", payload)
    print(f"Post updated successfully! URL: {updated_post['link']}")
    
    # Save the updated HTML locally as well
    (ROOT / "output/Week1_Rank7_EngagementQuotes_article.html").write_text(final_content)
    print("Saved local HTML file output/Week1_Rank7_EngagementQuotes_article.html")


if __name__ == "__main__":
    main()
