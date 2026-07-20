#!/usr/bin/env python3
"""Clean patch: upload Daughter's Day Type 3 images, set featured, insert body images, refresh schema."""
from __future__ import annotations

import base64
import json
import os
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "emotional-daughters-day-quotes-2026"

PROMPTS = json.loads(
    (ROOT / "output/Week1_Rank32_DaughtersDay_type3_prompts.json").read_text(encoding="utf-8")
)
POST_ID = PROMPTS.get("wp_post_id")

SLOTS = {
    "hero": {
        "src": ROOT / "output/magnific_generated/daughters-day-hero-2026.webp",
        "featured": True,
        "media_title": "emotional daughters day quotes 2026 Hero",
    },
    "flatlay": {
        "src": ROOT / "output/magnific_generated/daughters-day-flatlay-2026.webp",
        "featured": False,
        "media_title": "emotional daughters day quotes 2026 Flatlay",
    },
    "lifestyle": {
        "src": ROOT / "output/magnific_generated/daughters-day-lifestyle-2026.webp",
        "featured": False,
        "media_title": "emotional daughters day quotes 2026 Lifestyle",
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
    req = urllib.request.Request(
        f"https://blog.bluestone.com/wp-json/wp/v2/{path}", data=body, headers=h, method=method
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read().decode())


def upload_media(path, alt, title):
    headers = {
        "Content-Disposition": f'attachment; filename="{path.name}"',
        "Content-Type": "image/webp",
    }
    media = api("POST", "media", raw_body=path.read_bytes(), headers=headers)
    api("POST", f"media/{media['id']}", {"alt_text": alt, "title": title})
    return media


def image_block(mid, src, alt):
    clean_alt = re.sub(r"[^A-Za-z0-9\s,\.\-\'\!\(\)\?]", "", alt)
    return (
        f'<!-- wp:image {{"id":{mid},"sizeSlug":"full","linkDestination":"none"}} -->\n'
        f'<figure class="wp-block-image size-full">'
        f'<img src="{src}" alt="{clean_alt}" class="wp-image-{mid}"/>'
        f"</figure>\n<!-- /wp:image -->"
    )


def main():
    if not POST_ID:
        raise SystemExit("Set wp_post_id in Week1_Rank32_DaughtersDay_type3_prompts.json first.")

    load_env()

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

    print("Stripping old schema blocks...")
    content_clean = re.sub(
        r'<!-- wp:html -->\s*<script type="application/ld\+json" id="bs-faq-schema">.*?</script>\s*'
        r'<script type="application/ld\+json" id="bs-blogposting-schema">.*?</script>\s*<!-- /wp:html -->',
        "",
        content_clean,
        flags=re.DOTALL,
    ).strip()

    uploaded = {}
    featured_id = None

    for slot, cfg in SLOTS.items():
        if not cfg["src"].exists():
            raise SystemExit(f"Missing {cfg['src']}. Generate first.")
        alt = PROMPTS["slots"][slot].get("alt", f"emotional daughters day quotes 2026 {slot}")
        print(f"Uploading {slot} image...")
        media = upload_media(cfg["src"], alt, cfg["media_title"])
        uploaded[slot] = {"id": media["id"], "src": media["source_url"], "alt": alt}
        if cfg["featured"]:
            featured_id = media["id"]
        print(f"  Uploaded {slot} -> media ID: {media['id']}")

    import sys

    sys.path.append(str(ROOT / "scripts"))
    from publish_daughters_day_article import FLATLAY_INSERT_H2, LIFESTYLE_INSERT_H2, META_DESC, TITLE, build_faqs

    def find_h2_target(heading: str) -> str:
        candidates = [
            f'<h2 class="wp-block-heading">{heading}</h2>',
            f'<h2 class="wp-block-heading">{heading.replace(chr(39), "&#x27;")}</h2>',
            f'<h2 class="wp-block-heading">{heading.replace(chr(39), "&#39;")}</h2>',
        ]
        for target in candidates:
            if target in content_clean:
                return target
        raise SystemExit(f"Could not find {heading!r} heading for image insertion.")

    flatlay_target = find_h2_target(FLATLAY_INSERT_H2)
    flatlay_block = image_block(
        uploaded["flatlay"]["id"],
        uploaded["flatlay"]["src"],
        uploaded["flatlay"]["alt"],
    )
    content_clean = content_clean.replace(flatlay_target, f"{flatlay_block}\n\n{flatlay_target}", 1)

    lifestyle_target = find_h2_target(LIFESTYLE_INSERT_H2)
    lifestyle_block = image_block(
        uploaded["lifestyle"]["id"],
        uploaded["lifestyle"]["src"],
        uploaded["lifestyle"]["alt"],
    )
    content_clean = content_clean.replace(lifestyle_target, f"{lifestyle_block}\n\n{lifestyle_target}", 1)

    product_media = json.loads(
        (ROOT / "output/Week1_Rank32_DaughtersDay_product_media.json").read_text(encoding="utf-8")
    )
    product_images = [p["src"] for p in product_media]
    _, faq_schema = build_faqs()
    faq_page = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_schema}

    all_images = [
        uploaded["hero"]["src"],
        uploaded["flatlay"]["src"],
        uploaded["lifestyle"]["src"],
    ] + product_images
    blog_posting = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": TITLE,
        "description": META_DESC,
        "datePublished": "2026-07-19",
        "dateModified": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "author": {"@type": "Person", "name": "Vikas"},
        "publisher": {"@type": "Organization", "name": "BlueStone", "url": "https://www.bluestone.com/"},
        "image": all_images,
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"https://blog.bluestone.com/{SLUG}/"},
        "keywords": [
            "emotional daughters day quotes",
            "daughters day wishes",
            "beautiful words for my daughter",
            "wishes for daughter",
            "daughters day captions",
            "daughters day 2026",
        ],
    }
    schema_block = (
        "\n\n<!-- wp:html -->\n"
        f'<script type="application/ld+json" id="bs-faq-schema">{json.dumps(faq_page, ensure_ascii=False)}</script>\n'
        f'<script type="application/ld+json" id="bs-blogposting-schema">{json.dumps(blog_posting, ensure_ascii=False)}</script>\n'
        "<!-- /wp:html -->\n"
    )
    final_content = content_clean + schema_block

    img_blocks = re.findall(r"<!-- wp:image", final_content)
    print(f"  Image blocks in content: {len(img_blocks)} (expected: 2)")
    assert len(img_blocks) == 2, f"Expected 2 image blocks, found {len(img_blocks)}"

    print("Updating post content and featured image...")
    updated = api(
        "POST",
        f"posts/{POST_ID}",
        {
            "content": final_content,
            "featured_media": featured_id,
            "author": 270271338,
            "categories": [554493477, 554493415],
            "meta": {
                "_yoast_wpseo_opengraph-image": uploaded["hero"]["src"],
                "_yoast_wpseo_twitter-image": uploaded["hero"]["src"],
            },
        },
    )
    print(f"Post updated! URL: {updated['link']}")
    (ROOT / "output/Week1_Rank32_DaughtersDay_article.html").write_text(final_content, encoding="utf-8")
    (ROOT / "output/Week1_Rank32_DaughtersDay_type3_media.json").write_text(
        json.dumps(uploaded, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
