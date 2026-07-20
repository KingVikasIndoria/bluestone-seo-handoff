#!/usr/bin/env python3
"""Optimize Week 1 Rank 18: Appreciation Happy Men's Day Quotes (WP #16212)."""
import base64
import json
import os
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]


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

POST_ID = 16212
TITLE = "100+ Appreciation Happy Men's Day Quotes, Wishes & Messages for 2026"
SLUG = "happy-international-mens-day-best-quotes-wishes-messages"
META_DESC = (
    "Find 100+ appreciation happy men's day quotes, International Men's Day wishes, "
    "and happy mens day quotes for 2026. Ready to copy for WhatsApp, cards and Instagram."
)
FOCUS_KW = "appreciation happy men's day quotes"
YOAST_TITLE = "Appreciation Happy Men's Day Quotes & Wishes 2026 | BlueStone"
LIVE_URL = f"https://blog.bluestone.com/{SLUG}/"

PRODUCTS = [
    {
        "code": "BISL0851R28",
        "name": "The Jasper Band For Him",
        "url": "https://www.bluestone.com/rings/the-jasper-band-for-him~93964.html",
        "png": ROOT / "ProductImages/seo images/Rings/The Jasper Band For Him.png",
    },
    {
        "code": "BISL1006V287",
        "name": "The Volara Bracelet For Him",
        "url": "https://www.bluestone.com/bracelets/the-volara-bracelet-for-him~163432.html",
        "png": ROOT / "ProductImages/seo images/Bracelet/The Volara Bracelet For Him.png",
    },
    {
        "code": "BVEM0663C88",
        "name": "The Tetyana Gold Chain",
        "url": "https://www.bluestone.com/chains/the-tetyana-gold-chain~124927.html",
        "png": ROOT / "ProductImages/seo images/Chains/The Tetyana Gold Chain.png",
    },
    {
        "code": "BISV0910V22",
        "name": "The Concatenate Bracelet For Him",
        "url": "https://www.bluestone.com/bracelets/the-concatenate-bracelet-for-him~109542.html",
        "png": ROOT / "ProductImages/seo images/Bracelet/The Concatenate Bracelet For Him.png",
    },
    {
        "code": "BISV0910R24",
        "name": "The Interlink Band Ring",
        "url": "https://www.bluestone.com/rings/the-interlink-band-ring~108785.html",
        "png": ROOT / "ProductImages/seo images/Rings/The Interlink Band Ring.png",
    },
    {
        "code": "BIPO0945V21",
        "name": "The Amandine Bracelet For Him",
        "url": "https://www.bluestone.com/bracelets/the-amandine-bracelet-for-him~111826.html",
        "png": ROOT / "ProductImages/seo images/Bracelet/The Amandine Bracelet For Him.png",
    },
]

SECTIONS = {
    "appreciation": [
        "Happy Men's Day to the man who shows up with patience, honesty, and quiet strength every day.",
        "Appreciation happy men's day quotes start here: thank you for the care you give without asking for applause.",
        "To the men who lead with kindness, Happy International Men's Day. Your calm courage matters.",
        "Today we celebrate the men who listen, protect, and lift others without making it about themselves.",
        "Happy Men's Day. Grateful for the men who make home feel safer and life feel steadier.",
        "Appreciation note for Men's Day: your hard work, soft heart, and steady support never go unnoticed.",
        "Happy International Men's Day to every man learning, growing, and choosing respect every day.",
        "To the men who carry responsibility with grace: today is for you. Happy Men's Day 2026.",
    ],
    "wishes": [
        "Happy International Men's Day! Wishing you strength, peace, and a day that feels truly yours.",
        "Sending warm mens day wishes to the men who make ordinary days better for everyone around them.",
        "Happy Men's Day 2026. May you feel seen, valued, and celebrated for who you are.",
        "Wishing you a Happy International Men's Day filled with rest, respect, and good company.",
        "Happy mens day wishes to my favourite man: thank you for being both strong and kind.",
        "On International Men's Day, may your health stay strong and your heart stay light.",
        "Happy Men's Day! You deserve appreciation not only today, but in every quiet moment of the year.",
        "Warm wishes on Happy International Men's Day. Keep shining in your own honest way.",
    ],
    "quotes": [
        "A real man is not defined by silence. He is defined by the care he chooses to give.",
        "Happy men's day quote: strength looks beautiful when it protects someone else's peace.",
        "International Men's Day quote: the best men make room for feelings, fairness, and growth.",
        "Masculinity is not hardness. It is responsibility worn with warmth.",
        "Happy mens day quotes should sound true: thank you for being reliable when it was hard.",
        "The measure of a man is how gently he treats the people who need him.",
        "On Men's Day we celebrate courage that includes kindness, not courage that erases it.",
        "A good man leaves people feeling safer after he walks into the room.",
    ],
    "dad": [
        "Happy Men's Day, Dad. Thank you for every lesson wrapped in love and quiet protection.",
        "To my father: your steady presence is my first example of strength. Happy International Men's Day.",
        "Dad, today I celebrate the man who made sacrifice look like love. Happy Men's Day.",
        "Happy Men's Day to the father who taught me courage without raising his voice.",
    ],
    "husband": [
        "Happy Men's Day to my husband: thank you for partnership, patience, and everyday loyalty.",
        "To my hubby on International Men's Day: you are my calm, my teammate, and my favourite person.",
        "Happy Men's Day, love. Grateful for the way you show up for our home and our future.",
        "Husband, your quiet support is the loudest love I know. Happy International Men's Day.",
    ],
    "brother_friend": [
        "Happy Men's Day to my brother: thank you for loyalty that never needed a stage.",
        "To my best friend: Happy International Men's Day. Grateful for the laughs and the real talks.",
        "Happy Men's Day, brother. You make family feel lighter and stronger at the same time.",
        "To the friend who stays: Happy mens day wishes and endless respect.",
    ],
    "captions": [
        "Men's Day caption: Soft heart. Strong values. Happy International Men's Day.",
        "Status idea: Celebrating the men who lead with kindness.",
        "Instagram line: Appreciation looks good on you. Happy Men's Day 2026.",
        "Caption for him: Quiet strength, loud impact. Happy International Men's Day.",
        "WhatsApp status: Today we thank the men who make life feel safer.",
        "Reel text: Respect, rest, and real appreciation. Happy Men's Day.",
    ],
    "funny": [
        "Happy Men's Day! Thanks for fixing things you secretly broke first.",
        "To the men who claim they do not need compliments: here is a full page anyway.",
        "Happy International Men's Day. Remote in one hand, big heart in the other.",
        "Men's Day wish: may your WiFi stay strong and your snacks stay untouched.",
    ],
    "short": [
        "Happy Men's Day. You are appreciated.",
        "Happy International Men's Day 2026. Thank you for being you.",
        "Proud of you. Happy Men's Day!",
        "Strength + kindness = you. Happy Men's Day.",
        "Feeling grateful for you today. Happy International Men's Day.",
        "You matter. Happy Men's Day 2026.",
    ],
}


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


def upload_media(path: Path, alt: str):
    headers = {
        "Content-Disposition": f'attachment; filename="{path.name}"',
        "Content-Type": "image/webp",
    }
    media = api("POST", "media", raw_body=path.read_bytes(), headers=headers)
    api("POST", f"media/{media['id']}", {"alt_text": alt, "title": path.stem})
    return media


def h2(text):
    return f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{escape(text)}</h2>\n<!-- /wp:heading -->'


def h3(text):
    return f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{escape(text)}</h3>\n<!-- /wp:heading -->'


def para(text, align=None):
    if align:
        return f'<!-- wp:paragraph {{"align":"{align}"}} -->\n<p class="has-text-align-{align}">{text}</p>\n<!-- /wp:paragraph -->'
    return f'<!-- wp:paragraph -->\n<p>{text}</p>\n<!-- /wp:paragraph -->'


def list_block(items, ordered=True):
    tag = "ol" if ordered else "ul"
    attrs = ' {"ordered":true}' if ordered else ""
    lines = [f"<!-- wp:list{attrs} -->", f'<{tag} class="wp-block-list">']
    lines.extend(f"<li>{escape(item)}</li>" for item in items)
    lines.extend([f"</{tag}>", "<!-- /wp:list -->"])
    return "\n".join(lines)


def build_carousel(product_media):
    cards = []
    dots = []
    for index, product in enumerate(product_media):
        alt = f"International Men's Day 2026 gift idea: {product['name']} from BlueStone"
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
    script = script.replace("bs-cf-eid", "bs-cf-mensday")
    return (
        "<!-- wp:html -->\n<style>\n"
        + style
        + '\n</style>\n<div class="bs-cf" id="bs-cf-mensday" data-interval="3200" aria-roledescription="carousel" aria-label="BlueStone Men\'s Day gift ideas for him">\n'
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
    faqs = [
        (
            "What are the best appreciation happy men's day quotes?",
            "The best appreciation happy men's day quotes are sincere and specific: "
            "“Happy Men's Day to the man who shows up with patience, honesty, and quiet strength every day.” "
            "Add one personal detail to make it land better.",
        ),
        (
            "What are good Happy International Men's Day wishes?",
            "Try: “Happy International Men's Day! Wishing you strength, peace, and a day that feels truly yours.” "
            "These mens day wishes work for WhatsApp and cards.",
        ),
        (
            "Can you share a happy men's day quote for Instagram?",
            "Use: “Happy men's day quote: strength looks beautiful when it protects someone else's peace.” "
            "Keep the caption short and pair it with a warm photo.",
        ),
        (
            "What should I write for my husband on Men's Day?",
            "Write: “Happy Men's Day to my husband: thank you for partnership, patience, and everyday loyalty.” "
            "Husband messages feel best when they mention one daily habit you appreciate.",
        ),
        (
            "Are short Happy Men's Day messages okay for WhatsApp?",
            "Yes. Short lines like “Happy Men's Day. You are appreciated.” are perfect for busy chats and status updates.",
        ),
        (
            "What is a thoughtful Men's Day gift idea for him from BlueStone?",
            "Gold chains, band rings, and bracelets for him such as The Tetyana Gold Chain, "
            "The Jasper Band For Him, or The Volara Bracelet For Him make lasting appreciation gifts.",
        ),
    ]
    html = [h2("Frequently Asked Questions about Happy Men's Day Quotes")]
    schema = []
    for question, answer in faqs:
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
            "Looking for the best <strong>appreciation happy men's day quotes</strong>, "
            "Happy International Men's Day wishes, and happy mens day quotes to share? "
            "This collection covers appreciation lines, short WhatsApp notes, quotes for dad, husband, brother, and friends."
        ),
        para(
            "<strong>TL;DR:</strong> Copy an appreciation quote, a warm International Men's Day wish, "
            "a caption for Instagram, or a short message for WhatsApp. All lists are refreshed for Men's Day 2026."
        ),
        para(
            "International Men's Day is a chance to thank the men who lead with care, not only strength. "
            "A sincere message, and sometimes a lasting gift for him, can make that appreciation feel real."
        ),
        h2("Appreciation Happy Men's Day Quotes"),
        para("These appreciation happy men's day quotes celebrate kindness, responsibility, and quiet support."),
        list_block(SECTIONS["appreciation"]),
        h2("Happy International Men's Day Wishes"),
        para("Send these Happy International Men's Day wishes to the men you value."),
        list_block(SECTIONS["wishes"]),
        h2("Happy Men's Day Quotes & International Men's Day Quotes"),
        para("Thoughtful happy men's day quotes and International Men's Day quotes for cards and captions."),
        list_block(SECTIONS["quotes"]),
        h2("Men's Day Quotes for Dad"),
        para("Warm lines for fathers on Happy International Men's Day."),
        list_block(SECTIONS["dad"]),
        h2("Men's Day Wishes for Husband"),
        para("Personal messages for the man who shares your everyday life."),
        list_block(SECTIONS["husband"]),
        h2("A Soft Men's Day Gift Idea for Him"),
        para(
            "If you are gifting too, International Men's Day is a beautiful time to mark appreciation with something lasting. "
            "Gold chains, band rings, and bracelets for him make thoughtful keepsakes beyond a quick text. "
            "Explore these six approved designs from the BlueStone collection."
        ),
        carousel,
        h2("Men's Day Captions for Instagram & Status"),
        para("Pair these captions with a favourite photo of him."),
        list_block(SECTIONS["captions"], ordered=False),
        h2("Men's Day Wishes for Brother & Friends"),
        para("Appreciation lines for brothers and the friends who feel like family."),
        list_block(SECTIONS["brother_friend"]),
        h2("Funny Happy Men's Day Wishes"),
        para("Light lines for men who prefer humour with their compliments."),
        list_block(SECTIONS["funny"]),
        h2("Short Happy Men's Day Messages for WhatsApp"),
        para("Quick copy-ready notes for busy chats."),
        list_block(SECTIONS["short"]),
        h2("More Festive & Occasion Reads"),
        para(
            'Explore our other guides including <a href="https://blog.bluestone.com/happy-fathers-day-wishes-quotes-and-messages-for-every-dad/">Father\'s Day quotes for 2026</a>, '
            '<a href="https://blog.bluestone.com/romantic-valentines-day-wishes-quotes-celebrate-love-in-the-most-beautiful-way/">Valentine\'s hubby quotes for 2027</a>, '
            '<a href="https://blog.bluestone.com/26-january-republic-day-wishes-quotes-patriotic-messages/">Republic Day wishes for 2027</a>, '
            '<a href="https://blog.bluestone.com/friendship-day-2023-wishes/">Friendship Day wishes for 2026</a>, '
            '<a href="https://blog.bluestone.com/bhai-dooj-wishes/">Bhai Dooj wishes for 2026</a>, and '
            '<a href="https://blog.bluestone.com/raksha-bandhan-quotes-in-english/">Raksha Bandhan quotes for 2026</a>. '
            'Learn more about <a href="https://en.wikipedia.org/wiki/International_Men%27s_Day">International Men\'s Day on Wikipedia</a>.'
        ),
        faq_html,
        h2("Conclusion"),
        para(
            "The best appreciation happy men's day quotes keep gratitude simple and sincere. "
            "Pick a line that fits the man you are celebrating, personalize it, and share it with warmth. "
            "Happy International Men's Day 2026!"
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
        "datePublished": "2024-11-10",
        "dateModified": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "author": {"@type": "Person", "name": "Vikas"},
        "publisher": {"@type": "Organization", "name": "BlueStone", "url": "https://www.bluestone.com/"},
        "image": images,
        "mainEntityOfPage": {"@type": "WebPage", "@id": LIVE_URL},
        "keywords": [
            "appreciation happy men's day quotes",
            "happy international men's day",
            "mens day wishes",
            "international men's day quote",
            "men's day wishes",
            "happy men's day quote",
            "happy international men's day wishes",
            "happy mens day quotes",
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
    rules = {
        "no_em_dash": "—" not in visible,
        "no_en_dash": "–" not in visible,
        "no_spaced_hyphen": re.search(r"\s-\s", visible) is None,
        "no_prices": not re.search(r"(?:₹|Rs\.?\s*\d|INR\s*\d)", visible, re.I),
        "no_last_updated": "Last updated" not in visible,
        "carousel_mid_article": content.index("bs-cf-mensday") < content.index("Frequently Asked Questions"),
        "six_buy_links": content.count(">Buy now<") == 6,
        "faq_schema": '"@type": "FAQPage"' in content,
        "blog_schema": '"@type": "BlogPosting"' in content,
        "no_content_h1": "<h1" not in content.lower(),
    }
    failed = [name for name, passed in rules.items() if not passed]
    if failed:
        raise SystemExit(f"Content validation failed: {failed}")
    return rules


def main():
    assets = ROOT / "output/Week1_Rank18_MensDay_assets"
    assets.mkdir(parents=True, exist_ok=True)

    product_media = []
    for product in PRODUCTS:
        if not product["png"].exists():
            raise SystemExit(f"Missing SEO Type 2 image: {product['png']}")
        filename = re.sub(r"[^A-Za-z0-9]+", "-", product["name"]).strip("-").lower() + "-carousel-seo.webp"
        webp = assets / filename
        to_carousel_webp(product["png"], webp)
        alt = f"International Men's Day 2026 gift idea: {product['name']} from BlueStone"
        media = upload_media(webp, alt)
        product_media.append(
            {
                "code": product["code"],
                "name": product["name"],
                "url": product["url"],
                "id": media["id"],
                "src": media["source_url"],
                "alt": alt,
            }
        )
        print("uploaded product", product["code"], media["id"])

    carousel = build_carousel(product_media)
    content = build_content(carousel, product_media)
    rules = validate_content(content)
    (ROOT / "output/Week1_Rank18_MensDay_article.html").write_text(content)
    (ROOT / "output/Week1_Rank18_MensDay_product_media.json").write_text(json.dumps(product_media, indent=2))

    post = api(
        "POST",
        f"posts/{POST_ID}",
        {
            "title": TITLE,
            "slug": SLUG,
            "status": "publish",
            "author": 270271338,
            "content": content,
            "excerpt": META_DESC,
            "meta": {
                "_yoast_wpseo_focuskw": FOCUS_KW,
                "_yoast_wpseo_title": YOAST_TITLE,
                "_yoast_wpseo_metadesc": META_DESC,
            },
        },
    )
    print("optimized post", post["id"], post["link"])
    print("local_validation", rules)


if __name__ == "__main__":
    main()
