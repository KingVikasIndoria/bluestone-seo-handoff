#!/usr/bin/env python3
"""Publish/Optimize Week 1 Rank 12: Friendship Day Wishes (New post)."""
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

TITLE = "100+ Happy Friendship Day Wishes, Quotes & Messages in English for 2026"
SLUG = "friendship-day-2023-wishes"
META_DESC = (
    "Find 100+ Happy Friendship Day wishes, quotes and messages in English. "
    "Features best wishes for best friend, emotional friendship day quotes, school friends memories. Ready to copy."
)
FOCUS_KW = "friendship day 2023 wishes"
YOAST_TITLE = "Happy Friendship Day Wishes, Quotes & Messages | BlueStone"
LIVE_URL = f"https://blog.bluestone.com/{SLUG}/"

PRODUCTS = [
    {
        "code": "BIAR0097R07",
        "name": "The Liza ring",
        "url": "https://www.bluestone.com/rings/the-liza-ring~7623.html",
        "png": ROOT / "ProductImages/seo images/Rings/The Liza ring.png",
    },
    {
        "code": "BIAR0097R16",
        "name": "The Quinn Ring",
        "url": "https://www.bluestone.com/rings/the-quinn-ring~57845.html",
        "png": ROOT / "ProductImages/seo images/Rings/The Quinn Ring.png",
    },
    {
        "code": "BINS0639R18",
        "name": "The Gigi Ring",
        "url": "https://www.bluestone.com/rings/the-gigi-ring~64382.html",
        "png": ROOT / "ProductImages/seo images/Rings/The Gigi Ring.png",
    },
    {
        "code": "BIAB0503R03",
        "name": "The Rafia Ring",
        "url": "https://www.bluestone.com/rings/the-rafia-ring~53638.html",
        "png": ROOT / "ProductImages/seo images/Rings/The Rafia Ring.png",
    },
    {
        "code": "BIPM0017R18",
        "name": "The Malibu Ring",
        "url": "https://www.bluestone.com/rings/the-malibu-ring~2321.html",
        "png": ROOT / "ProductImages/seo images/Rings/The Malibu Ring.png",
    },
    {
        "code": "BISV0910R24",
        "name": "The Interlink Band Ring",
        "url": "https://www.bluestone.com/rings/the-interlink-band-ring~108785.html",
        "png": ROOT / "ProductImages/seo images/Rings/The Interlink Band Ring.png",
    },
]

SECTIONS = {
    "short": [
        "Wishing you a very Happy Friendship Day! Thank you for always being my constant anchor and support.",
        "To my dearest friend, may our bond grow stronger, brighter, and more peaceful with each passing year.",
        "Wishing you a beautiful and happy Friendship Day! Grateful for the daily laughs we share.",
        "May the light of our friendship continue to guide us through every challenge. Happy Friendship Day!",
        "Thank you for being the quiet strength and absolute clarity in my life. Happy Holiday!",
        "Warmest greetings on Friendship Day! Hoping your day is filled with sweet memories and rest.",
        "To the friend who knows me best and loves me anyway, wishing you a happy and peaceful day.",
        "May the circle of our trust remain unbroken forever. Happy Friendship Day!",
    ],
    "best_friends": [
        "To my best friend, thank you for listening to my stories with patience, loyalty, and daily kindness.",
        "Wishing my absolute best friend a very happy Friendship Day! You make every day a beautiful journey.",
        "Grateful for the day you walked into my life, bringing stability, happiness, and honest guidance.",
        "To the sibling of my choice, may our daily connection remain a source of courage and peace.",
        "Sending sweet wishes and prayers for your health, happiness, and success. Happy Friendship Day!",
        "Thank you for standing by me in every difficulty, proving that true friendship has no limits.",
        "May our shared memories keep us close, and may we build many more beautiful moments together.",
        "To my rock and constant supporter, wishing you the happiest and most restful Friendship Day!",
    ],
    "quotes": [
        "A true friend is one who walks in when the rest of the world walks out. Happy Friendship Day!",
        "Friendship is born at that moment when one person says to another: 'What! You too? I thought I was the only one.'",
        "A single rose can be my garden... a single friend, my world.",
        "True friendship is a quiet agreement to support, guide, and trust each other through everything.",
        "A friend is someone who gives you total freedom to be yourself, offering constant shelter.",
        "May we always celebrate the rare and precious gift of understanding that true friends share.",
    ],
    "childhood": [
        "From school desks to life milestones, thank you for being my oldest and truest friend.",
        "Wishing my childhood best friend a happy Friendship Day! Grateful for the shared history and memories.",
        "To the one who remembers my childhood dreams, thank you for always keeping me grounded.",
        "May the innocence and joy of our school days continue to inspire our adult path. Happy Friendship Day!",
        "Hoping our bond outlasts every change, keeping the sweet memory of our youth alive daily.",
        "Sending warm wishes to the friend who has shared my laughter, tears, and classrooms. Jai Hind!",
    ],
    "funny": [
        "Happy Friendship Day! Thank you for keeping all my secrets (mostly because you forget them anyway).",
        "We are best friends because you are the only one who tolerates my daily drama with a smile.",
        "Wishing you a happy Friendship Day! May our friendship last until we are old and completely senile.",
        "Thanks for being the partner-in-crime who never lets me make bad choices alone. Cheers!",
        "To the friend who knows how crazy I am and still chooses to be seen in public with me, thank you.",
        "May we always remain close, if only because you know too much about me to ever let go.",
    ],
    "distance": [
        "Miles cannot weaken the promise of our bond. Sending a warm hug and happy Friendship Day wishes from afar.",
        "Though we are far apart, you are always close to my thoughts. Wishing you a happy and peaceful day.",
        "To my long-distance best friend, thank you for keeping our connection strong across every timezone.",
        "May the memories of our past gatherings bridge the distance between us today. Happy Friendship Day!",
        "Hoping to reunite soon, but until then, sending prayers for your safety, progress, and joy.",
        "No matter where life takes us, you will always remain my chosen sibling and constant anchor.",
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
        alt = f"Friendship Day 2026 gift idea: {product['name']} from BlueStone"
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
    script = script.replace("bs-cf-eid", "bs-cf-friendship")
    return (
        "<!-- wp:html -->\n<style>\n"
        + style
        + '\n</style>\n<div class="bs-cf" id="bs-cf-friendship" data-interval="3200" aria-roledescription="carousel" aria-label="BlueStone Friendship Day gift ideas">\n'
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
            "What are the best happy friendship day wishes for 2026?",
            "The best happy Friendship Day wishes focus on gratitude, loyalty, and daily support: “Wishing you a very Happy Friendship Day! Thank you for always being my constant anchor and support.” These greetings make beautiful card notes.",
        ),
        (
            "What are the most emotional friendship day quotes for a best friend?",
            "An emotional quote is: “A true friend is one who walks in when the rest of the world walks out.” These quotes are perfect for card headings and formal messages.",
        ),
        (
            "How do I write a short best wishes for best friend card?",
            "Keep card messages short and sweet: “Your lessons are the foundation of my success. Thank you for teaching us with patience, clarity, and daily kindness. Happy Friendship Day!”",
        ),
        (
            "What is a good caption for friendship day best friend quotes on Instagram?",
            "A popular caption is: “To the friend who knows how crazy I am and still chooses to be seen in public with me, thank you. Happy Friendship Day!”",
        ),
        (
            "How do I wish a long-distance best friend?",
            "Write: “Miles cannot weaken the promise of our bond. Sending a warm hug and happy Friendship Day wishes from afar.”",
        ),
        (
            "Can I gift a friendship ring for Friendship Day?",
            "Yes! Gold and diamond friendship rings like The Interlink Band Ring are beautiful, lasting symbols of a lifelong bond.",
        ),
    ]
    html = [h2("Frequently Asked Questions about Friendship Day Wishes")]
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
            "Looking for the best <strong>friendship day 2023 wishes</strong>, quotes, and messages to share with your chosen family? "
            "Whether you need short card messages, emotional quotes, childhood school memories, funny status lines, or long-distance greetings, this collection has it all."
        ),
        para(
            "<strong>TL;DR:</strong> Copy a quick wish for a card, an emotional quote for a text, a dedicated message for childhood friends, or a funny WhatsApp status. "
            "All lists are updated for Friendship Day 2026."
        ),
        para(
            "A best friend represents loyalty, shared laughter, and constant support. Sharing a sincere card message or ring keepsake is a beautiful way to mark this milestone."
        ),
        h2("Short & Sweet Friendship Day Wishes"),
        para("Keep your greetings direct and scanable with these quick, copy-ready wishes."),
        list_block(SECTIONS["short"]),
        h2("Heartfelt Wishes for Best Friends"),
        para("Send these warm, respectful wishes to your best friend to thank them for their daily guidance and trust."),
        list_block(SECTIONS["best_friends"]),
        h2("Emotional Friendship Day Quotes"),
        para("These emotional friendship day quotes and famous quotes celebrate the rare gift of understanding."),
        list_block(SECTIONS["quotes"]),
        h2("Childhood & School Friends Nostalgic Messages"),
        para("Reflect on your shared history, school days, and childhood memories with these nostalgic messages."),
        list_block(SECTIONS["childhood"]),
        h2("A Circle of Trust: Friendship Ring Gift Ideas"),
        para(
            "A ring is a beautiful symbol of eternity, trust, and protective bonds. "
            "If you are celebrating your best friend with a holiday keepsake, simple stackable rings or interlinking diamond bands make classic choices. "
            "Explore these six approved ring designs from the BlueStone collection."
        ),
        carousel,
        h2("Funny & Light-Hearted Friendship Messages"),
        para("Celebrate your shared inside jokes and humor with these funny friendship messages."),
        list_block(SECTIONS["funny"]),
        h2("Long-Distance Friendship Day Wishes"),
        para("Keep your long-distance best friend close with these warm wishes sent across every timezone."),
        list_block(SECTIONS["distance"]),
        h2("More Festive & Occasion Reads"),
        para(
            'Explore our other occasion guides including <a href="https://blog.bluestone.com/heart-touching-love-proposal-quotes-2027/">proposal quotes for 2027</a>, '
            '<a href="https://blog.bluestone.com/happy-holi-wishes-messages-quotes-2027/">Holi wishes for 2027</a>, '
            '<a href="https://blog.bluestone.com/happy-diwali-wishes-messages-quotes-2026/">Diwali wishes for 2026</a>, '
            '<a href="https://blog.bluestone.com/happy-eid-mubarak-wishes-messages-quotes-2027/">Eid wishes for 2027</a>, '
            '<a href="https://blog.bluestone.com/happy-childrens-day-best-wishes-quotes-messages-for-kids/">Children\'s Day quotes for 2026</a>, '
            '<a href="https://blog.bluestone.com/engagement-quotes/">engagement quotes for 2026</a>, '
            '<a href="https://blog.bluestone.com/teachers-day-wishes-in-english/">Teachers\' Day wishes for 2026</a>, and '
            '<a href="https://blog.bluestone.com/dussehra-wishes-in-english/">Dussehra wishes for 2026</a>.'
        ),
        faq_html,
        h2("Conclusion"),
        para(
            "The best friendship day 2023 wishes focus on gratitude, loyalty, and the shared circles of trust. "
            "Select a message that fits your friendship, customize it with a name or memory, and share it with love. Happy Friendship Day 2026!"
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
        "datePublished": "2026-07-16",
        "dateModified": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "author": {"@type": "Person", "name": "Vikas"},
        "publisher": {"@type": "Organization", "name": "BlueStone", "url": "https://www.bluestone.com/"},
        "image": images,
        "mainEntityOfPage": {"@type": "WebPage", "@id": LIVE_URL},
        "keywords": [
            "friendship day 2023 wishes",
            "emotional friendship day quotes",
            "best wishes for best friend",
            "happy friendship day 2024 wishes quotes",
            "friendship day quotes for best friend",
            "friendship day best friend quotes",
            "best friends friendship day quotes",
            "best friend quotes for friendship day",
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
        "year_2025_body_gone": "2025" not in visible,
        "carousel_mid_article": content.index("bs-cf-friendship") < content.index("Frequently Asked Questions"),
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
    assets = ROOT / "output/Week1_Rank12_FriendshipDay_assets"
    assets.mkdir(parents=True, exist_ok=True)

    product_media = []
    for product in PRODUCTS:
        if not product["png"].exists():
            raise SystemExit(f"Missing approved Type 2 image: {product['png']}")
        filename = re.sub(r"[^A-Za-z0-9]+", "-", product["name"]).strip("-").lower() + "-carousel.webp"
        webp = assets / filename
        to_carousel_webp(product["png"], webp)
        alt = f"Friendship Day 2026 gift idea: {product['name']} from BlueStone"
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
    (ROOT / "output/Week1_Rank12_FriendshipDay_article.html").write_text(content)
    (ROOT / "output/Week1_Rank12_FriendshipDay_product_media.json").write_text(
        json.dumps(product_media, indent=2)
    )

    # Post as published (New article flow)
    post = api(
        "POST",
        "posts",
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
    print("published new post", post["id"], post["link"])
    print("local_validation", rules)


if __name__ == "__main__":
    main()
