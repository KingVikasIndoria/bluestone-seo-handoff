#!/usr/bin/env python3
"""Clean patch: strip ALL old wp:image blocks, upload new Type 3 images, re-insert cleanly."""
from __future__ import annotations
import base64
import json
import os
import re
import urllib.request
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
POST_ID = 21265
SLUG = "happy-womens-day-quotes-wishes-and-messages-to-celebrate-strength-and-empowerment"

PROMPTS = json.loads((ROOT / "output/Week1_Rank20_WomensDay_type3_prompts.json").read_text())

SLOTS = {
    "hero": {"src": ROOT / "output/magnific_generated/womens-day-hero-2027.webp", "featured": True},
    "flatlay": {"src": ROOT / "output/magnific_generated/womens-day-flatlay-2027.webp", "featured": False},
    "lifestyle": {"src": ROOT / "output/magnific_generated/womens-day-lifestyle-2027.webp", "featured": False},
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


def upload_media(path, alt):
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


def main():
    load_env()
    from PIL import Image

    print("Fetching post...")
    post = api("GET", f"posts/{POST_ID}?context=edit")
    content = post["content"]["raw"]

    print("Stripping ALL old wp:image blocks...")
    content_clean = re.sub(
        r"<!-- wp:image \{.*?\} -->\s*<figure.*?</figure>\s*<!-- /wp:image -->",
        "",
        content,
        flags=re.DOTALL,
    )
    content_clean = re.sub(
        r'<!-- wp:html -->\s*<script type="application/ld\+json" id="bs-faq-schema">.*?</script>\s*<script type="application/ld\+json" id="bs-blogposting-schema">.*?</script>\s*<!-- /wp:html -->',
        "",
        content_clean,
        flags=re.DOTALL,
    ).strip()

    uploaded = {}
    featured_id = None
    for slot, cfg in SLOTS.items():
        if not cfg["src"].exists():
            raise SystemExit(f"Missing {cfg['src']}. Generate first.")
        alt = PROMPTS["slots"][slot].get("alt", f"Women's Day 2027 {slot}")
        im = Image.open(cfg["src"])
        w, h = im.size
        print(f"Uploading {slot} image ({w}x{h})...")
        media = upload_media(cfg["src"], alt)
        uploaded[slot] = {"id": media["id"], "src": media["source_url"], "alt": alt, "w": w, "h": h}
        if cfg["featured"]:
            featured_id = media["id"]
        print(f"  Uploaded {slot} -> media ID: {media['id']}")

    flatlay_targets = [
        '<h2 class="wp-block-heading">Womens Day Quote in English</h2>',
    ]
    lifestyle_targets = [
        '<h2 class="wp-block-heading">Women&#x27;s Day Status for Instagram &amp; WhatsApp</h2>',
        '<h2 class="wp-block-heading">Women\'s Day Status for Instagram &amp; WhatsApp</h2>',
    ]

    flatlay_block = image_block(
        uploaded["flatlay"]["id"], uploaded["flatlay"]["src"], uploaded["flatlay"]["alt"],
        uploaded["flatlay"]["w"], uploaded["flatlay"]["h"],
    )
    for target in flatlay_targets:
        if target in content_clean:
            content_clean = content_clean.replace(target, f"{flatlay_block}\n\n{target}", 1)
            break
    else:
        raise SystemExit("Could not find English quotes heading for flatlay.")

    lifestyle_block = image_block(
        uploaded["lifestyle"]["id"], uploaded["lifestyle"]["src"], uploaded["lifestyle"]["alt"],
        uploaded["lifestyle"]["w"], uploaded["lifestyle"]["h"],
    )
    for target in lifestyle_targets:
        if target in content_clean:
            content_clean = content_clean.replace(target, f"{lifestyle_block}\n\n{target}", 1)
            break
    else:
        raise SystemExit("Could not find status heading for lifestyle.")

    import sys
    sys.path.append(str(ROOT / "scripts"))
    from optimize_womens_day_article import TITLE, META_DESC, build_faqs

    product_media = json.loads((ROOT / "output/Week1_Rank20_WomensDay_product_media.json").read_text())
    product_images = [p["src"] for p in product_media]
    _, faq_schema = build_faqs()
    faq_page = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_schema}
    all_images = [uploaded["hero"]["src"], uploaded["flatlay"]["src"], uploaded["lifestyle"]["src"]] + product_images
    blog_posting = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": TITLE,
        "description": META_DESC,
        "datePublished": "2026-02-16",
        "dateModified": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "author": {"@type": "Person", "name": "Vikas"},
        "publisher": {"@type": "Organization", "name": "BlueStone", "url": "https://www.bluestone.com/"},
        "image": all_images,
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"https://blog.bluestone.com/{SLUG}/"},
        "keywords": [
            "women's day message",
            "international women's day wishes",
            "happy womens day wishes quotes",
            "womens day quote in english",
            "womens day inspire quotes",
            "women's day status",
        ],
    }
    schema_block = (
        "\n\n<!-- wp:html -->\n"
        f'<script type="application/ld+json" id="bs-faq-schema">{json.dumps(faq_page, ensure_ascii=False)}</script>\n'
        f'<script type="application/ld+json" id="bs-blogposting-schema">{json.dumps(blog_posting, ensure_ascii=False)}</script>\n'
        "<!-- /wp:html -->\n"
    )
    final_content = content_clean + schema_block
    assert len(re.findall(r"<!-- wp:image", final_content)) == 2

    print("Updating post...")
    updated = api(
        "POST",
        f"posts/{POST_ID}",
        {"content": final_content, "featured_media": featured_id, "author": 270271338},
    )
    print(f"Post updated! URL: {updated['link']}")
    (ROOT / "output/Week1_Rank20_WomensDay_article.html").write_text(final_content)


if __name__ == "__main__":
    main()
