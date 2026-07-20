#!/usr/bin/env python3
"""Publish Week 1 Rank 30: Akshaya Tritiya quotes and wishes 2027 (New post)."""
import base64
import json
import os
import re
import urllib.request
from datetime import datetime, timezone
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAT_FESTIVE = 554493477
CAT_QUOTES = 554493415
LOCAL_ONLY = os.environ.get("BS_PUBLISH", "").lower() not in ("1", "true", "yes")


def load_local_env():
    env_path = ROOT / ".env"
    if env_path.exists():
        for raw_line in env_path.read_text().splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_local_env()
USER = os.environ.get("WP_USER", "")
PWD = os.environ.get("WP_APP_PASSWORD", "")
TOKEN = base64.b64encode(f"{USER}:{PWD}".encode()).decode() if USER and PWD else ""
AUTH = {"Authorization": f"Basic {TOKEN}", "User-Agent": "BluestoneSEO/1.0"} if TOKEN else {}
API = "https://blog.bluestone.com/wp-json/wp/v2"

CONTENT_DATA = json.loads(
    (ROOT / "output/Week1_Rank30_AkshayaQuotes_sections.json").read_text(encoding="utf-8")
)
META = CONTENT_DATA["meta"]
TITLE = META["title"]
SLUG = META["slug"]
META_DESC = META["meta_desc"]
FOCUS_KW = META["focus_kw"]
YOAST_TITLE = META["yoast_title"]
LIVE_URL = f"https://blog.bluestone.com/{SLUG}/"
OCCASION_YEAR = "Akshaya Tritiya 2027"
SECTIONS = CONTENT_DATA["sections"]
FAQS = CONTENT_DATA["faqs"]

PRODUCTS = [
    {
        "code": "BIPM0001H28",
        "name": "The Rohal Huggie Earrings",
        "url": "https://www.bluestone.com/earrings/the-rohal-huggie-earrings~21864.html",
        "png": ROOT / "ProductImages/seo images/Earrings/The Rohal Huggie Earrings.png",
    },
    {
        "code": "BIHS1145P21",
        "name": "The Valeria Rose Pendant",
        "url": "https://www.bluestone.com/pendants/the-valeria-rose-pendant~181266.html",
        "png": ROOT / "ProductImages/seo images/Pendants/The Valeria Rose Pendant.png",
    },
    {
        "code": "BISM0003O14",
        "name": "The Muricelle Bangle",
        "url": "https://www.bluestone.com/bangles/the-muricelle-bangle~1001.html",
        "png": ROOT / "ProductImages/seo images/Bangles/The Muricelle Bangle.png",
    },
    {
        "code": "BINS0639R18",
        "name": "The Gigi Ring",
        "url": "https://www.bluestone.com/rings/the-gigi-ring~64382.html",
        "png": ROOT / "ProductImages/seo images/Rings/The Gigi Ring.png",
    },
    {
        "code": "BISP0506C05",
        "name": "The Aarabhi Mangalsutra",
        "url": "https://www.bluestone.com/mangalsutra+chains/the-aarabhi-mangalsutra~46940.html",
        "png": ROOT / "ProductImages/seo images/Mangalsutra Chains/The Aarabhi Mangalsutra.png",
    },
    {
        "code": "BISA0255D05",
        "name": "The Asya Huggie Earrings",
        "url": "https://www.bluestone.com/earrings/the-asya-huggie-earrings~13494.html",
        "png": ROOT / "ProductImages/seo images/Earrings/The Asya Huggie Earrings.png",
    },
]


def api(method, path, data=None, raw_body=None, headers=None):
    request_headers = dict(AUTH)
    if headers:
        request_headers.update(headers)
    if data is not None:
        request_headers["Content-Type"] = "application/json"
        body = json.dumps(data).encode()
    else:
        body = raw_body
    req = urllib.request.Request(f"{API}/{path}", data=body, headers=request_headers, method=method)
    with urllib.request.urlopen(req, timeout=180) as response:
        return json.loads(response.read().decode())


def to_carousel_webp(src: Path, dest: Path):
    from PIL import Image

    image = Image.open(src).convert("RGB")
    target_w, target_h = 960, 535
    image.thumbnail((target_w, target_h), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (target_w, target_h), (245, 243, 240))
    canvas.paste(image, ((target_w - image.width) // 2, (target_h - image.height) // 2))
    dest.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dest, "WEBP", quality=82, method=6)


def upload_media(path: Path, alt: str, title: str):
    headers = {
        "Content-Disposition": f'attachment; filename="{path.name}"',
        "Content-Type": "image/webp",
    }
    media = api("POST", "media", raw_body=path.read_bytes(), headers=headers)
    api("POST", f"media/{media['id']}", {"alt_text": alt, "title": title})
    return media


def h2(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{escape(text)}</h2>\n<!-- /wp:heading -->'


def h3(text):
    return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{escape(text)}</h3>\n<!-- /wp:heading -->'


def para(text):
    return f'<!-- wp:paragraph -->\n<p>{text}</p>\n<!-- /wp:paragraph -->'


def list_block(items, ordered=True):
    tag = "ol" if ordered else "ul"
    attrs = ' {"ordered":true}' if ordered else ""
    lines = [f"<!-- wp:list{attrs} -->", f'<{tag} class="wp-block-list">']
    lines.extend(f"<li>{escape(item)}</li>" for item in items)
    lines.extend([f"</{tag}>", "<!-- /wp:list -->"])
    return "\n".join(lines)


def product_alt(name: str) -> str:
    return f"akshaya tritiya quote 2027 gift idea: {name}"


def product_title(name: str) -> str:
    return f"{name} carousel, {OCCASION_YEAR}"


def build_carousel(product_media):
    cards = []
    dots = []
    for index, product in enumerate(product_media):
        cards.append(
            f'    <div class="bs-cf-card" data-i="{index}">\n'
            f'      <a class="bs-cf-media" href="{product["url"]}">\n'
            f'        <img src="{product["src"]}" alt="{escape(product["alt"])}" width="960" height="535" loading="lazy" decoding="async"/>\n'
            f"      </a>\n"
            f'      <div class="bs-cf-meta">\n'
            f'        <p class="bs-cf-name">{escape(product["name"])}</p>\n'
            f'        <a class="bs-cf-cta" href="{product["url"]}">Buy now</a>\n'
            f"      </div>\n"
            f"    </div>"
        )
        active = " is-active" if index == 0 else ""
        dots.append(
            f'    <button type="button" class="bs-cf-dot{active}" data-i="{index}" aria-label="Product {index + 1}"></button>'
        )
    template = (ROOT / "templates/eid_carousel_6_snippet.html").read_text()
    style = template.split("<style>", 1)[1].split("</style>", 1)[0]
    script = template.split("<script>", 1)[1].split("</script>", 1)[0]
    script = script.replace("bs-cf-eid", "bs-cf-akshaya")
    return (
        "<!-- wp:html -->\n<style>\n"
        + style
        + '\n</style>\n<div class="bs-cf" id="bs-cf-akshaya" data-interval="3200" aria-roledescription="carousel" aria-label="BlueStone Akshaya Tritiya gift ideas">\n'
        + '  <button type="button" class="bs-cf-nav bs-cf-prev" aria-label="Previous">&#8249;</button>\n'
        + '  <button type="button" class="bs-cf-nav bs-cf-next" aria-label="Next">&#8250;</button>\n'
        + '  <div class="bs-cf-stage">\n'
        + "\n".join(cards)
        + '\n  </div>\n  <div class="bs-cf-dots" role="tablist">\n'
        + "\n".join(dots)
        + "\n  </div>\n</div>\n<script>\n"
        + script
        + "\n</script>\n<!-- /wp:html -->"
    )


def build_faqs():
    html = [h2("Frequently Asked Questions about Akshaya Tritiya Quotes")]
    schema = []
    for question, answer in FAQS:
        html.append(h3(question))
        html.append(para(escape(answer)))
        schema.append(
            {
                "@type": "Question",
                "name": question,
                "acceptedAnswer": {"@type": "Answer", "text": answer},
            }
        )
    return "\n\n".join(html), schema


def build_content(carousel, product_media):
    faq_html, faq_schema = build_faqs()
    parts = [
        '<!-- wp:html -->\n<style>\n.bs-eeat{margin:0 auto 1.25rem;max-width:720px;text-align:center;font-size:.95rem;color:#444;line-height:1.5}\n.bs-eeat strong{color:#111}\n.entry-content img,.wp-block-image img{max-width:100%;height:auto}\n</style>\n<!-- /wp:html -->',
        '<!-- wp:paragraph {"align":"center"} -->\n<p class="has-text-align-center bs-eeat">By <strong>Vikas</strong>, BlueStone Editorial</p>\n<!-- /wp:paragraph -->',
        para(
            "Looking for an <strong>akshaya tritiya quote</strong> you can copy for Akshaya Tritiya 2027? "
            "This guide gathers happy akshaya tritiya wishes, subho akshaya tritiya messages, WhatsApp lines, "
            "family blessings, spiritual notes, captions, and status updates ready to paste."
        ),
        para(
            "<strong>TL;DR:</strong> Pick a short WhatsApp wish, a family blessing, an akshaya tritiya quote for cards, "
            "or an Instagram caption. Every list is refreshed for Akshaya Tritiya 2027."
        ),
        para(
            "Akshaya Tritiya marks an auspicious spring day when many families pray, donate, and begin new plans with hope. "
            "A sincere wish, sent early, can feel as festive as temple visits when the words sound like your real gratitude."
        ),
        h2("Short Akshaya Tritiya Quotes for WhatsApp"),
        para(
            "These copy ready happy akshaya tritiya wishes stay short, warm, and easy to paste into chats and family groups."
        ),
        list_block(SECTIONS["whatsapp"]),
        h2("Happy Akshaya Tritiya Wishes for Family"),
        para(
            "Share these subho akshaya tritiya messages when you want fuller blessings for parents, elders, and the whole household."
        ),
        list_block(SECTIONS["family"]),
        h2("Happy Akshaya Tritiya Wishes for Friends"),
        para("Send these lighter festive lines to friends who feel like family."),
        list_block(SECTIONS["friends"]),
        h2("A Soft Akshaya Tritiya Gift Idea (If You Are Gifting Too)"),
        para(
            "Akshaya Tritiya is a beautiful time to mark prosperity with something lasting. "
            "Earrings, pendants, bangles, rings, and mangalsutra styles make thoughtful keepsakes after the puja. "
            "Explore these six approved designs from the BlueStone collection."
        ),
        carousel,
        h2("Akshaya Tritiya Quotes"),
        para(
            "Use these akshaya tritiya quote lines for cards, scrapbooks, and thoughtful notes that celebrate abundance with a light heart."
        ),
        list_block(SECTIONS["quotes"]),
        h2("Akshaya Tritiya Captions for Instagram"),
        para("Pair these Akshaya Tritiya captions with puja photos, gold shopping reels, or festive outfit posts."),
        list_block(SECTIONS["captions"], ordered=False),
        h2("Spiritual Akshaya Tritiya Wishes and Blessings"),
        para("Choose these spiritual lines when you want a calmer, prayerful tone for elders and morning blessings."),
        list_block(SECTIONS["spiritual"]),
        h2("Akshaya Tritiya Wishes for Colleagues"),
        para("Keep office greetings polite, brief, and hopeful for a productive season ahead."),
        list_block(SECTIONS["colleagues"]),
        h2("Akshaya Tritiya Status Lines"),
        para("Keep these Akshaya Tritiya status updates short enough for WhatsApp and warm enough for family circles."),
        list_block(SECTIONS["status"], ordered=False),
        h2("How to Pick the Right Akshaya Tritiya Message"),
        para(
            "Choose a short WhatsApp line for busy mornings, a family blessing for elders, and an akshaya tritiya quote for cards. "
            "Personalize with one name or memory, keep the tone honest, and refresh older year lines to Akshaya Tritiya 2027 before you send."
        ),
        h2("More Festive and Occasion Reads"),
        para(
            'Explore our other guides including <a href="https://blog.bluestone.com/happy-gudi-padwa-in-marathi-2027/">Happy Gudi Padwa in Marathi for 2027</a>, '
            '<a href="https://blog.bluestone.com/happy-ugadi-wishes-in-telugu-2027/">Happy Ugadi wishes in Telugu for 2027</a>, '
            '<a href="https://blog.bluestone.com/ganesh-chaturthi-wishes/">Ganesh Chaturthi wishes</a>, '
            '<a href="https://blog.bluestone.com/happy-diwali-wishes-messages-quotes-2026/">Diwali wishes for 2026</a>, '
            '<a href="https://blog.bluestone.com/happy-holi-wishes-messages-quotes-2027/">Holi wishes for 2027</a>, and '
            '<a href="https://blog.bluestone.com/dussehra-wishes-messages-quotes/">Dussehra wishes</a>. '
            'Learn more about <a href="https://en.wikipedia.org/wiki/Akshaya_Tritiya">Akshaya Tritiya on Wikipedia</a>.'
        ),
        faq_html,
        h2("Conclusion"),
        para(
            "The best akshaya tritiya quote lines sound personal, hopeful, and ready to share. "
            "Pick a WhatsApp wish, a family blessing, a quote, or a caption for Akshaya Tritiya 2027, "
            "and let your people know the day begins with grace. Happy Akshaya Tritiya 2027!"
        ),
    ]
    content = "\n\n".join(parts)
    images = [product["src"] for product in product_media]
    faq_page = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_schema}
    blog_posting = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": TITLE,
        "description": META_DESC,
        "datePublished": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "dateModified": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "author": {"@type": "Person", "name": "Vikas"},
        "publisher": {"@type": "Organization", "name": "BlueStone", "url": "https://www.bluestone.com/"},
        "image": images,
        "mainEntityOfPage": {"@type": "WebPage", "@id": LIVE_URL},
        "keywords": [
            "akshaya tritiya quote",
            "happy akshaya tritiya wishes",
            "subho akshaya tritiya",
            "akshaya tritiya captions",
            "akshaya tritiya status",
            "akshaya tritiya 2027",
        ],
    }
    content += (
        "\n\n<!-- wp:html -->\n"
        f'<script type="application/ld+json" id="bs-faq-schema">{json.dumps(faq_page, ensure_ascii=False)}</script>\n'
        f'<script type="application/ld+json" id="bs-blogposting-schema">{json.dumps(blog_posting, ensure_ascii=False)}</script>\n'
        "<!-- /wp:html -->\n"
    )
    return content


def validate_content(content):
    article_content = content.split('<script type="application/ld+json" id="bs-faq-schema">', 1)[0]
    visible = re.sub(r"<(style|script)\b[^>]*>[\s\S]*?</\1>", " ", article_content, flags=re.I)
    visible = re.sub(r"<[^>]+>", " ", visible)
    body_no_links = re.sub(r"<a\b[^>]*>[\s\S]*?</a>", " ", article_content, flags=re.I)
    body_no_links = re.sub(r"<(style|script)\b[^>]*>[\s\S]*?</\1>", " ", body_no_links, flags=re.I)
    body_no_links = re.sub(r"<[^>]+>", " ", body_no_links)
    rules = {
        "no_em_dash": "\u2014" not in visible,
        "no_en_dash": "\u2013" not in visible,
        "no_spaced_hyphen": re.search(r"\s-\s", visible) is None,
        "no_prices": not re.search(r"(?:₹|Rs\.?\s*\d|INR\s*\d)", visible, re.I),
        "no_last_updated": "Last updated" not in visible,
        "carousel_mid_article": content.index("bs-cf-akshaya") < content.index("Frequently Asked Questions"),
        "six_buy_links": content.count(">Buy now<") == 6,
        "faq_schema": '"@type": "FAQPage"' in content,
        "blog_schema": '"@type": "BlogPosting"' in content,
        "no_content_h1": "<h1" not in content.lower(),
        "year_2027": "2027" in visible,
        "primary_kw": "akshaya tritiya quote" in visible.lower(),
        "no_old_years_body": not re.search(r"\b(2021|2022|2023|2024|2025)\b", body_no_links),
        "meta_title_len": len(YOAST_TITLE) <= 60,
        "meta_desc_len": 150 <= len(META_DESC) <= 160,
        "hundred_plus_lines": sum(len(v) for v in SECTIONS.values()) >= 100,
    }
    failed = [name for name, passed in rules.items() if not passed]
    if failed:
        raise SystemExit(f"Content validation failed: {failed}")
    return rules


def build_product_media():
    assets = ROOT / "output/Week1_Rank30_AkshayaQuotes_assets"
    assets.mkdir(parents=True, exist_ok=True)
    product_media = []
    for product in PRODUCTS:
        if not product["png"].exists():
            raise SystemExit(f"Missing approved Type 2 image: {product['png']}")
        filename = re.sub(r"[^A-Za-z0-9]+", "-", product["name"]).strip("-").lower() + "-carousel.webp"
        webp = assets / filename
        to_carousel_webp(product["png"], webp)
        alt = product_alt(product["name"])
        title = product_title(product["name"])
        if LOCAL_ONLY:
            media = {"id": None, "source_url": str(webp.relative_to(ROOT))}
        else:
            media = upload_media(webp, alt, title)
        product_media.append(
            {
                "code": product["code"],
                "name": product["name"],
                "url": product["url"],
                "id": media["id"],
                "src": media["source_url"],
                "alt": alt,
                "title": title,
            }
        )
        print("prepared product", product["code"], media.get("id"), media["source_url"])
    return product_media


def main():
    assert 150 <= len(META_DESC) <= 160, len(META_DESC)
    assert len(YOAST_TITLE) <= 60, len(YOAST_TITLE)

    product_media = build_product_media()
    carousel = build_carousel(product_media)
    content = build_content(carousel, product_media)
    rules = validate_content(content)

    (ROOT / "output/Week1_Rank30_AkshayaQuotes_article.html").write_text(content, encoding="utf-8")
    (ROOT / "output/Week1_Rank30_AkshayaQuotes_product_media.json").write_text(
        json.dumps(product_media, indent=2), encoding="utf-8"
    )
    print("wrote local article and product_media")
    print("local_validation", rules)

    if LOCAL_ONLY:
        print("LOCAL_ONLY: skipped WordPress publish (set BS_PUBLISH=1 to publish)")
        return

    post = api(
        "POST",
        "posts",
        {
            "title": TITLE,
            "slug": SLUG,
            "status": "publish",
            "author": 270271338,
            "categories": [CAT_FESTIVE, CAT_QUOTES],
            "content": content,
            "excerpt": META_DESC,
            "meta": {
                "_yoast_wpseo_focuskw": FOCUS_KW,
                "_yoast_wpseo_title": YOAST_TITLE,
                "_yoast_wpseo_metadesc": META_DESC,
            },
        },
    )
    print("published new post", post["id"], post["link"])

    manifest_path = ROOT / "output/Week1_Rank30_AkshayaQuotes_type3_prompts.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["wp_post_id"] = post["id"]
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
