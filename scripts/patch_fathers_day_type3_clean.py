#!/usr/bin/env python3
"""Clean patch: strip old schemas, handle media uploads, and generate optimized HTML local file if 401 block is encountered."""
from __future__ import annotations
import base64, json, os, re, urllib.request, urllib.error
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
POST_ID = 28468
SLUG = "happy-fathers-day-wishes-quotes-and-messages-for-every-dad"

PROMPTS = json.loads((ROOT / "output/Week1_Rank14_FathersDay_type3_prompts.json").read_text())

SLOTS = {
    "hero": {
        "src": ROOT / "output/magnific_generated/fathers-day-hero-2026.webp",
        "featured": True,
        "alt": "Father's Day warm family celebration featuring The Tetyana Gold Chain",
    },
    "flatlay": {
        "src": ROOT / "output/magnific_generated/fathers-day-flatlay-2026.webp",
        "featured": False,
        "alt": "Father's Day greeting card flatlay with The Jasper Band For Him",
    },
    "lifestyle": {
        "src": ROOT / "output/magnific_generated/fathers-day-lifestyle-2026.webp",
        "featured": False,
        "alt": "Father's Day warm celebration lifestyle with The Volara Bracelet For Him",
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
    print("Success fetching post raw content.")

    # STEP 1: Load pre-optimized local article text
    optimized_text_file = ROOT / "output/Week1_Rank14_FathersDay_article_optimized.html"
    if optimized_text_file.exists():
        print("Loading pre-optimized local text draft...")
        optimized_content = optimized_text_file.read_text(encoding='utf-8')
    else:
        print("WARNING: optimized content file not found. Using downloaded content.")
        optimized_content = content

    # STEP 2: Strip ALL existing wp:image blocks (prevents duplicates on re-runs)
    print("Stripping ALL existing wp:image blocks...")
    optimized_content = re.sub(
        r'<!-- wp:image \{.*?\} -->\s*<figure.*?</figure>\s*<!-- /wp:image -->',
        '',
        optimized_content,
        flags=re.DOTALL
    )
    # Also remove any leftover placeholder comments from previous fallback runs
    optimized_content = re.sub(r'<!-- WP_FEATURED_IMAGE_PLACEHOLDER:.*?-->', '', optimized_content)
    optimized_content = re.sub(r'<!-- IMAGE_FLATLAY_PLACEHOLDER:.*?-->', '', optimized_content)
    optimized_content = re.sub(r'<!-- IMAGE_LIFESTYLE_PLACEHOLDER:.*?-->', '', optimized_content)

    # Strip old schema script blocks
    print("Stripping old schema blocks...")
    optimized_content = re.sub(
        r'<!-- wp:html -->\s*<script type="application/ld\+json" id="bs-faq-schema">.*?</script>\s*<script type="application/ld\+json" id="bs-blogposting-schema">.*?</script>\s*<!-- /wp:html -->',
        '',
        optimized_content,
        flags=re.DOTALL
    ).strip()


    # STEP 2: Upload new images
    uploaded = {}
    featured_id = None

    for slot, cfg in SLOTS.items():
        img_path = cfg["src"]
        if not img_path.exists():
            print(f"Skipping missing image for {slot}: {img_path}")
            continue

        im = Image.open(img_path)
        w, h = im.size
        print(f"Uploading {slot} image ({w}x{h})...")
        media = upload_media(img_path, cfg["alt"])
        uploaded[slot] = {
            "id": media["id"],
            "url": media["source_url"],
            "w": w,
            "h": h
        }
        print(f"  Uploaded {slot} → media ID: {media['id']}")
        if cfg["featured"]:
            featured_id = media["id"]

    # STEP 3: Insert image blocks at the right positions
    # Hero goes before the first H2; flatlay goes after H2 #1; lifestyle goes after H2 #4
    print("Injecting Flatlay image block...")
    flatlay_block = image_block(
        uploaded["flatlay"]["id"],
        uploaded["flatlay"]["url"],
        SLOTS["flatlay"]["alt"],
        uploaded["flatlay"]["w"],
        uploaded["flatlay"]["h"]
    )
    print("Injecting Lifestyle image block...")
    lifestyle_block = image_block(
        uploaded["lifestyle"]["id"],
        uploaded["lifestyle"]["url"],
        SLOTS["lifestyle"]["alt"],
        uploaded["lifestyle"]["w"],
        uploaded["lifestyle"]["h"]
    )

    # Insert flatlay before the 2nd H2 and lifestyle before the 4th H2
    h2_pattern = re.compile(r'(<h2\b[^>]*>)', re.IGNORECASE)
    h2_matches = list(h2_pattern.finditer(optimized_content))
    content_patched = optimized_content
    if len(h2_matches) >= 4:
        # Insert lifestyle before H2 #4 (index 3)
        pos4 = h2_matches[3].start()
        content_patched = content_patched[:pos4] + lifestyle_block + "\n\n" + content_patched[pos4:]
        # Re-find H2s since string changed
        h2_matches2 = list(h2_pattern.finditer(content_patched))
        if len(h2_matches2) >= 2:
            pos2 = h2_matches2[1].start()
            content_patched = content_patched[:pos2] + flatlay_block + "\n\n" + content_patched[pos2:]
    else:
        # Fallback: append flatlay and lifestyle at the end if H2 structure not found
        content_patched = optimized_content + "\n\n" + flatlay_block + "\n\n" + lifestyle_block

    # STEP 4: Build Schema scripts
    print("Building schema scripts...")
    faq_schema = (
        '<!-- wp:html -->\n'
        '<script type="application/ld+json" id="bs-faq-schema">\n'
        '{\n'
        '  "@context": "https://schema.org",\n'
        '  "@type": "FAQPage",\n'
        '  "mainEntity": [\n'
        '    {\n'
        '      "@type": "Question",\n'
        '      "name": "What are some emotional Father\'s Day wishes?",\n'
        '      "acceptedAnswer": {\n'
        '        "@type": "Answer",\n'
        '        "text": "Sentimental Father\'s Day messages thank dads for their silent sacrifices, protection, guidance, and unconditional love, expressing how much they mean to you."\n'
        '      }\n'
        '    },\n'
        '    {\n'
        '      "@type": "Question",\n'
        '      "name": "How do I wish my dad a Happy Father\'s Day?",\n'
        '      "acceptedAnswer": {\n'
        '        "@type": "Answer",\n'
        '        "text": "You can send a heartfelt quotes message, write a handwritten card, present a custom masculine gift, or share a WhatsApp Father Status to celebrate him."\n'
        '      }\n'
        '    }\n'
        '  ]\n'
        '}\n'
        '</script>\n'
        '<script type="application/ld+json" id="bs-blogposting-schema">\n'
        '{\n'
        '  "@context": "https://schema.org",\n'
        '  "@type": "BlogPosting",\n'
        '  "headline": "Happy Father’s Day Wishes, Quotes and Messages for Every Dad",\n'
        '  "image": "' + (uploaded["hero"]["url"] if "hero" in uploaded else "") + '",\n'
        '  "datePublished": "2026-05-15T11:34:21+00:00",\n'
        '  "dateModified": "' + datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00") + '",\n'
        '  "author": {\n'
        '    "@type": "Person",\n'
        '    "name": "BlueStone Editorial"\n'
        '  }\n'
        '}\n'
        '</script>\n'
        '<!-- /wp:html -->'
    )

    # Append schema to content
    content_final = content_patched.strip() + "\n\n" + faq_schema
    
    # Save optimized copy locally for manual upload fallback
    ROOT_OUTPUT_FILE = ROOT / "output/Week1_Rank14_FathersDay_article_optimized.html"
    ROOT_OUTPUT_FILE.write_text(content_final, encoding='utf-8')
    print(f"Saved local HTML copy to: {ROOT_OUTPUT_FILE}")

    # STEP 5: Push update to WordPress
    print("Running validation checks...")
    image_count = len(re.findall(r'<!-- wp:image', content_final))
    print(f"  Image blocks in content: {image_count} (expected: 2)")
    assert image_count == 2, f"Expected 2 image blocks, got {image_count}"
    print("  All checks passed!")

    print("Updating post content and featured image...")
    update_data = {"content": content_final}
    if featured_id:
        update_data["featured_media"] = featured_id
    res = api("POST", f"posts/{POST_ID}", update_data)
    print(f"Post updated! URL: {res['link']}")
    print("Saved local HTML file.")


if __name__ == "__main__":
    main()
