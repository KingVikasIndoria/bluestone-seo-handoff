#!/usr/bin/env python3
"""Publish/Optimize Week 1 Rank 11: Dussehra Wishes in English (New post)."""
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

TITLE = "100+ Happy Dussehra Wishes, Quotes & Greetings in English for 2026"
SLUG = "dussehra-wishes-in-english"
META_DESC = (
    "Find 100+ Happy Dussehra wishes, quotes and greetings in English for 2026. "
    "Features Shubho Bijoya Bengali wishes, Dasara wishes in Hindi and Kannada, and meaningful quotes. Ready to copy."
)
FOCUS_KW = "dussehra wishes in english"
YOAST_TITLE = "Happy Dussehra Wishes, Quotes & Greetings 2026 | BlueStone"
LIVE_URL = f"https://blog.bluestone.com/{SLUG}/"

PRODUCTS = [
    {
        "code": "BINK0363B03",
        "name": "The Skein Bangle",
        "url": "https://www.bluestone.com/bangles/the-skein-bangle~27491.html",
        "png": ROOT / "ProductImages/seo images/Bangles/The Skein Bangle.png",
    },
    {
        "code": "BISM0003O14",
        "name": "The Muricelle Bangle",
        "url": "https://www.bluestone.com/bangles/the-muricelle-bangle~1001.html",
        "png": ROOT / "ProductImages/seo images/Bangles/The Muricelle Bangle.png",
    },
    {
        "code": "BIPS0003O06",
        "name": "The Channing Bangle",
        "url": "https://www.bluestone.com/bangles/the-channing-bangle~975.html",
        "png": ROOT / "ProductImages/seo images/Bangles/The Channing Bangle.png",
    },
    {
        "code": "BENS0325O09",
        "name": "The Tarentella Oval Bangle",
        "url": "https://www.bluestone.com/bangles/the-tarentella-oval-bangle~31547.html",
        "png": ROOT / "ProductImages/seo images/Bangles/The Tarentella Oval Bangle.png",
    },
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
]

SECTIONS = {
    "short": [
        "Wishing you a very Happy Dussehra! May all your troubles burn away with the effigy of Ravana.",
        "May this festive day bring victory, prosperity, and happiness to you and your loved ones.",
        "Wishing you a bright and joyful Vijaya Dashami! Celebrate the triumph of good over evil.",
        "May the blessings of Lord Rama keep you secure, happy, and prosperous. Happy Dussehra 2026!",
        "Let the positive energy of Dussehra light up your path to success and peace. Jai Sri Ram!",
        "Warm greetings on Dussehra! May you conquer all your challenges with courage and grace.",
        "Hoping this festive season fills your home with good health and endless joy. Happy Dasara!",
        "May the light of truth always guide your steps. Wishing you a blessed Vijayadashami!",
    ],
    "family": [
        "Sending our warmest family wishes on Dussehra. May our household be blessed with peace and daily progress.",
        "To my wonderful family, may this Dussehra mark the beginning of new achievements and warm memories.",
        "Wishing my dear friends a happy and peaceful Dussehra. Grateful for the protective bonds we share.",
        "May the victory of Lord Rama inspire us to face every life challenge together as a strong family.",
        "Hoping the warm festive lights of Vijayadashami bring health, security, and wealth to your doorstep.",
        "Let's celebrate the triumph of good, reflecting on our shared values and family traditions this Dussehra.",
        "May Lord Rama bless our home with unity, harmony, and prosperity on this auspicious day.",
        "Sending sweet wishes and prayers for a bright and successful year ahead to my best friends.",
    ],
    "quotes": [
        "Dussehra is a reminder that truth always wins, and good triumphs over evil. Jai Sri Ram!",
        "Let the inner Ravana burn away, leaving room for truth, integrity, and daily kindness.",
        "Vijayadashami is the celebration of courage, patience, and the ultimate victory of light over dark.",
        "The story of Rama is a guide for daily actions, showing that patience and character lead to success.",
        "May you find the strength to conquer your fears and build a path of honesty and wisdom.",
        "Dussehra is not just a holiday; it's a promise that honesty outlasts any temporary difficulty.",
    ],
    "regional": [
        "Dussehra ki hardik shubhkamnayen! May this day bring light and peace to your life.",
        "Happy Dasara wishes in Hindi: Aapko aur aapke parivar ko Dussehra ki dheron shubhkamnayen.",
        "Dasara wishes in Kannada: Vijayadashamiya hardika shubhashayagalu. May the Goddess bless you.",
        "Bengal's Shubho Bijoya wishes: Shubho Bijoya Dashami! Sending respect and warm festive hugs.",
        "Shubho Bijoya wishes to all: May the sweet joy of Dashami remain with you throughout the year.",
        "Dasara wishes in Hindi: Ravan dahan ke sath aapke dukhon ka nash ho, aur sukh ka agaman ho.",
        "Wishing you shubho bijoya! Reflecting on the strength Durga Puja leaves in our hearts.",
        "May the spirit of Vijayadashami bring joy and success in every language and region.",
    ],
    "colleagues": [
        "Wishing you a successful and happy Dussehra! Proud to work alongside you daily.",
        "May this Vijayadashami open new doors of progress and professional achievements for you.",
        "Warm greetings on Dussehra to our team. May our collective efforts bring victory and growth.",
        "Wishing you and your family a peaceful holiday. Thank you for your daily support in office.",
        "May the festival of Dussehra inspire new creativity and successful project launches.",
        "Hoping this festive season brings you rest, inspiration, and renewed professional energy.",
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
        alt = f"Dussehra 2026 gift idea: {product['name']} from BlueStone"
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
    script = script.replace("bs-cf-eid", "bs-cf-dussehra")
    return (
        "<!-- wp:html -->\n<style>\n"
        + style
        + '\n</style>\n<div class="bs-cf" id="bs-cf-dussehra" data-interval="3200" aria-roledescription="carousel" aria-label="BlueStone Dussehra gift ideas">\n'
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
            "What are the best happy dussehra wishes in english for 2026?",
            "The best happy Dussehra wishes focus on victory, positive starts, and prosperity. For example: “Wishing you a very Happy Dussehra! May all your troubles burn away with the effigy of Ravana.” These greetings are perfect for card messages or text wishes.",
        ),
        (
            "What are some famous quotes of dussehra?",
            "Famous quotes focus on the triumph of light over dark: “Dussehra is a reminder that truth always wins, and good triumphs over evil. Jai Sri Ram!” It is a traditional sentiment shared across India during Vijayadashami.",
        ),
        (
            "How do I wish happy shubho bijoya to my friends?",
            "You can say: “Shubho Bijoya Dashami! Sending respect, happiness, and warm festive hugs to you and your parivar.” It is the traditional way to greet friends and family on the final day of Durga Puja.",
        ),
        (
            "What is a short happy dasara wish in kannada?",
            "In Kannada, you can wish: “Vijayadashamiya hardika shubhashayagalu.” It translates to warm wishes for a successful and happy Vijayadashami.",
        ),
        (
            "How can I write happy dasara wishes in hindi?",
            "In Hindi, write: “Aapko aur aapke parivar ko Dussehra ki dheron shubhkamnayen.” This translates to wishing you and your parivar a very happy and blessed Dussehra.",
        ),
        (
            "Can I send professional dussehra greetings to colleagues?",
            "Yes! Professional greetings focus on shared progress and victory: “Wishing you a successful and happy Dussehra! May this Vijayadashami open new doors of progress and professional achievements.”",
        ),
    ]
    html = [h2("Frequently Asked Questions about Dussehra Wishes")]
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
            "Looking for the best <strong>dussehra wishes in english</strong>, quotes, and greetings to share in 2026? "
            "Whether you need short card messages, heartfelt family greetings, meaningful quotes, or regional wishes in Hindi, Bengali, or Kannada, this list has you covered."
        ),
        para(
            "<strong>TL;DR:</strong> Copy a quick Dussehra wish for WhatsApp, a traditional shubho bijoya greeting, a dasara wish in Hindi, or a professional colleague message. "
            "All lists are updated for Dussehra 2026."
        ),
        para(
            "Dussehra (Vijayadashami) marks the triumph of truth, light, and righteousness. Sharing respect and blessings on this auspicious day is a beautiful home tradition."
        ),
        h2("Short & Meaningful Dussehra Wishes"),
        para("Keep your greetings direct, quick, and scanable with these copy-ready Dussehra wishes."),
        list_block(SECTIONS["short"]),
        h2("Heartfelt Dussehra Messages for Friends & Family"),
        para("Send these warm, personal wishes to friends and family members to celebrate the protective bonds of home."),
        list_block(SECTIONS["family"]),
        h2("Meaningful Dussehra Quotes"),
        para("These quotes of Dussehra celebrate courage, character, and the victory of Lord Rama."),
        list_block(SECTIONS["quotes"]),
        h2("Dussehra wishes in Hindi & Regional Languages"),
        para("Celebrate India's diverse traditions with these transliterated regional greetings, including Kannada, Hindi, and Bengali Shubho Bijoya wishes."),
        list_block(SECTIONS["regional"]),
        h2("A Sparkle of Victory: Festive Gold Jewelry Gifting"),
        para(
            "Dussehra is an auspicious time to buy gold jewelry, symbolising prosperity, wealth, and positive new beginnings. "
            "Whether you are treating yourself or finding a holiday keepsake for family, traditional diamond bangles and circular pendants are excellent choices. "
            "Explore these six approved options from the BlueStone collection."
        ),
        carousel,
        h2("Dussehra Greetings for Colleagues & Professional Contacts"),
        para("Share these professional greetings with your coworkers, clients, and managers to wish them success and daily progress."),
        list_block(SECTIONS["colleagues"]),
        h2("More Festive & Occasion Reads"),
        para(
            'Explore our other occasion guides including <a href="https://blog.bluestone.com/heart-touching-love-proposal-quotes-2027/">proposal quotes for 2027</a>, '
            '<a href="https://blog.bluestone.com/happy-holi-wishes-messages-quotes-2027/">Holi wishes for 2027</a>, '
            '<a href="https://blog.bluestone.com/happy-diwali-wishes-messages-quotes-2026/">Diwali wishes for 2026</a>, '
            '<a href="https://blog.bluestone.com/happy-eid-mubarak-wishes-messages-quotes-2027/">Eid wishes for 2027</a>, '
            '<a href="https://blog.bluestone.com/happy-childrens-day-best-wishes-quotes-messages-for-kids/">Children\'s Day quotes for 2026</a>, '
            '<a href="https://blog.bluestone.com/engagement-quotes/">engagement quotes for 2026</a>, and '
            '<a href="https://blog.bluestone.com/teachers-day-wishes-in-english/">Teachers\' Day wishes for 2026</a>.'
        ),
        faq_html,
        h2("Conclusion"),
        para(
            "The best dussehra wishes in english are simple, positive, and celebrate the victory of truth. "
            "Choose a wish that matches your relationship, add a warm personal note, and share the festive joy. Happy Dussehra 2026!"
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
            "dussehra wishes in english",
            "happy dussehra wishes hindi",
            "happy dasara wishes in hindi",
            "quotes of dussehra",
            "shubho bijoya wishes",
            "dasara wishes in kannada",
            "meaningful dussehra quotes",
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
        "carousel_mid_article": content.index("bs-cf-dussehra") < content.index("Frequently Asked Questions"),
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
    assets = ROOT / "output/Week1_Rank11_DussehraWishes_assets"
    assets.mkdir(parents=True, exist_ok=True)

    product_media = []
    for product in PRODUCTS:
        if not product["png"].exists():
            raise SystemExit(f"Missing approved Type 2 image: {product['png']}")
        filename = re.sub(r"[^A-Za-z0-9]+", "-", product["name"]).strip("-").lower() + "-carousel.webp"
        webp = assets / filename
        to_carousel_webp(product["png"], webp)
        alt = f"Dussehra 2026 gift idea: {product['name']} from BlueStone"
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
    (ROOT / "output/Week1_Rank11_DussehraWishes_article.html").write_text(content)
    (ROOT / "output/Week1_Rank11_DussehraWishes_product_media.json").write_text(
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
