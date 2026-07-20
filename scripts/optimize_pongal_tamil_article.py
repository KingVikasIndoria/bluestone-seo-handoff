#!/usr/bin/env python3
"""Optimize Week 1 Rank 19: Creative Pongal Wishes in Tamil (WP #17858)."""
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

POST_ID = 17858
TITLE = "75+ Creative Pongal Wishes in Tamil for 2027 | Pongal Valthukkal"
SLUG = "makar-sankranti-quotes-wishes-pongal-and-magh-bihu-festival-greetings"
META_DESC = (
    "Find 75+ creative Pongal wishes in Tamil for 2027, happy Pongal wishes in Tamil, "
    "pongal valthukkal, and WhatsApp Tamil greetings ready to copy."
)
FOCUS_KW = "creative pongal wishes in tamil"
YOAST_TITLE = "Creative Pongal Wishes in Tamil 2027 | Pongal Valthukkal | BlueStone"
LIVE_URL = f"https://blog.bluestone.com/{SLUG}/"

PRODUCTS = [
    {
        "code": "BVPJ0935C06",
        "name": "The Shubhlatika Mangalsutra Necklace",
        "url": "https://www.bluestone.com/mangalsutra+chains/the-shubhlatika-mangalsutra-necklace~146084.html",
        "png": ROOT / "ProductImages/seo images/Mangalsutra Chains/The Shubhlatika Mangalsutra Necklace.png",
    },
    {
        "code": "BIDG0393O37",
        "name": "The Estrella Oval Bangle",
        "url": "https://www.bluestone.com/bangles/the-estrella-oval-bangle~34771.html",
        "png": ROOT / "ProductImages/seo images/Bangles/The Estrella Oval Bangle.png",
    },
    {
        "code": "BISP0427H21",
        "name": "The Ursa Hoop Earrings",
        "url": "https://www.bluestone.com/earrings/the-ursa-hoop-earrings~35069.html",
        "png": ROOT / "ProductImages/seo images/Earrings/The Ursa Hoop Earrings.png",
    },
    {
        "code": "BVEM0663C65",
        "name": "The Chevalier Gold Chain",
        "url": "https://www.bluestone.com/chains/the-chevalier-gold-chain~124914.html",
        "png": ROOT / "ProductImages/seo images/Chains/The Chevalier Gold Chain.png",
    },
    {
        "code": "BIMG0635V45",
        "name": "The Shining Star Bracelet",
        "url": "https://www.bluestone.com/bracelets/the-shining-star-bracelet~63731.html",
        "png": ROOT / "ProductImages/seo images/Bracelet/The Shining Star Bracelet.png",
    },
    {
        "code": "BINS0639R11",
        "name": "The Haily Ring",
        "url": "https://www.bluestone.com/rings/the-haily-ring~64366.html",
        "png": ROOT / "ProductImages/seo images/Rings/The Haily Ring.png",
    },
]

SECTIONS = {
    "creative": [
        "பொங்கல் வாழ்த்துக்கள்! புது நெல்லின் வாசமும், புது நம்பிக்கையும் உங்கள் வீட்டில் நிறையட்டும்.",
        "இனிய பொங்கல் திருநாள் நல்வாழ்த்துக்கள். சூரியனின் ஒளி போல உங்கள் வாழ்க்கை பிரகாசிக்கட்டும்.",
        "Creative Pongal wish: May your pot of joy overflow like sweet Pongal this harvest season.",
        "பொங்கல் திருநாள் வாழ்த்துக்கள். நன்றி, அன்பு, செழிப்பு ஆகியவை உங்கள் குடும்பத்தைச் சுற்றி வளரட்டும்.",
        "புதுப்பொங்கல் வாழ்த்துக்கள்! பழைய கவலைகள் போக, புதிய ஆனந்தம் உங்கள் நாளுக்குள் வரட்டும்.",
        "இனிய பொங்கல்! கரும்பின் இனிப்பும், பொங்கலின் வெப்பமும் உங்கள் உறவுகளில் நிறையட்டும்.",
        "Happy Pongal 2027! May every home feel warmer, fuller, and grateful for the harvest.",
        "பொங்கல் வளம் பெருகட்டும். உங்கள் கனவுகள் பொங்கி வழியட்டும். இனிய பொங்கல் வாழ்த்துக்கள்!",
        "A creative line for cards: Fresh harvest, fresh hope, and a heart full of Pongal joy.",
        "சூரிய பகவானின் ஆசியுடன் இனிய தைப்பொங்கல் வாழ்த்துக்கள். நலம் பெருகட்டும்!",
    ],
    "happy": [
        "இனிய பொங்கல் வாழ்த்துக்கள்! உங்கள் குடும்பத்திற்கு அமைதியும் மகிழ்ச்சியும் நிரம்பட்டும்.",
        "Happy Pongal wishes in Tamil start here: பொங்கலோ பொங்கல்! நல்வாழ்த்துகள்.",
        "தைப்பொங்கல் நல்வாழ்த்துக்கள். உழைப்பின் பலன் இனிமையாகத் தெரியட்டும்.",
        "Happy Pongal 2027 to you and your family. May prosperity visit every doorway.",
        "இனிய பொங்கல் திருநாள். அன்புள்ள உறவுகளுடன் இனிமையான நாள் அமையட்டும்.",
        "பொங்கல் வாழ்த்துகள்! ஆரோக்கியம், செல்வம், சந்தோஷம் உங்களைத் தேடி வரட்டும்.",
        "Wishing you a Happy Pongal filled with sugarcane sweetness and family laughter.",
        "புத்தம் புதிய பொங்கல் வாழ்த்துக்கள். உங்கள் நாட்கள் பொங்கி மகிழட்டும்!",
    ],
    "valthukkal": [
        "பொங்கல் வாழ்த்துக்கள்! உங்கள் வீட்டில் அமைதி பொங்கட்டும், மகிழ்ச்சி பொங்கட்டும்.",
        "Pongal valthukkal tamil: இனிய பொங்கல் திருநாள் நல்வாழ்த்துக்கள் அனைவருக்கும்.",
        "இனிய பொங்கல் வாழ்த்துக்கள் உங்களுக்கும் உங்கள் அன்பார்ந்தவர்களுக்கும்.",
        "நன்றி நிறைந்த பொங்கல் வாழ்த்துக்கள். விவசாயத்தின் வெற்றியைக் கொண்டாடுவோம்.",
        "Pongal valthukkal for WhatsApp: பொங்கலோ பொங்கல்! இனிய தை திருநாள்.",
        "குடும்பத்துடன் பகிரும் இனிய பொங்கல் வாழ்த்துக்கள். அன்பு பெருகட்டும்.",
        "வணக்கம்! இனிய பொங்கல் வாழ்த்துக்கள். புது ஆண்டு நம்பிக்கையுடன் தொடங்கட்டும்.",
        "Warm pongal valthukkal: May your kitchen smell of joy and your heart stay light.",
    ],
    "new": [
        "New Pongal wishes in Tamil: புதிய பொங்கல், புதிய நம்பிக்கை, புதிய வெற்றி!",
        "புதுப்பொங்கல் 2027 வாழ்த்துக்கள். உங்கள் இலக்குகள் இனிமையாக நிறைவேறட்டும்.",
        "இந்த புதிய பொங்கலில் பழைய சோர்வு நீங்கட்டும், புதிய ஆர்வம் பிறக்கட்டும்.",
        "Fresh greeting: New harvest energy for every plan you start this Pongal.",
        "புதிய பொங்கல் வாழ்த்துகள்! உங்கள் வாழ்க்கை பொன் போல ஒளிரட்டும்.",
        "New Pongal line for stories: Fresh rice, fresh smiles, fresh beginnings.",
    ],
    "whatsapp": [
        "WhatsApp Pongal wishes in Tamil: இனிய பொங்கல்! நீங்களும் உங்கள் குடும்பமும் நலமாக இருங்கள்.",
        "Copy this: பொங்கல் வாழ்த்துக்கள் 🌾 உங்கள் நாள் இனிமையாக அமையட்டும்.",
        "Status ready: Happy Pongal 2027 | பொங்கலோ பொங்கல்!",
        "குழு செய்தி: அனைவருக்கும் இனிய பொங்கல் வாழ்த்துக்கள். அன்புடன்.",
        "Short text: இனிய தைப்பொங்கல் நல்வாழ்த்துக்கள்.",
        "Pongal wishes in tamil text: May sweetness fill your home this harvest festival.",
        "Send this: புது நெல், புது மகிழ்ச்சி, புது ஆசீர்வாதம். இனிய பொங்கல்!",
        "Quick chat note: Happy Pongal! Thinking of you and sending warm wishes.",
    ],
    "images": [
        "Caption for Pongal wishes in tamil images: பொங்கலோ பொங்கல்! Joy in every frame.",
        "Photo text idea: Fresh pot, fresh hope. Happy Pongal 2027.",
        "Reel cover line: இனிய பொங்கல் வாழ்த்துக்கள் from our home to yours.",
        "Story sticker text: Pongal vibes + grateful hearts.",
        "Image caption: Sugarcane smiles and family hugs. இனிய பொங்கல்!",
        "Poster line: Celebrate the harvest. Share the love. Happy Pongal.",
    ],
    "family": [
        "அம்மாவுக்கு: உங்கள் கையால் வந்த பொங்கல் போல, என் வாழ்க்கையும் இனிக்கிறது. இனிய பொங்கல்!",
        "அப்பாவுக்கு: உங்கள் உழைப்பே எங்கள் செழிப்பு. இனிய பொங்கல் வாழ்த்துக்கள்.",
        "To my siblings: Sharing Pongal sweetness with the people who feel like home.",
        "குடும்பத்திற்கு: ஒன்றாக உண்ணும் பொங்கல் போல, ஒன்றாக வாழும் மகிழ்ச்சி பெருகட்டும்.",
    ],
    "friends": [
        "நண்பர்களுக்கு இனிய பொங்கல்! உங்கள் நட்பு எப்போதும் இனிமையாக இருக்கட்டும்.",
        "Happy Pongal, friend. May this season bring easy laughter and good news.",
        "நண்பா, பொங்கல் வாழ்த்துக்கள். உன் கனவுகள் பொங்கி வழியட்டும்!",
        "To my circle: Grateful for friends who make every festival warmer.",
    ],
    "sankranti": [
        "Happy Makar Sankranti! May the sun's journey bring clarity and courage to your year.",
        "Wishing you a bright Makar Sankranti filled with gratitude for every harvest blessing.",
        "On Makar Sankranti, may kite skies and kind hearts rise together.",
        "Makar Sankranti greetings: Sweet sesame wishes for a sweeter year ahead.",
    ],
    "bihu": [
        "Happy Magh Bihu! May the community feast fill your home with warmth and song.",
        "Magh Bihu wishes: Celebrate the harvest, honour the land, cherish your people.",
        "Sending Magh Bihu greetings across Assam and beyond. Prosperity to every hearth.",
        "On Magh Bihu, may gratitude stay as rich as the feast you share.",
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
        alt = f"Pongal 2027 gift idea: {product['name']} from BlueStone"
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
    script = script.replace("bs-cf-eid", "bs-cf-pongal")
    return (
        "<!-- wp:html -->\n<style>\n"
        + style
        + '\n</style>\n<div class="bs-cf" id="bs-cf-pongal" data-interval="3200" aria-roledescription="carousel" aria-label="BlueStone Pongal gift ideas">\n'
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
            "What are some creative Pongal wishes in Tamil?",
            "Try: “பொங்கல் வாழ்த்துக்கள்! புது நெல்லின் வாசமும், புது நம்பிக்கையும் உங்கள் வீட்டில் நிறையட்டும்.” "
            "It feels warm for cards and WhatsApp.",
        ),
        (
            "What is a simple Happy Pongal wish in Tamil?",
            "A clear line is: “இனிய பொங்கல் வாழ்த்துக்கள்!” "
            "Add a name or family note to make it personal.",
        ),
        (
            "What does Pongal valthukkal mean?",
            "Pongal valthukkal means Pongal greetings or blessings in Tamil. "
            "Use it for festive messages, status updates, and family group chats.",
        ),
        (
            "Can I send Pongal wishes in Tamil text on WhatsApp?",
            "Yes. Short Tamil lines with one emoji work best. "
            "Example: “பொங்கலோ பொங்கல்! இனிய தைப்பொங்கல் நல்வாழ்த்துக்கள்.”",
        ),
        (
            "What caption fits Pongal wishes in Tamil images?",
            "Use a short bilingual caption such as “பொங்கலோ பொங்கல்! Happy Pongal 2027.” "
            "Keep the text light so the photo stays the focus.",
        ),
        (
            "What is a thoughtful Pongal gift idea from BlueStone?",
            "Festive gold pieces such as The Shubhlatika Mangalsutra Necklace or The Estrella Oval Bangle "
            "make lasting harvest-season keepsakes for family celebrations.",
        ),
    ]
    html = [h2("Frequently Asked Questions about Creative Pongal Wishes in Tamil")]
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
            "Looking for <strong>creative Pongal wishes in Tamil</strong>, happy Pongal wishes in Tamil, "
            "pongal valthukkal, and WhatsApp-ready Tamil greetings for 2027? "
            "This refreshed guide gathers copy-paste Tamil wishes, English harvest lines, and soft gift ideas for the season."
        ),
        para(
            "<strong>TL;DR:</strong> Copy a creative Tamil Pongal wish, a short pongal valthukkal for status, "
            "or a bilingual caption for images. All lists are refreshed for Pongal 2027."
        ),
        para(
            "Pongal celebrates harvest, gratitude, and togetherness. "
            "A sincere Tamil greeting, and sometimes a lasting gold keepsake, can make the festival feel personal and bright."
        ),
        h2("Creative Pongal Wishes in Tamil"),
        para(
            "These creative Pongal wishes in Tamil mix festive warmth with lines that feel fresh for cards, stories, and family chats."
        ),
        list_block(SECTIONS["creative"]),
        h2("Happy Pongal Wishes in Tamil"),
        para("Send these happy Pongal wishes in Tamil to relatives, neighbours, and festive groups."),
        list_block(SECTIONS["happy"]),
        carousel,
        h2("A Soft Pongal Gift Idea for Her"),
        para(
            "If your Pongal greeting comes with a keepsake, festive gold jewellery feels lasting and graceful. "
            "Browse the carousel above for BlueStone pieces that suit harvest celebrations and family gifting."
        ),
        h2("Pongal Valthukkal Tamil Greetings"),
        para("Classic pongal valthukkal tamil lines for elders, friends, and morning festive messages."),
        list_block(SECTIONS["valthukkal"]),
        h2("New Pongal Wishes in Tamil"),
        para("Fresh new Pongal wishes in Tamil for 2027 status updates and invitation notes."),
        list_block(SECTIONS["new"]),
        h2("WhatsApp Pongal Wishes in Tamil & Text"),
        para("Short WhatsApp Pongal wishes in Tamil and easy Pongal wishes in Tamil text for busy chats."),
        list_block(SECTIONS["whatsapp"]),
        h2("Pongal Wishes in Tamil Images: Caption Ideas"),
        para("Use these lines with Pongal wishes in Tamil images, reels, and story posts."),
        list_block(SECTIONS["images"]),
        h2("Pongal Wishes for Family"),
        para("Warm Tamil and English lines for parents, siblings, and the people who cook the feast."),
        list_block(SECTIONS["family"]),
        h2("Pongal Wishes for Friends"),
        para("Friendly greetings for the people who make every festival sweeter."),
        list_block(SECTIONS["friends"]),
        h2("Makar Sankranti Wishes"),
        para("Because harvest joy travels across India, here are clear Makar Sankranti wishes for 2027."),
        list_block(SECTIONS["sankranti"]),
        h2("Magh Bihu Wishes"),
        para("Share these Magh Bihu wishes with friends celebrating the Assamese harvest feast."),
        list_block(SECTIONS["bihu"]),
        h2("More Festive & Occasion Reads"),
        para(
            'Explore our other guides including <a href="https://blog.bluestone.com/happy-diwali-wishes-messages-quotes-2026/">Diwali wishes for 2026</a>, '
            '<a href="https://blog.bluestone.com/26-january-republic-day-wishes-quotes-patriotic-messages/">Republic Day wishes for 2027</a>, '
            '<a href="https://blog.bluestone.com/happy-international-mens-day-best-quotes-wishes-messages/">International Men\'s Day quotes for 2026</a>, '
            '<a href="https://blog.bluestone.com/bhai-dooj-wishes/">Bhai Dooj wishes for 2026</a>, and '
            '<a href="https://blog.bluestone.com/raksha-bandhan-quotes-in-english/">Raksha Bandhan quotes for 2026</a>. '
            'Learn more about <a href="https://en.wikipedia.org/wiki/Pongal_(festival)">Pongal on Wikipedia</a>.'
        ),
        faq_html,
        h2("Conclusion"),
        para(
            "The best creative Pongal wishes in Tamil keep gratitude simple and the tone warm. "
            "Pick a pongal valthukkal that fits your people, personalize it, and share it with joy. "
            "Happy Pongal 2027!"
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
        "datePublished": "2026-01-10",
        "dateModified": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "author": {"@type": "Person", "name": "Vikas"},
        "publisher": {"@type": "Organization", "name": "BlueStone", "url": "https://www.bluestone.com/"},
        "image": images,
        "mainEntityOfPage": {"@type": "WebPage", "@id": LIVE_URL},
        "keywords": [
            "creative pongal wishes in tamil",
            "happy pongal wishes in tamil",
            "new pongal wishes in tamil",
            "pongal wishes in tamil images",
            "pongal valthukkal tamil",
            "pongal wishes in tamil text",
            "whatsapp pongal wishes in tamil",
            "pongal valthukkal",
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
        "carousel_mid_article": content.index("bs-cf-pongal") < content.index("Frequently Asked Questions"),
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
    assets = ROOT / "output/Week1_Rank19_PongalTamil_assets"
    assets.mkdir(parents=True, exist_ok=True)

    product_media = []
    for product in PRODUCTS:
        if not product["png"].exists():
            raise SystemExit(f"Missing SEO Type 2 image: {product['png']}")
        filename = re.sub(r"[^A-Za-z0-9]+", "-", product["name"]).strip("-").lower() + "-carousel-seo.webp"
        webp = assets / filename
        to_carousel_webp(product["png"], webp)
        alt = f"Pongal 2027 gift idea: {product['name']} from BlueStone"
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
    (ROOT / "output/Week1_Rank19_PongalTamil_article.html").write_text(content)
    (ROOT / "output/Week1_Rank19_PongalTamil_product_media.json").write_text(json.dumps(product_media, indent=2))

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
