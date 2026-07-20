#!/usr/bin/env python3
"""Patch Type 3 image on published Diwali post (WP #29935)."""
import base64
import json
import os
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POST_ID = 29935
SLUG = "happy-diwali-wishes-messages-quotes-2026"

FLATLAY = {
    "src": ROOT / "output/magnific_generated/diwali-flatlay-phone-2026.webp",
    "filename": "diwali-flatlay-phone-2026.webp",
    "alt": "Happy Diwali 2026 flatlay with Thyvarne pendant, diyas and blank phone on cream linen",
    "old_media_id": 29933,
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


def main():
    load_env()
    if "WP_USER" not in os.environ or "WP_APP_PASSWORD" not in os.environ:
        raise SystemExit("WP_USER and WP_APP_PASSWORD required in .env")
    if not FLATLAY["src"].exists():
        raise SystemExit(f"Missing {FLATLAY['src']}. Regenerate first.")

    from PIL import Image

    im = Image.open(FLATLAY["src"])
    w, h = im.size

    media = upload_media(FLATLAY["src"], FLATLAY["alt"])
    new_id = media["id"]
    new_url = media["source_url"]
    print("uploaded flatlay", new_id, new_url)

    post = api("GET", f"posts/{POST_ID}?context=edit")
    content = post["content"]["raw"]

    old_id = FLATLAY["old_media_id"]
    old_media = api("GET", f"media/{old_id}")
    old_url = old_media["source_url"]

    content = content.replace(old_url, new_url)
    content = re.sub(
        rf'<!-- wp:image {{"id":{old_id},',
        f'<!-- wp:image {{"id":{new_id},',
        content,
    )
    content = re.sub(rf'class="wp-image-{old_id}"', f'class="wp-image-{new_id}"', content)
    content = content.replace(
        f'width="{old_media.get("media_details", {}).get("width", 1024)}"',
        f'width="{w}"',
        1,
    )
    # Update flatlay img tag dimensions by id
    content = re.sub(
        rf'(class="wp-image-{new_id}"[^>]+width=")\d+("[^>]+height=")\d+',
        lambda m: f'{m.group(1)}{w}{m.group(2)}{h}',
        content,
        count=1,
    )

    # Refresh BlogPosting schema image array entry for flatlay
    content = content.replace(old_url, new_url)

    api("POST", f"posts/{POST_ID}", {"content": content})
    print("patched post", POST_ID, f"https://blog.bluestone.com/{SLUG}/")

    html = urllib.request.urlopen(
        urllib.request.Request(f"https://blog.bluestone.com/{SLUG}/?v=flatlay", headers={"User-Agent": "Mozilla/5.0"}),
        timeout=30,
    ).read().decode("utf-8", "replace")
    print("live flatlay url in page:", new_url in html)
    print("old flatlay url gone:", old_url not in html)


if __name__ == "__main__":
    main()
