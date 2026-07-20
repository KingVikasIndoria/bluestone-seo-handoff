#!/usr/bin/env python3
"""Clean patch: strip ALL old wp:image blocks, upload new Type 3 images, re-insert cleanly."""
from __future__ import annotations
import base64, json, os, re, urllib.request
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
POST_ID = 30064
SLUG = "ganesh-chaturthi-wishes-in-english"

PROMPTS = json.loads((ROOT / "output/Week1_Rank13_GaneshChaturthi_type3_prompts.json").read_text())

SLOTS = {
    "hero": {
        "src": ROOT / "output/magnific_generated/ganesh-hero-2026.webp",
        "featured": True,
    },
    "flatlay": {
        "src": ROOT / "output/magnific_generated/ganesh-flatlay-2026.webp",
        "featured": False,
    },
    "lifestyle": {
        "src": ROOT / "output/magnific_generated/ganesh-lifestyle-2026.webp",
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

    # STEP 1: Strip ALL existing wp:image blocks (remove old duplicates)
    print("Stripping ALL old wp:image blocks...")
    content_clean = re.sub(
        r'<!-- wp:image \{.*?\} -->\s*<figure.*?</figure>\s*<!-- /wp:image -->',
        '',
        content,
        flags=re.DOTALL
    )

    # STEP 2: Strip old schema blocks
    print("Stripping old schema blocks...")
    content_clean = re.sub(
        r'<!-- wp:html -->\s*<script type="application/ld\+json" id="bs-faq-schema">.*?</script>\s*<script type="application/ld\+json" id="bs-blogposting-schema">.*?</script>\s*<!-- /wp:html -->',
        '',
        content_clean,
        flags=re.DOTALL
    ).strip()

    # STEP 3: Upload new images
    uploaded = {}
    featured_id = None

    for slot, cfg in SLOTS.items():
        if not cfg["src"].exists():
            raise SystemExit(f"Missing {cfg['src']}. Generate first.")
        alt = PROMPTS["slots"][slot].get("alt", f"Ganesh Chaturthi 2026 {slot}")
        im = Image.open(cfg["src"])
        w, h = im.size
        print(f"Uploading {slot} image ({w}x{h})...")
        media = upload_media(cfg["src"], alt)
        uploaded[slot] = {"id": media["id"], "src": media["source_url"], "alt": alt, "w": w, "h": h}
        if cfg["featured"]:
            featured_id = media["id"]
        print(f"  Uploaded {slot} → media ID: {media['id']}")

    # STEP 4: Insert flatlay block (exactly once)
    print("Inserting Flatlay image block...")
    flatlay_target = '<h2 class="wp-block-heading">Vinayagar Chaturthi Wishes &amp; Regional Greetings</h2>'
    flatlay_block = image_block(uploaded["flatlay"]["id"], uploaded["flatlay"]["src"], uploaded["flatlay"]["alt"], uploaded["flatlay"]["w"], uploaded["flatlay"]["h"])
    
    if flatlay_target in content_clean:
        content_clean = content_clean.replace(flatlay_target, f"{flatlay_block}\n\n{flatlay_target}", 1)
    else:
        raise SystemExit("Could not find Vinayagar heading for flatlay insertion.")

    # STEP 5: Insert lifestyle block (exactly once)
    print("Inserting Lifestyle image block...")
    lifestyle_target = '<h2 class="wp-block-heading">Ganesh Chaturthi Wishes for Wealth, Prosperity &amp; Success</h2>'
    lifestyle_block = image_block(uploaded["lifestyle"]["id"], uploaded["lifestyle"]["src"], uploaded["lifestyle"]["alt"], uploaded["lifestyle"]["w"], uploaded["lifestyle"]["h"])
    
    if lifestyle_target in content_clean:
        content_clean = content_clean.replace(lifestyle_target, f"{lifestyle_block}\n\n{lifestyle_target}", 1)
    else:
        raise SystemExit("Could not find Wealth heading for lifestyle insertion.")

    # STEP 6: Re-build schemas
    import sys
    sys.path.append(str(ROOT / "scripts"))
    from publish_ganesh_article import build_faqs, TITLE, META_DESC

    product_media = json.loads((ROOT / "output/Week1_Rank13_GaneshChaturthi_product_media.json").read_text())
    product_images = [p["src"] for p in product_media]
    _, faq_schema = build_faqs()
    faq_page = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_schema}
    
    all_images = [uploaded["hero"]["src"], uploaded["flatlay"]["src"], uploaded["lifestyle"]["src"]] + product_images
    blog_posting = {
        "@context": "https://schema.org", "@type": "BlogPosting",
        "headline": TITLE, "description": META_DESC,
        "datePublished": "2026-07-16",
        "dateModified": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "author": {"@type": "Person", "name": "Vikas"},
        "publisher": {"@type": "Organization", "name": "BlueStone", "url": "https://www.bluestone.com/"},
        "image": all_images,
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"https://blog.bluestone.com/{SLUG}/"},
        "keywords": ["ganesh chaturthi wishes in english", "vinayagar chaturthi wishes", "lord ganesha happy ganesh chaturthi", "ganesh chaturthi quotes", "ganapti quotes", "ganesha quotes", "ganpati quotes"],
    }
    schema_block = (
        "\n\n<!-- wp:html -->\n"
        f'<script type="application/ld+json" id="bs-faq-schema">{json.dumps(faq_page, ensure_ascii=False)}</script>\n'
        f'<script type="application/ld+json" id="bs-blogposting-schema">{json.dumps(blog_posting, ensure_ascii=False)}</script>\n'
        "<!-- /wp:html -->\n"
    )
    final_content = content_clean + schema_block

    # STEP 7: Validate
    print("Running validation checks...")
    # Count image blocks — should be exactly 2
    img_blocks = re.findall(r'<!-- wp:image', final_content)
    print(f"  Image blocks in content: {len(img_blocks)} (expected: 2)")
    assert len(img_blocks) == 2, f"Expected 2 image blocks, found {len(img_blocks)}"
    
    assert "ganesh-flatlay" in final_content, "Flatlay missing"
    assert "ganesh-lifestyle" in final_content, "Lifestyle missing"
    assert '"@type": "FAQPage"' in final_content, "FAQ schema missing"
    assert '"@type": "BlogPosting"' in final_content, "BlogPosting schema missing"
    print("  All checks passed!")

    # STEP 8: Update post
    print("Updating post content and featured image...")
    updated = api("POST", f"posts/{POST_ID}", {"content": final_content, "featured_media": featured_id})
    print(f"Post updated! URL: {updated['link']}")
    
    (ROOT / "output/Week1_Rank13_GaneshChaturthi_article.html").write_text(final_content)
    print("Saved local HTML file.")


if __name__ == "__main__":
    main()
