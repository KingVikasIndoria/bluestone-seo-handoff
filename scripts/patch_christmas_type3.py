#!/usr/bin/env python3
"""Patch all Type 3 images on Christmas post WP #16842."""
import base64
import json
import os
import re
import urllib.request
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
POST_ID = 16842
SLUG = "xmas-wishes-quotes"

PROMPTS = json.loads((ROOT / "output/Week1_Rank8_ChristmasWishes_type3_prompts.json").read_text())

SLOTS = {
    "hero": {
        "src": ROOT / "output/magnific_generated/christmas-hero-2026.webp",
        "featured": True,
    },
    "flatlay": {
        "src": ROOT / "output/magnific_generated/christmas-flatlay-2026.webp",
        "featured": False,
    },
    "lifestyle": {
        "src": ROOT / "output/magnific_generated/christmas-lifestyle-2026.webp",
        "featured": False,
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


def upload_media(path: Path, alt: str):
    headers = {
        "Content-Disposition": f'attachment; filename="{path.name}"',
        "Content-Type": "image/webp",
    }
    media = api("POST", "media", raw_body=path.read_bytes(), headers=headers)
    api("POST", f"media/{media['id']}", {"alt_text": alt, "title": path.stem})
    return media


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
        "carousel_mid_article": content.index("bs-cf-christmas") < content.index("Frequently Asked Questions"),
        "six_buy_links": content.count(">Buy now<") == 6,
        "faq_schema": '"@type": "FAQPage"' in content,
        "blog_schema": '"@type": "BlogPosting"' in content,
        "no_content_h1": "<h1" not in content.lower(),
        "flatlay_inserted": "christmas-flatlay-2026.webp" in content,
        "lifestyle_inserted": "christmas-lifestyle-2026.webp" in content,
    }
    failed = [name for name, passed in rules.items() if not passed]
    if failed:
        raise SystemExit(f"Content validation failed: {failed}")
    return rules


def main():
    load_env()
    from PIL import Image

    print("Fetching post...")
    post = api("GET", f"posts/{POST_ID}?context=edit")
    content = post["content"]["raw"]

    uploaded = {}
    featured_id = None

    for slot, cfg in SLOTS.items():
        if not cfg["src"].exists():
            raise SystemExit(f"Missing {cfg['src']}. Generate first.")
        alt = PROMPTS["slots"][slot].get("alt", f"Christmas 2026 {slot}")
        im = Image.open(cfg["src"])
        w, h = im.size
        print(f"Uploading {slot} image ({w}x{h})...")
        media = upload_media(cfg["src"], alt)
        uploaded[slot] = {
            "id": media["id"],
            "src": media["source_url"],
            "alt": alt,
            "w": w,
            "h": h
        }
        if cfg["featured"]:
            featured_id = media["id"]
        print(f"Uploaded {slot} media ID: {media['id']}")

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
    # Escape character & is represented as &amp; in WP content if any
    flatlay_target = '<!-- wp:heading -->\n<h2 class="wp-block-heading">Romantic Christmas Wishes for Partners</h2>'
    flatlay_block = image_block(
        uploaded["flatlay"]["id"],
        uploaded["flatlay"]["src"],
        uploaded["flatlay"]["alt"],
        uploaded["flatlay"]["w"],
        uploaded["flatlay"]["h"]
    )
    if flatlay_target not in content_clean:
        flatlay_target_alt = '<h2 class="wp-block-heading">Romantic Christmas Wishes for Partners</h2>'
        if flatlay_target_alt in content_clean:
            content_clean = content_clean.replace(flatlay_target_alt, f"{flatlay_block}\n\n{flatlay_target_alt}")
        else:
            raise SystemExit("Could not find insertion point for Flatlay image.")
    else:
        content_clean = content_clean.replace(flatlay_target, f"{flatlay_block}\n\n{flatlay_target}")

    # 3. Insert lifestyle image block
    print("Inserting Lifestyle image...")
    lifestyle_target = '<!-- wp:heading -->\n<h2 class="wp-block-heading">Combined Christmas and Happy New Year Wishes</h2>'
    lifestyle_block = image_block(
        uploaded["lifestyle"]["id"],
        uploaded["lifestyle"]["src"],
        uploaded["lifestyle"]["alt"],
        uploaded["lifestyle"]["w"],
        uploaded["lifestyle"]["h"]
    )
    if lifestyle_target not in content_clean:
        lifestyle_target_alt = '<h2 class="wp-block-heading">Combined Christmas and Happy New Year Wishes</h2>'
        if lifestyle_target_alt in content_clean:
            content_clean = content_clean.replace(lifestyle_target_alt, f"{lifestyle_block}\n\n{lifestyle_target_alt}")
        else:
            raise SystemExit("Could not find insertion point for Lifestyle image.")
    else:
        content_clean = content_clean.replace(lifestyle_target, f"{lifestyle_block}\n\n{lifestyle_target}")

    # 4. Extract existing schema and update images
    product_media_file = ROOT / "output/Week1_Rank8_ChristmasWishes_product_media.json"
    product_media = json.loads(product_media_file.read_text())
    product_images = [p["src"] for p in product_media]

    # Re-build schemas
    import sys
    sys.path.append(str(ROOT / "scripts"))
    from optimize_christmas_article import build_faqs, TITLE, META_DESC, FOCUS_KW, YOAST_TITLE
    _, faq_schema = build_faqs()
    
    faq_page = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_schema}
    
    all_images = [uploaded["hero"]["src"], uploaded["flatlay"]["src"], uploaded["lifestyle"]["src"]] + product_images
    
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
            "xmas wishes quotes",
            "merry christmas wishes 2021",
            "christmas and happy new year wishes",
            "christmas wishes and new year wishes",
            "christmas and new year wishes",
            "great christmas wishes",
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
    (ROOT / "output/Week1_Rank8_ChristmasWishes_article.html").write_text(final_content)
    print("Saved local HTML file output/Week1_Rank8_ChristmasWishes_article.html")


if __name__ == "__main__":
    main()
