#!/usr/bin/env python3
"""Publish/Optimize Week 1 Rank 8: Xmas Wishes & Quotes (WP #16842)."""
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

POST_ID = 16842
TITLE = "100+ Merry Christmas Wishes, Quotes & Xmas Messages for 2026"
SLUG = "xmas-wishes-quotes"
META_DESC = (
    "Find 100+ Merry Christmas wishes, quotes and Xmas messages for 2026. "
    "Perfect for friends, family, partners, Instagram captions, WhatsApp status and cards. Ready to share."
)
FOCUS_KW = "xmas wishes quotes"
YOAST_TITLE = "Merry Christmas Wishes, Quotes & Xmas Messages 2026 | BlueStone"
LIVE_URL = f"https://blog.bluestone.com/{SLUG}/"

PRODUCTS = [
    {
        "code": "BISW1080P28",
        "name": "The Thyvarne Pendant",
        "url": "https://www.bluestone.com/pendants/the-thyvarne-pendant~173761.html",
        "png": ROOT / "ProductImages/seo images/Pendants/The Thyvarne Pendant.png",
    },
    {
        "code": "BIHS1145P21",
        "name": "The Valeria Rose Pendant",
        "url": "https://www.bluestone.com/pendants/the-valeria-rose-pendant~181266.html",
        "png": ROOT / "ProductImages/seo images/Pendants/The Valeria Rose Pendant.png",
    },
    {
        "code": "BISW1080P32",
        "name": "The Teshvarya Pendant",
        "url": "https://www.bluestone.com/pendants/the-teshvarya-pendant~173771.html",
        "png": ROOT / "ProductImages/seo images/Pendants/The Teshvarya Pendant.png",
    },
    {
        "code": "BIPM0001H28",
        "name": "The Rohal Huggie Earrings",
        "url": "https://www.bluestone.com/earrings/the-rohal-huggie-earrings~21864.html",
        "png": ROOT / "ProductImages/seo images/Earrings/The Rohal Huggie Earrings.png",
    },
    {
        "code": "BIIP0279S08",
        "name": "The Aleena Huggie Earrings",
        "url": "https://www.bluestone.com/earrings/the-aleena-huggie-earrings~16735.html",
        "png": ROOT / "ProductImages/seo images/Earrings/The Aleena Huggie Earrings.png",
    },
    {
        "code": "BISA0255D05",
        "name": "The Asya Huggie Earrings",
        "url": "https://www.bluestone.com/earrings/the-asya-huggie-earrings~13494.html",
        "png": ROOT / "ProductImages/seo images/Earrings/The Asya Huggie Earrings.png",
    },
]

SECTIONS = {
    "short_quotes": [
        "May the peace and joy of Christmas live in your heart throughout the coming year.",
        "Xmas is a necessity, there has to be at least one day of the year to remind us that we are here for something else.",
        "The best of all gifts around any Christmas tree is the presence of a happy family.",
        "Christmas is not a time nor a season, but a state of mind.",
        "Peace on earth will come to stay, when we live Christmas every day.",
        "Let the warmth of the holiday season fill your home with confidence and hope.",
        "Xmas wishes bring us closer, even when we are miles apart.",
        "A quiet Christmas is a beautiful chance to reflect on our blessings.",
        "May the light of the Christmas star guide your family toward peace and progress.",
        "Christmas waves a magic wand over this world, and behold, everything is softer and more beautiful.",
        "Grateful for the past, hopeful for the future, happy Christmas 2026.",
        "Let us keep Christmas in our hearts, today and every day.",
    ],
    "wishes": [
        "Wishing you and your family a peaceful, healthy, and happy Christmas 2026.",
        "May your holiday season be wrapped in joy and filled with laughter.",
        "Sending warm wishes for a Merry Christmas and a wonderful year ahead.",
        "May the magic of Christmas bring peace to your mind and joy to your home.",
        "Wishing you a beautiful holiday season surrounded by the people you love.",
        "May this Christmas bring new opportunities, fresh hopes, and quiet strength.",
        "Warmest thoughts and best wishes for a wonderful Christmas and a successful New Year.",
        "So grateful to have you in my life, wishing you a happy and peaceful Christmas.",
        "May the festive spirit fill your home with warmth and togetherness.",
        "Wishing you a Merry Christmas filled with sweet memories and shared pride.",
        "May your holidays be bright, peaceful, and filled with gratitude. Jai Hind!",
    ],
    "family": [
        "To my wonderful family, thank you for making every Christmas feel like home.",
        "May this Christmas bring our family closer together as we celebrate our shared blessings.",
        "Wishing my parents a peaceful and happy Christmas filled with warmth and rest.",
        "To my siblings, so grateful for the childhood memories and the future we are building.",
        "May our home be filled with laughter, love, and sweet festive aromas this Christmas.",
        "Wishing you all a memorable Christmas, missing you and sending love from afar.",
        "May the holiday season bring peace, health, and happiness to every member of our family.",
        "Grateful for the traditions we share and the quiet moments together. Happy Christmas!",
    ],
    "romantic": [
        "You are my favorite Christmas gift, today and every day. Happy Christmas, my love.",
        "Thank you for filling my life with warmth, love, and laughter. Merry Christmas!",
        "Wishing my partner a beautiful Christmas, so glad to share this life and this holiday with you.",
        "May our love grow stronger with every Christmas we celebrate together.",
        "Holding your hand is the best part of my holiday. Merry Christmas, sweetheart.",
        "You make every ordinary day feel festive. So happy to celebrate Christmas with you.",
        "Wishing you a bright Christmas and a future filled with shared dreams, my love.",
    ],
    "funny": [
        "Merry Christmas! May your family drama be minimal and your presents be plentiful.",
        "Congratulations on surviving another year of holiday shopping. Happy Christmas!",
        "Merry Christmas! I put so much thought into your gift that it's actually still in the store.",
        "Happy Christmas! May your holiday weight gain be temporary and your joy be permanent.",
        "Merry Christmas! May Santa bring you everything you asked for and forget what you did.",
        "Here's to a holiday season filled with eating, sleeping, and remote control sharing.",
        "Congratulations on officially qualifying for the holiday treat marathon. Happy Christmas!",
    ],
    "inspirational": [
        "May the message of Christmas fill your life with peace, hope, and determination.",
        "A stronger community begins with everyday choices of kindness and respect.",
        "Let the peace of the season inspire us to build a fairer and kinder tomorrow.",
        "The best tribute to the holiday spirit is a life lived with generosity and integrity.",
        "May your choices reflect hope, your actions reflect kindness, and your heart find peace.",
        "Progress is built on shared responsibility, may this Christmas bring us closer to that goal.",
        "Wishing you a Christmas that renews your confidence in yourself and your dreams.",
        "Let the lights of the tree remind us that even small actions can brighten the world.",
    ],
    "combo": [
        "Wishing you a Merry Christmas and a successful, healthy, and Happy New Year 2027.",
        "May the joy of Christmas stay with you as you step into a bright and hopeful New Year.",
        "Sending combined wishes for a wonderful holiday season and a prosperous year ahead.",
        "May your holidays be peaceful and your New Year be filled with fresh possibilities.",
        "Wishing you a Merry Christmas and a Happy New Year filled with blessings and growth.",
        "Let us celebrate the holidays with gratitude and welcome the New Year with courage. Jai Hind!",
        "Warm wishes for a Happy Christmas and a bright, successful 2027.",
    ],
    "captions": [
        "Warm lights, cozy nights, happy hearts. Jai Hind!",
        "Merry Christmas! Grateful for the magic and the memories.",
        "Cozy mood: on. Happy Christmas 2026!",
        "Choosing peace, hope, and gratitude this Christmas.",
        "Under the tree: love, laughter, and family. Merry Christmas!",
        "Xmas mood: grateful, peaceful, hopeful.",
        "May your holidays be as bright as a well-lit tree.",
        "Officially celebrating, and so happy about it.",
        "Two holidays, one promise, infinite joy.",
        "Here's to cozy sweaters, hot chocolate, and loved ones.",
        "A quiet Christmas, a bright tomorrow. Jai Hind!",
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
        alt = f"Christmas 2026 gift idea: {product['name']} from BlueStone"
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
    script = script.replace("bs-cf-eid", "bs-cf-christmas")
    return (
        "<!-- wp:html -->\n<style>\n"
        + style
        + '\n</style>\n<div class="bs-cf" id="bs-cf-christmas" data-interval="3200" aria-roledescription="carousel" aria-label="BlueStone Christmas gift ideas">\n'
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
            "What are the best Xmas wishes quotes for 2026?",
            "The best Xmas wishes quotes for 2026 focus on peace, hope, and gratitude. Try: “The best of all gifts around any Christmas tree is the presence of a happy family.” Sincere quotes work beautifully for card greetings and group messages.",
        ),
        (
            "What is a short Merry Christmas wish for WhatsApp?",
            "A short wish is: “Wishing you a season filled with warmth, joy, and shared laughter. Merry Christmas 2026!” It is concise, easy to copy, and fits on a single phone screen.",
        ),
        (
            "How do I write a combined Christmas and Happy New Year wish?",
            "A combined wish can be: “Wishing you a Merry Christmas and a successful, healthy, and Happy New Year 2027.” It covers both milestones naturally and works for personal and professional connections.",
        ),
        (
            "What is a thoughtful Christmas message for family?",
            "For family, try: “May this Christmas bring our family closer together as we celebrate our shared blessings.” Family wishes work best when they focus on gratitude, love, and home traditions.",
        ),
        (
            "What is a good Christmas caption for Instagram?",
            "A popular caption is: “Xmas mood: grateful, peaceful, hopeful.” Keeping captions brief allows the photo or story to occupy the main focus.",
        ),
        (
            "When should I send Merry Christmas and Happy New Year messages?",
            "Send them between December 20th and January 1st. Direct messages on Christmas Eve and Christmas Day work best for close connections, while combined holiday cards can be sent earlier.",
        ),
    ]
    html = [h2("Frequently Asked Questions about Xmas Wishes Quotes")]
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
            "Looking for the perfect <strong>xmas wishes quotes</strong>, Merry Christmas greetings, and holiday messages to share in 2026? "
            "Whether you need short quotes for cards, warm messages for friends and family, romantic lines, or captions for Instagram, this guide brings them together."
        ),
        para(
            "<strong>TL;DR:</strong> Choose a traditional wish for cards, a short status line for WhatsApp, a romantic message for your spouse, "
            "or a combined holiday wish that carries you into the New Year. Every list is updated for Christmas 2026."
        ),
        para(
            "Christmas is a time of joy, love, and connection. A thoughtful message goes a long way in showing care for the people in your life."
        ),
        h2("Short Xmas Wishes & Quotes"),
        para("These short Christmas quotes and sayings are perfect for cards, gift tags, or quick notes."),
        list_block(SECTIONS["short_quotes"]),
        h2("Merry Christmas Wishes for Friends & Loved Ones"),
        para("Share these warm happy Christmas wishes with the friends who make every season bright."),
        list_block(SECTIONS["wishes"]),
        h2("Christmas Greetings for Family"),
        para("Send these warm Christmas greetings to your family members to celebrate the season of togetherness."),
        list_block(SECTIONS["family"]),
        h2("Romantic Christmas Wishes for Partners"),
        para("These romantic Christmas messages help you share your love with your spouse or partner during the holiday season."),
        list_block(SECTIONS["romantic"]),
        h2("A Thoughtful Gift for the Holiday Season"),
        para(
            "If you are looking to pair your wishes with a keepsake, gold, diamond, gemstone, and pearl jewellery are classic choices. "
            "Choose a red ruby pendant or a green emerald huggie to coordinate with the festive theme, or pick a classic pearl drop hoop. "
            "Here are six approved festive design ideas from the BlueStone collection."
        ),
        carousel,
        h2("Funny Christmas Quotes & Messages"),
        para("Keep the holiday mood light and happy with these funny Christmas greetings."),
        list_block(SECTIONS["funny"]),
        h2("Inspirational Christmas Messages"),
        para("These thoughtful inspirational Christmas quotes focus on peace, responsibility, community, and fresh hopes."),
        list_block(SECTIONS["inspirational"]),
        h2("Combined Christmas and Happy New Year Wishes"),
        para("Send these double-milestone messages when you want to wish someone a Merry Christmas and a successful New Year."),
        list_block(SECTIONS["combo"]),
        h2("Christmas Captions for Instagram & WhatsApp Status"),
        para("Keep your holiday updates simple and scanable with these quick captions and status updates."),
        list_block(SECTIONS["captions"]),
        h2("More Festive Wishes to Explore"),
        para(
            'Keep celebrating with our other collections including <a href="https://blog.bluestone.com/happy-holi-wishes-messages-quotes-2027/">Holi wishes for 2027</a>, '
            '<a href="https://blog.bluestone.com/happy-diwali-wishes-messages-quotes-2026/">Diwali wishes for 2026</a>, '
            '<a href="https://blog.bluestone.com/happy-eid-mubarak-wishes-messages-quotes-2027/">Eid wishes for 2027</a>, '
            '<a href="https://blog.bluestone.com/happy-childrens-day-best-wishes-quotes-messages-for-kids/">Children\'s Day quotes for 2026</a>, and '
            '<a href="https://blog.bluestone.com/engagement-quotes/">engagement quotes for 2026</a>.'
        ),
        faq_html,
        h2("Conclusion"),
        para(
            "The best xmas wishes quotes are sincere, simple to share, and respectful of the season. "
            "Pick a line that fits your relationship, personalize it with a name or shared memory, and share the holiday spirit. Merry Christmas 2026!"
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
            "xmas wishes quotes",
            "merry christmas wishes 2021",
            "christmas and happy new year wishes",
            "christmas wishes and new year wishes",
            "christmas and new year wishes",
            "great christmas wishes",
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
        "carousel_mid_article": content.index("bs-cf-christmas") < content.index("Frequently Asked Questions"),
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
    assets = ROOT / "output/Week1_Rank8_ChristmasWishes_assets"
    assets.mkdir(parents=True, exist_ok=True)

    product_media = []
    for product in PRODUCTS:
        if not product["png"].exists():
            raise SystemExit(f"Missing approved Type 2 image: {product['png']}")
        filename = re.sub(r"[^A-Za-z0-9]+", "-", product["name"]).strip("-").lower() + "-carousel.webp"
        webp = assets / filename
        to_carousel_webp(product["png"], webp)
        alt = f"Christmas 2026 gift idea: {product['name']} from BlueStone"
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
    (ROOT / "output/Week1_Rank8_ChristmasWishes_article.html").write_text(content)
    (ROOT / "output/Week1_Rank8_ChristmasWishes_product_media.json").write_text(
        json.dumps(product_media, indent=2)
    )

    # Post to WP under ID 16842 and slug xmas-wishes-quotes (Optimize flow)
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
