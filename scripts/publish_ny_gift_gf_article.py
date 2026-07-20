#!/usr/bin/env python3
"""Publish Week 1 Rank 27: New Year Gift for Girlfriend 2027 (New post)."""
import base64
import json
import os
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
CAT_FESTIVE = 554493477
CAT_QUOTES = 554493415


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
USER = os.environ["WP_USER"]
PWD = os.environ["WP_APP_PASSWORD"]
TOKEN = base64.b64encode(f"{USER}:{PWD}".encode()).decode()
AUTH = {"Authorization": f"Basic {TOKEN}", "User-Agent": "BluestoneSEO/1.0"}
API = "https://blog.bluestone.com/wp-json/wp/v2"

CONTENT_DATA = json.loads(
    (ROOT / "output/Week1_Rank27_NYGiftGF_sections.json").read_text(encoding="utf-8")
)
META = CONTENT_DATA["meta"]
TITLE = META["title"]
SLUG = META["slug"]
META_DESC = META["meta_desc"]
FOCUS_KW = META["focus_kw"]
YOAST_TITLE = META["yoast_title"]
LIVE_URL = f"https://blog.bluestone.com/{SLUG}/"
OCCASION_YEAR = "New Year 2027"
SECTIONS = CONTENT_DATA["sections"]
FAQS = CONTENT_DATA["faqs"]
INTRO = META.get("intro") or (
    "Looking for a thoughtful <strong>new year gift for girlfriend</strong> for New Year 2027? "
    "This jewellery gift guide gathers classic, minimal, statement, and romantic ideas she can wear all year."
)

PRODUCTS = [
    {
        "code": "BIHS1145P21",
        "name": "The Valeria Rose Pendant",
        "url": "https://www.bluestone.com/pendants/the-valeria-rose-pendant~181266.html",
        "png": ROOT / "ProductImages/seo images/Pendants/The Valeria Rose Pendant.png",
    },
    {
        "code": "BIAR0097R07",
        "name": "The Liza ring",
        "url": "https://www.bluestone.com/rings/the-liza-ring~7623.html",
        "png": ROOT / "ProductImages/seo images/Rings/The Liza ring.png",
    },
    {
        "code": "BIPM0001H28",
        "name": "The Rohal Huggie Earrings",
        "url": "https://www.bluestone.com/earrings/the-rohal-huggie-earrings~21864.html",
        "png": ROOT / "ProductImages/seo images/Earrings/The Rohal Huggie Earrings.png",
    },
    {
        "code": "BIMG0635V45",
        "name": "The Shining Star Bracelet",
        "url": "https://www.bluestone.com/bracelets/the-shining-star-bracelet~63731.html",
        "png": ROOT / "ProductImages/seo images/Bracelet/The Shining Star Bracelet.png",
    },
    {
        "code": "BINS0639R18",
        "name": "The Gigi Ring",
        "url": "https://www.bluestone.com/rings/the-gigi-ring~64382.html",
        "png": ROOT / "ProductImages/seo images/Rings/The Gigi Ring.png",
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
    return f"new year gift for girlfriend 2027 gift idea: {name}"


def product_title(name: str) -> str:
    return f"{name} carousel, {OCCASION_YEAR}"


def build_carousel(product_media):
    cards = []
    dots = []
    for index, product in enumerate(product_media):
        alt = product["alt"]
        cards.append(
            f'    <div class="bs-cf-card" data-i="{index}">\n'
            f'      <a class="bs-cf-media" href="{product["url"]}">\n'
            f'        <img src="{product["src"]}" alt="{escape(alt)}" width="960" height="535" loading="lazy" decoding="async"/>\n'
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
    script = script.replace("bs-cf-eid", "bs-cf-nygiftgf")
    return (
        "<!-- wp:html -->\n<style>\n"
        + style
        + '\n</style>\n<div class="bs-cf" id="bs-cf-nygiftgf" data-interval="3200" aria-roledescription="carousel" aria-label="BlueStone New Year gift ideas for girlfriend">\n'
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
    html = [h2("Frequently Asked Questions about New Year Gift for Girlfriend")]
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
    intro_html = INTRO if INTRO.strip().startswith("Looking") or "<strong>" in INTRO else escape(INTRO)
    if "<strong>" not in intro_html and "new year gift for girlfriend" in intro_html.lower():
        intro_html = re.sub(
            r"(?i)new year gift for girlfriend",
            "<strong>new year gift for girlfriend</strong>",
            intro_html,
            count=1,
        )
    parts = [
        '<!-- wp:html -->\n<style>\n.bs-eeat{margin:0 auto 1.25rem;max-width:720px;text-align:center;font-size:.95rem;color:#444;line-height:1.5}\n.bs-eeat strong{color:#111}\n.entry-content img,.wp-block-image img{max-width:100%;height:auto}\n</style>\n<!-- /wp:html -->',
        '<!-- wp:paragraph {"align":"center"} -->\n<p class="has-text-align-center bs-eeat">By <strong>Vikas</strong>, BlueStone Editorial</p>\n<!-- /wp:paragraph -->',
        para(intro_html),
        para(
            "<strong>TL;DR:</strong> Match her everyday style first, then pick classic, minimal, statement, or romantic jewellery. "
            "Use the carousel below for six ready new year gift for girlfriend ideas for 2027."
        ),
        h2("Classic New Year Gift for Girlfriend Ideas"),
        para("Choose these timeless looks when she loves polished, elegant jewellery that never feels trendy for one season only."),
        list_block(SECTIONS["style_classic"]),
        h2("Minimal New Year Gift for GF Ideas"),
        para("If she prefers quiet sparkle, these minimal new year gift for gf picks stay light, stackable, and easy for daily wear."),
        list_block(SECTIONS["style_minimal"]),
        h2("Statement Jewellery She Will Remember"),
        para("Go bolder when she enjoys colour, larger silhouettes, or a piece that makes an entrance at New Year 2027 celebrations."),
        list_block(SECTIONS["style_statement"]),
        h2("Shop Ready New Year Gift Ideas"),
        para(
            "Browse these six approved BlueStone designs when you want a concrete new year gift for girlfriend shortlist. "
            "Pendants, rings, earrings, and bracelets cover romantic, everyday, and festive moods without price talk."
        ),
        carousel,
        h2("Everyday Wear Gifts She Can Reach for Daily"),
        para("The best new year gift for girlfriend ideas often win after December: pieces she actually wears to work, brunch, and travel."),
        list_block(SECTIONS["everyday_wear"]),
        h2("Romantic and Symbolic Jewellery Gifts"),
        para("Pick heart motifs, paired meanings, and soft romantic shapes when you want the gift to speak for your New Year 2027 promise."),
        list_block(SECTIONS["romantic_symbolic"]),
        h2("How to Choose the Right New Year Gift for Girlfriend"),
        para("Use this checklist before you buy so the piece feels chosen for her, not chosen in a rush."),
        list_block(SECTIONS["how_to_choose"]),
        h2("Gifting Tips for New Year 2027"),
        para("Presentation and timing matter as much as the design. Keep the reveal warm, private, and personal."),
        list_block(SECTIONS["gifting_tips"]),
        h2("More Festive and Occasion Reads"),
        para(
            'Explore our other guides including <a href="https://blog.bluestone.com/happy-new-year-wishes-for-love-2027/">Happy New Year wishes for love 2027</a>, '
            '<a href="https://blog.bluestone.com/gudi-padwa-meaning-2027/">Gudi Padwa meaning 2027</a>, '
            '<a href="https://blog.bluestone.com/mothers-day-wishes-in-english-2027/">Mother\'s Day wishes in English 2027</a>, '
            '<a href="https://blog.bluestone.com/happy-holi-wishes-messages-quotes-2027/">Holi wishes for 2027</a>, and '
            '<a href="https://blog.bluestone.com/happy-diwali-wishes-messages-quotes-2026/">Diwali wishes for 2026</a>.'
        ),
        faq_html,
        h2("Conclusion"),
        para(
            "A great new year gift for girlfriend for 2027 feels like her style, not a generic festival basket. "
            "Choose classic, minimal, statement, or romantic jewellery she will wear past midnight, and let the year begin with something lasting."
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
            "new year gift for girlfriend",
            "new year gift for girlfriend ideas",
            "new year gift for gf",
            "new year jewellery gift",
            "new year gift 2027",
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
        "carousel_mid_article": content.index("bs-cf-nygiftgf") < content.index("Frequently Asked Questions"),
        "six_buy_links": content.count(">Buy now<") == 6,
        "faq_schema": '"@type": "FAQPage"' in content,
        "blog_schema": '"@type": "BlogPosting"' in content,
        "no_content_h1": "<h1" not in content.lower(),
        "year_2027": "2027" in visible,
        "primary_kw": "new year gift for girlfriend" in visible.lower(),
        "no_old_years_body": not re.search(r"\b(2021|2022|2023|2024|2025)\b", body_no_links),
        "meta_title_len": len(YOAST_TITLE) <= 60,
        "meta_desc_len": 150 <= len(META_DESC) <= 160,
        "gift_sections": all(k in SECTIONS for k in ["style_classic", "style_minimal", "romantic_symbolic"]),
    }
    failed = [name for name, passed in rules.items() if not passed]
    if failed:
        raise SystemExit(f"Content validation failed: {failed}")
    return rules


def main():
    assert 150 <= len(META_DESC) <= 160, len(META_DESC)
    assert len(YOAST_TITLE) <= 60, len(YOAST_TITLE)
    assets = ROOT / "output/Week1_Rank27_NYGiftGF_assets"
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
        print("uploaded product", product["code"], media["id"])
    carousel = build_carousel(product_media)
    content = build_content(carousel, product_media)
    rules = validate_content(content)
    (ROOT / "output/Week1_Rank27_NYGiftGF_article.html").write_text(content, encoding="utf-8")
    (ROOT / "output/Week1_Rank27_NYGiftGF_product_media.json").write_text(
        json.dumps(product_media, indent=2), encoding="utf-8"
    )
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
    print("local_validation", rules)
    manifest_path = ROOT / "output/Week1_Rank27_NYGiftGF_type3_prompts.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["wp_post_id"] = post["id"]
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
