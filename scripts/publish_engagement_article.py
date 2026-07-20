#!/usr/bin/env python3
"""Publish Week 1 Rank 7: Engagement Quotes for 2026."""
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

TITLE = "100+ Engagement Quotes, Wishes & Captions for 2026"
SLUG = "engagement-quotes"
META_DESC = (
    "Find 100+ engagement quotes and wishes for 2026. Perfect for friends, couples, "
    "siblings, Instagram captions, WhatsApp status and card congratulations. Ready to share."
)
FOCUS_KW = "engagement quotes"
YOAST_TITLE = "Engagement Quotes, Wishes & Captions 2026 | BlueStone"
LIVE_URL = f"https://blog.bluestone.com/{SLUG}/"

PRODUCTS = [
    {
        "code": "BIAR0097R04",
        "name": "The Anya Ring",
        "url": "https://www.bluestone.com/rings/the-anya-ring~7515.html",
        "png": ROOT / "ProductImages/seo images/Rings/The Anya Ring.png",
    },
    {
        "code": "BIAR0097R07",
        "name": "The Liza Ring",
        "url": "https://www.bluestone.com/rings/the-liza-ring~7623.html",
        "png": ROOT / "ProductImages/seo images/Rings/The Liza ring.png",
    },
    {
        "code": "BINS0639R18",
        "name": "The Gigi Ring",
        "url": "https://www.bluestone.com/rings/the-gigi-ring~64382.html",
        "png": ROOT / "ProductImages/seo images/Rings/The Gigi Ring.png",
    },
    {
        "code": "BIPM0017R18",
        "name": "The Malibu Ring",
        "url": "https://www.bluestone.com/rings/the-malibu-ring~2321.html",
        "png": ROOT / "ProductImages/seo images/Rings/The Malibu Ring.png",
    },
    {
        "code": "BIKR0993R117",
        "name": "The Luvee Highway Ring",
        "url": "https://www.bluestone.com/rings/the-luvee-highway-ring~123242.html",
        "png": ROOT / "ProductImages/seo images/Rings/The Luvee Highway Ring.png",
    },
    {
        "code": "BISL0851R28",
        "name": "The Jasper Band For Him",
        "url": "https://www.bluestone.com/rings/the-jasper-band-for-him~93964.html",
        "png": ROOT / "ProductImages/seo images/Rings/The Jasper Band For Him.png",
    },
]

SECTIONS = {
    "short_quotes": [
        "A successful engagement begins with a shared promise and grows with daily respect.",
        "Commitment is the choice to write a story where two voices speak as one.",
        "An engagement ring is a quiet reminder that the best chapters are yet to come.",
        "Love is not just looking at each other, it is looking in the same direction.",
        "An engagement mark is a bridge from a beautiful history to a hopeful future.",
        "Two hearts, one decision, and a lifetime of shared laughter.",
        "The best thing to hold onto in life is each other.",
        "A promise made today is a foundation built for tomorrow.",
        "Love does not consist in gazing at each other, but in looking outward together in the same direction.",
        "An engagement is the beginning of a lifelong conversation.",
        "Two souls with but a single thought, two hearts that beat as one.",
        "To find someone who loves you for who you are is the ultimate blessing.",
    ],
    "wishes": [
        "Wishing you both a beautiful engagement filled with peace, hope, and laughter.",
        "May this new chapter bring you closer together with every passing day.",
        "Congratulations on finding the person you want to share all your tomorrows with.",
        "May your love continue to grow as you build a home and a life together.",
        "Sending warm wishes for a wonderful engagement and a happy life ahead.",
        "So happy to celebrate your decision to build a future together. Congratulations!",
        "May the bond you share today strengthen with every year that follows.",
        "Wishing you a lifetime of joy, understanding, and shared adventures. Happy engagement!",
        "May your commitment bring you peace of mind and confidence in the future.",
        "Here is to the beautiful couple, may your love shine brighter with every day.",
        "Wishing you a smooth journey as you plan your wedding and your future together.",
        "Congratulations on taking this beautiful step toward forever. Jai Hind!",
    ],
    "congratulations": [
        "Warmest congratulations on your engagement. May your future be bright and peaceful.",
        "It is a joy to see two wonderful people choose a shared path. Heartiest congratulations.",
        "May your commitment inspire others and bring your families closer together.",
        "Sending sincere congratulations on this meaningful milestone. Wishing you all the best.",
        "Wishing you both a happy engagement and a marriage built on friendship and respect.",
        "Congratulations! May your shared home become a sanctuary of love and understanding.",
        "So thrilled to hear the wonderful news. Wishing you both a lifetime of happiness.",
        "May your mutual respect and affection guide you through all of life's seasons.",
        "Sending love and congratulations as you celebrate this beautiful announcement.",
        "Wishing you a joyful ring ceremony and a calm path toward your wedding day.",
    ],
    "ring_ceremony": [
        "May the exchange of rings remind you of the quiet commitment you share today.",
        "A ring ceremony celebrates the choice to face life's adventure hand in hand.",
        "As you wear these rings, may you carry each other's hopes in your hearts.",
        "Wishing you a beautiful ring ceremony filled with family, friends, and warm memories.",
        "May the circle of the ring represent a promise with no end and a love with no conditions.",
        "Congratulations on your ring ceremony! May this exchange begin a lifetime of joy.",
        "May these rings shine as a symbol of unity, courage, and daily kindness.",
        "Sending warm wishes for your ring ceremony, may your commitment bring daily strength.",
        "Let the exchange of rings be a promise of respect, support, and mutual growth.",
        "Wishing you a memorable ring ceremony and a lifetime of shared dreams.",
    ],
    "siblings": [
        "To my wonderful sister, so happy to see you find a partner who values and respects you.",
        "To my brother, wishing you and your partner a life of shared laughter and confidence.",
        "Watching you take this step fills my heart with joy. Happy engagement, dear sister!",
        "Happy engagement, brother! May your home be filled with peace, love, and growth.",
        "So proud of the person you are, sister, and so glad to welcome a new member to our family.",
        "Wishing you both a beautiful journey ahead, brother. May your bond grow stronger daily.",
        "To my sister, may your engagement ring always remind you of the love that surrounds you.",
        "To my brother, sending love as you step into a beautiful future with your chosen partner.",
    ],
    "funny": [
        "Congratulations on officially signing up to listen to each other's stories forever.",
        "Happy engagement! May your wedding planning be short and your patience be long.",
        "Two less fish in the sea, but two very happy people on land. Congratulations!",
        "Congratulations on finding the one person you want to annoy for the rest of your life.",
        "Happy engagement! Now the real challenge begins, choosing the wedding menu.",
        "So glad you decided to go on this adventure together, mostly because you make a great team.",
        "Congratulations on your engagement! May your love survive the wedding budget talks.",
        "Happy engagement! Here is to a lifetime of sharing the remote and the chores.",
    ],
    "anniversary": [
        "Happy engagement anniversary! May the promise you made years ago keep growing.",
        "Wishing you both a happy engagement anniversary, reflecting on a beautiful journey.",
        "Happy anniversary! May the love that started with a ring keep building your home.",
        "To my spouse, happy engagement anniversary. Thank you for choosing a shared life with me.",
        "Wishing a wonderful couple a happy engagement anniversary. May your bond stay strong.",
        "Happy engagement anniversary to the couple who showed us what commitment looks like.",
        "Reflecting on the day you said yes, wishing you a happy engagement anniversary.",
        "Happy engagement anniversary! May your shared memories bring a smile today.",
    ],
    "captions": [
        "The start of our favorite chapter. Jai Hind!",
        "One promise, two rings, and a lifetime to go.",
        "He asked, and my heart had already said yes.",
        "Choosing a shared future. Happy engagement!",
        "Rings exchanged, promise made, forever begun.",
        "My favorite person, my lifetime commitment.",
        "The circle of the ring is a promise with no end.",
        "Officially off the market, and so happy about it.",
        "Two hands, one direction, infinite hopes.",
        "Here is to love, laughter, and wedding planning.",
        "A quiet promise, a bright future.",
        "Jai Hind to our next big adventure together.",
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
        alt = f"Engagement 2026 gift idea: {product['name']} from BlueStone"
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
    script = script.replace("bs-cf-eid", "bs-cf-engagement")
    return (
        "<!-- wp:html -->\n<style>\n"
        + style
        + '\n</style>\n<div class="bs-cf" id="bs-cf-engagement" data-interval="3200" aria-roledescription="carousel" aria-label="BlueStone Engagement gift ideas">\n'
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
            "What are the best engagement quotes for couples?",
            "The best engagement quotes for couples celebrate their decision to build a life together. Try: “An engagement ring is a quiet reminder that the best chapters are yet to come.” It highlights their shared promise and sets a hopeful tone for their upcoming journey.",
        ),
        (
            "What is a short happy engagement wish for WhatsApp?",
            "A short WhatsApp wish is: “Two rings, one promise, and a lifetime of shared laughter. Happy engagement!” It is concise, warm, and fits comfortably on a single phone screen, making it ideal for group messages or direct wishes.",
        ),
        (
            "How do I write a congratulations message for a ring ceremony?",
            "A ring ceremony congratulations message should focus on the commitment and the ceremony. For example: “Congratulations on your ring ceremony! May this exchange begin a lifetime of joy.” Keep the message focused on the couple and their mutual decision.",
        ),
        (
            "What is a unique engagement status for Instagram?",
            "A good status is: “One promise, two rings, and a lifetime to go.” Captions work best when they are short and direct, letting the couple's picture tell the main story.",
        ),
        (
            "How can I wish a happy engagement anniversary to my spouse?",
            "For a spouse, you can say: “To my spouse, happy engagement anniversary. Thank you for choosing a shared life with me.” It is personal and direct, celebrating the day you both agreed to take the next step together.",
        ),
        (
            "What is a warm engagement wish for a sibling?",
            "For a sibling, speak from the heart: “To my wonderful sister, so happy to see you find a partner who values and respects you.” Sibling wishes should feel personal and welcome the partner to the family.",
        ),
    ]
    html = [h2("Frequently Asked Questions about Engagement Quotes")]
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
            "Looking for the perfect <strong>engagement quotes</strong>, wishes, or captions to share in 2026? "
            "Whether you are wishing a close friend, a brother or sister, writing a card, or searching for an Instagram status, this collection has you covered."
        ),
        para(
            "<strong>TL;DR:</strong> Pick a short quote for a card, a simple wish for family and friends, "
            "a specialized message for a brother or sister, or a cute caption for Instagram. Every list is updated for 2026."
        ),
        para(
            "An engagement celebrates a shared promise. The best message is sincere, warm, and fits the couple's unique bond."
        ),
        h2("Short Engagement Quotes & Sayings"),
        para("These short engagement quotes are perfect for card openings, guest books, or elegant posts."),
        list_block(SECTIONS["short_quotes"]),
        h2("Happy Engagement Wishes for Friends & Couples"),
        para("Send these warm happy engagement wishes to celebrate a couple's exciting decision."),
        list_block(SECTIONS["wishes"]),
        h2("Congratulations Wishes for Engagement"),
        para("Formal congratulations wishes for engagement work beautifully in cards, wedding invitations, and letters."),
        list_block(SECTIONS["congratulations"]),
        h2("Ring Ceremony Wishes & Messages"),
        para("These ring ceremony wishes celebrate the exchange of bands and the formal promise of marriage."),
        list_block(SECTIONS["ring_ceremony"]),
        h2("A Thoughtful Gift for the Ring Ceremony"),
        para(
            "If you are pairing your congratulations with a keepsake, rings are the classic choice. "
            "Whether it is a diamond solitaire, a multi-stone band, or a plain gold comfort band, select something that fits their daily style. "
            "Here are six approved ring ideas from the BlueStone collection."
        ),
        carousel,
        h2("Engagement Wishes for Brother or Sister"),
        para("Wish your sister or brother a happy engagement with these sibling-focused messages."),
        list_block(SECTIONS["siblings"]),
        h2("Funny Engagement Quotes & Messages"),
        para("Add a lighthearted note to the celebration with these funny engagement quotes."),
        list_block(SECTIONS["funny"]),
        h2("Happy Engagement Anniversary Wishes"),
        para("Celebrate your own milestone or send happy engagement anniversary wishes to couples marking their promise anniversary."),
        list_block(SECTIONS["anniversary"]),
        h2("Engagement Captions for Instagram & WhatsApp Status"),
        para("Keep your announcement simple and sweet with these captions for Instagram and status updates."),
        list_block(SECTIONS["captions"]),
        h2("More Festive & Occasion Reads"),
        para(
            'Explore our other guides including <a href="https://blog.bluestone.com/heart-touching-love-proposal-quotes-2027/">proposal quotes for 2027</a>, '
            '<a href="https://blog.bluestone.com/happy-holi-wishes-messages-quotes-2027/">Holi wishes for 2027</a>, '
            '<a href="https://blog.bluestone.com/happy-diwali-wishes-messages-quotes-2026/">Diwali wishes for 2026</a>, '
            '<a href="https://blog.bluestone.com/happy-eid-mubarak-wishes-messages-quotes-2027/">Eid wishes for 2027</a>, and '
            '<a href="https://blog.bluestone.com/happy-childrens-day-best-wishes-quotes-messages-for-kids/">Children\'s Day quotes for 2026</a>.'
        ),
        faq_html,
        h2("Conclusion"),
        para(
            "The right engagement quotes are sincere, direct, and celebrate a promise with no end. "
            "Choose a message that fits your relationship, personalize it with a name or memory, and share it with love. Happy engagement 2026!"
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
            "engagement quotes",
            "happy engagement anniversary",
            "happy engagement wishes",
            "happy engagement",
            "ring ceremony wishes",
            "congratulations wishes for engagement",
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
        "carousel_mid_article": content.index("bs-cf-engagement") < content.index("Frequently Asked Questions"),
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
    assets = ROOT / "output/Week1_Rank7_EngagementQuotes_assets"
    assets.mkdir(parents=True, exist_ok=True)

    product_media = []
    for product in PRODUCTS:
        if not product["png"].exists():
            raise SystemExit(f"Missing approved Type 2 image: {product['png']}")
        filename = re.sub(r"[^A-Za-z0-9]+", "-", product["name"]).strip("-").lower() + "-carousel.webp"
        webp = assets / filename
        to_carousel_webp(product["png"], webp)
        alt = f"Engagement 2026 gift idea: {product['name']} from BlueStone"
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
    (ROOT / "output/Week1_Rank7_EngagementQuotes_article.html").write_text(content)
    (ROOT / "output/Week1_Rank7_EngagementQuotes_product_media.json").write_text(
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
