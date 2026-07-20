#!/usr/bin/env python3
"""Patch all Type 3 images on Children's Day post WP #16280."""
import base64
import json
import os
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POST_ID = 16280
SLUG = "happy-childrens-day-best-wishes-quotes-messages-for-kids"

PROMPTS = json.loads((ROOT / "output/Week1_Rank5_ChildrensDay_type3_prompts.json").read_text())

SLOTS = {
    "hero": {
        "src": ROOT / "output/magnific_generated/childrens-day-hero-2026.webp",
        "old_media_id": 29959,
        "featured": True,
    },
    "flatlay": {
        "src": ROOT / "output/magnific_generated/childrens-day-flatlay-2026.webp",
        "old_media_id": 29960,
        "featured": False,
    },
    "lifestyle": {
        "src": ROOT / "output/magnific_generated/childrens-day-lifestyle-2026.webp",
        "old_media_id": 29961,
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


def patch_image(content: str, slot: str, new_media: dict, old_id: int, w: int, h: int) -> str:
    old = api("GET", f"media/{old_id}")
    old_url = old["source_url"]
    new_url = new_media["source_url"]
    new_id = new_media["id"]
    content = content.replace(old_url, new_url)
    content = re.sub(rf'<!-- wp:image {{"id":{old_id},', f'<!-- wp:image {{"id":{new_id},', content)
    content = re.sub(rf'class="wp-image-{old_id}"', f'class="wp-image-{new_id}"', content)
    content = re.sub(
        rf'(class="wp-image-{new_id}"[^>]+width=")\d+("[^>]+height=")\d+',
        lambda m: f"{m.group(1)}{w}{m.group(2)}{h}",
        content,
        count=1,
    )
    return content


def main():
    load_env()
    from PIL import Image

    post = api("GET", f"posts/{POST_ID}?context=edit")
    content = post["content"]["raw"]
    featured_id = None
    new_urls = []

    for slot, cfg in SLOTS.items():
        if not cfg["src"].exists():
            raise SystemExit(f"Missing {cfg['src']}. Regenerate first.")
        alt = PROMPTS["slots"][slot].get("alt", f"Children's Day 2026 {slot}")
        im = Image.open(cfg["src"])
        w, h = im.size
        media = upload_media(cfg["src"], alt)
        new_urls.append(media["source_url"])
        content = patch_image(content, slot, media, cfg["old_media_id"], w, h)
        if cfg["featured"]:
            featured_id = media["id"]
        print("patched", slot, media["id"])

    payload = {"content": content}
    if featured_id:
        payload["featured_media"] = featured_id
    api("POST", f"posts/{POST_ID}", payload)
    print("updated post", POST_ID, f"https://blog.bluestone.com/{SLUG}/")


if __name__ == "__main__":
    main()
