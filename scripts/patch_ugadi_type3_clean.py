#!/usr/bin/env python3
"""Clean patch: upload Ugadi Type 3 images, set featured, insert body images, refresh schema."""
from __future__ import annotations
import base64
import json
import os
import re
import urllib.request
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
SLUG = "happy-ugadi-wishes-in-telugu-2027"

PROMPTS = json.loads((ROOT / "output/Week1_Rank21_Ugadi_type3_prompts.json").read_text(encoding="utf-8"))
POST_ID = PROMPTS.get("wp_post_id")

SLOTS = {
    "hero": {
        "src": ROOT / "output/magnific_generated/ugadi-hero-2027.webp",
        "featured": True,
    },
    "flatlay": {
        "src": ROOT / "output/magnific_generated/ugadi-flatlay-2027.webp",
        "featured": False,
    },
    "lifestyle": {
        "src": ROOT / "output/magnific_generated/ugadi-lifestyle-2027.webp",
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


def upload_media(path, alt):
    headers = {
        "Content-Disposition": f'attachment; filename="{path.name}"',
        "Content-Type": "image/webp",
    }
    media = api("POST", "media", raw_body=path.read_bytes(), headers=headers)
    api("POST", f"media/{media['id']}", {"alt_text": alt, "title": path.stem})
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
        raise SystemExit("Set wp_post_id in Week1_Rank21_Ugadi_type3_prompts.json first.")

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
        alt = PROMPTS["slots"][slot].get("alt", f"Ugadi 2027 {slot}")
        print(f"Uploading {slot} image...")
        media = upload_media(cfg["src"], alt)
        uploaded[slot] = {"id": media["id"], "src": media["source_url"], "alt": alt}
        if cfg["featured"]:
            featured_id = media["id"]
        print(f"  Uploaded {slot} -> media ID: {media['id']}")

    flatlay_target = '<h2 class="wp-block-heading">Happy Ugadi Wishes 2027 in English</h2>'
    flatlay_block = image_block(
        uploaded["flatlay"]["id"],
        uploaded["flatlay"]["src"],
        uploaded["flatlay"]["alt"],
    )
    if flatlay_target in content_clean:
        content_clean = content_clean.replace(flatlay_target, f"{flatlay_block}\n\n{flatlay_target}", 1)
    else:
        raise SystemExit("Could not find English wishes heading for flatlay insertion.")

    lifestyle_target = '<h2 class="wp-block-heading">Ugadi Captions &amp; Status for Instagram and WhatsApp</h2>'
    lifestyle_block = image_block(
        uploaded["lifestyle"]["id"],
        uploaded["lifestyle"]["src"],
        uploaded["lifestyle"]["alt"],
    )
    if lifestyle_target in content_clean:
        content_clean = content_clean.replace(lifestyle_target, f"{lifestyle_block}\n\n{lifestyle_target}", 1)
    else:
        raise SystemExit("Could not find captions heading for lifestyle insertion.")

    import sys

    sys.path.append(str(ROOT / "scripts"))
    from publish_ugadi_article import TITLE, META_DESC, build_faqs

    product_media = json.loads((ROOT / "output/Week1_Rank21_Ugadi_product_media.json").read_text(encoding="utf-8"))
    product_images = [p["src"] for p in product_media]
    _, faq_schema = build_faqs()
    faq_page = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_schema}

    all_images = [uploaded["hero"]["src"], uploaded["flatlay"]["src"], uploaded["lifestyle"]["src"]] + product_images
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
            "happy ugadi wishes in telugu",
            "happy ugadi 2027 wishes in telugu",
            "ugadi wishes in telugu",
            "whatsapp ugadi wishes",
            "happy ugadi wishes 2027",
            "ugadi 2027 wishes",
            "ugadi captions",
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
        {"content": final_content, "featured_media": featured_id, "author": 270271338},
    )
    print(f"Post updated! URL: {updated['link']}")
    (ROOT / "output/Week1_Rank21_Ugadi_article.html").write_text(final_content, encoding="utf-8")


if __name__ == "__main__":
    main()
