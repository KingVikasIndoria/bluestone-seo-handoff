#!/usr/bin/env python3
"""Optimize Week 1 Rank 20: Women's Day Message (WP #21265)."""
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

POST_ID = 21265
TITLE = "100+ Women's Day Message, Quotes & International Women's Day Wishes for 2027"
SLUG = "happy-womens-day-quotes-wishes-and-messages-to-celebrate-strength-and-empowerment"
META_DESC = (
    "Find 100+ women's day message ideas, International Women's Day wishes, "
    "happy womens day wishes quotes, and inspire quotes for 2027. Ready to copy."
)
FOCUS_KW = "women's day message"
YOAST_TITLE = "Women's Day Message, Quotes & Wishes 2027 | BlueStone"
LIVE_URL = f"https://blog.bluestone.com/{SLUG}/"

PRODUCTS = [
    {
        "code": "BIHS1145P21",
        "name": "The Valeria Rose Pendant",
        "url": "https://www.bluestone.com/pendants/the-valeria-rose-pendant~181266.html",
        "png": ROOT / "ProductImages/seo images/Pendants/The Valeria Rose Pendant.png",
    },
    {
        "code": "BISA0255D05",
        "name": "The Asya Huggie Earrings",
        "url": "https://www.bluestone.com/earrings/the-asya-huggie-earrings~13494.html",
        "png": ROOT / "ProductImages/seo images/Earrings/The Asya Huggie Earrings.png",
    },
    {
        "code": "BISE0932R181",
        "name": "The Le Sommet Ring",
        "url": "https://www.bluestone.com/rings/the-le-sommet-ring~105031.html",
        "png": ROOT / "ProductImages/seo images/Rings/The Le Sommet Ring.png",
    },
    {
        "code": "BIDG0393O37",
        "name": "The Estrella Oval Bangle",
        "url": "https://www.bluestone.com/bangles/the-estrella-oval-bangle~34771.html",
        "png": ROOT / "ProductImages/seo images/Bangles/The Estrella Oval Bangle.png",
    },
    {
        "code": "BIPO0730V39",
        "name": "The Kricia Charm Bracelet",
        "url": "https://www.bluestone.com/bracelets/the-kricia-charm-bracelet~75605.html",
        "png": ROOT / "ProductImages/seo images/Bracelet/The Kricia Charm Bracelet.png",
    },
    {
        "code": "BIAV0987N78",
        "name": "The Ailia Evil Eye Layered Necklace",
        "url": "https://www.bluestone.com/necklaces/the-ailia-evil-eye-layered-necklace~116379.html",
        "png": ROOT / "ProductImages/seo images/Necklaces/The Ailia Evil Eye Layered Necklace.png",
    },
]

SECTIONS = {
    "message": [
        "Happy Women's Day! Your courage, care, and quiet brilliance make every room better.",
        "A women's day message for you: thank you for leading with empathy and strength.",
        "On International Women's Day, may you feel seen for the work you do and the light you carry.",
        "Happy Women's Day 2027. You deserve rest, respect, and a celebration that feels personal.",
        "Today's women's day message is simple: your voice matters, and so does your peace.",
        "Wishing you a Happy International Women's Day filled with pride in how far you have come.",
        "To every woman building, healing, and rising: Happy Women's Day. The world is better with you in it.",
        "A warm women's day message: may your ambition stay bold and your heart stay kind.",
        "Happy Women's Day to the woman who makes ordinary days feel safer and brighter.",
        "Celebrating you today and every day. Happy International Women's Day 2027!",
    ],
    "wishes": [
        "Happy International Women's Day wishes to the women who lift others as they climb.",
        "Sending happy womens day wishes quotes of love, respect, and endless possibility.",
        "International Women's Day wishes: may your dreams find room, support, and applause.",
        "Happy Women's Day! Wishing you health, freedom, and joy that feels earned.",
        "Warm International Women's Day wishes for the teachers, mothers, leaders, and dreamers among us.",
        "Happy womens day wishes for a year of growth without apology.",
        "On this Women's Day, wishing you soft days and strong boundaries.",
        "International Women's Day wishes from our home to yours: you are celebrated.",
    ],
    "quotes_en": [
        "A woman is not defined by silence. She is defined by the truth she chooses to speak.",
        "Womens day quote in english: Strength looks beautiful when it protects someone else's peace.",
        "She believed she could, so she built a life that proved it.",
        "Empowerment begins when a woman trusts her own voice more than the noise around her.",
        "A womens day quote in english for cards: Grace is not softness alone. It is courage with kindness.",
        "The world moves forward every time a woman is given room to lead.",
        "She carries ambition and tenderness in the same brave hands.",
        "Real power is a woman who rises and still helps others rise.",
    ],
    "inspire": [
        "Womens day inspire quotes start here: Your story can open a door for someone else.",
        "Be the woman who turns doubt into direction and fear into focus.",
        "Inspire quote for Women's Day: You do not need permission to become who you already are.",
        "Shine without shrinking. Lead without apology. Love without losing yourself.",
        "Womens day inspire quotes for students: Learn loudly. Dream clearly. Grow kindly.",
        "Your resilience is not invisible. It is the quiet engine of everything you build.",
        "Keep going. The version of you that you are becoming is already worth celebrating.",
        "Inspiration for Women's Day: Choose courage in small moments. They change everything.",
    ],
    "status": [
        "Women's day status: Celebrating every woman who shows up with heart and grit.",
        "Happy International Women's Day 2027. Proud, grateful, unstoppable.",
        "Status idea: Strong women. Soft hearts. Loud dreams.",
        "Women's Day status for Instagram: Honour her story. Amplify her voice.",
        "Story text: Happy Women's Day to the women who make life kinder.",
        "Caption: Empowered women empower the whole room.",
        "WhatsApp status: Happy Women's Day! May respect be the default everywhere.",
        "Reel cover: International Women's Day vibes. Celebrate her always.",
    ],
    "friends_family": [
        "Happy Women's Day, Mom. Your strength taught me how to stand tall with kindness.",
        "To my sister: Happy Women's Day. Grateful for a lifelong teammate and friend.",
        "Happy Women's Day to my best friend. Your courage makes my world braver.",
        "For the women in my family: thank you for love that feels like home and hope.",
        "Happy International Women's Day to every aunt, cousin, and chosen sister who shows up.",
        "To my daughter: Happy Women's Day. May you always know your worth.",
    ],
    "office": [
        "Happy Women's Day to our brilliant team. Thank you for leadership that lifts everyone.",
        "Wishing every colleague a meaningful International Women's Day filled with respect and recognition.",
        "Office note: Happy Women's Day. May workplaces keep choosing fairness and growth.",
        "Professional wish: Celebrating the women who mentor, build, and inspire at work.",
        "Happy Women's Day to leaders who make inclusion a daily practice, not a slogan.",
    ],
    "short": [
        "Happy Women's Day! You are powerful and loved.",
        "Celebrating you today. Happy International Women's Day!",
        "Short wish: Stay bold. Stay kind. Happy Women's Day.",
        "You inspire me. Happy Women's Day 2027!",
        "Cheers to women everywhere. Happy Women's Day!",
        "Simple and true: Thank you for being you. Happy Women's Day.",
        "Rise and shine. Happy International Women's Day!",
        "Respect. Love. Freedom. Happy Women's Day!",
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
        alt = f"Women's Day 2027 gift idea: {product['name']} from BlueStone"
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
    script = script.replace("bs-cf-eid", "bs-cf-womensday")
    return (
        "<!-- wp:html -->\n<style>\n"
        + style
        + '\n</style>\n<div class="bs-cf" id="bs-cf-womensday" data-interval="3200" aria-roledescription="carousel" aria-label="BlueStone Women\'s Day gift ideas">\n'
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
            "What is a good women's day message for 2027?",
            "Try: “Happy Women's Day! Your courage, care, and quiet brilliance make every room better.” "
            "It works for cards, WhatsApp, and office notes.",
        ),
        (
            "What are popular International Women's Day wishes?",
            "A clear wish is: “Happy International Women's Day. May your dreams find room, support, and applause.” "
            "Keep it short for group chats.",
        ),
        (
            "Can you share a womens day quote in english?",
            "Yes. One strong line is: “A woman is not defined by silence. She is defined by the truth she chooses to speak.” "
            "Pair it with a sincere photo.",
        ),
        (
            "What are good womens day inspire quotes?",
            "Use: “You do not need permission to become who you already are.” "
            "It fits Instagram captions and classroom boards.",
        ),
        (
            "What should I post as a Women's Day status?",
            "Try: “Happy International Women's Day 2027. Proud, grateful, unstoppable.” "
            "Add a personal note if you are tagging someone special.",
        ),
        (
            "What is a thoughtful Women's Day gift idea from BlueStone?",
            "Elegant pieces such as The Valeria Rose Pendant or The Le Sommet Ring "
            "make lasting keepsakes for International Women's Day celebrations.",
        ),
    ]
    html = [h2("Frequently Asked Questions about Women's Day Messages & Quotes")]
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
            "Looking for a heartfelt <strong>women's day message</strong>, International Women's Day wishes, "
            "happy womens day wishes quotes, and inspire quotes for 2027? "
            "This refreshed collection is ready for WhatsApp, Instagram, cards, and office notes."
        ),
        para(
            "<strong>TL;DR:</strong> Copy a women's day message, a short International Women's Day wish, "
            "an English quote, or a status line. All lists are refreshed for Women's Day 2027."
        ),
        para(
            "International Women's Day celebrates courage, equality, and the everyday brilliance of women everywhere. "
            "A sincere message, and sometimes a lasting keepsake, can make 8 March feel personal and proud."
        ),
        h2("Women's Day Message Ideas for 2027"),
        para("These women's day message lines work for loved ones, mentors, and anyone you want to honour."),
        list_block(SECTIONS["message"]),
        h2("Happy International Women's Day Wishes"),
        para("Send these International Women's Day wishes and happy womens day wishes quotes with warmth."),
        list_block(SECTIONS["wishes"]),
        carousel,
        h2("A Soft Women's Day Gift Idea for Her"),
        para(
            "If your Women's Day greeting comes with a keepsake, elegant gold jewellery feels lasting and personal. "
            "Browse the carousel above for BlueStone pieces that celebrate her style."
        ),
        h2("Womens Day Quote in English"),
        para("Clear womens day quote in english lines for cards, captions, and speeches."),
        list_block(SECTIONS["quotes_en"]),
        h2("Womens Day Inspire Quotes"),
        para("Use these womens day inspire quotes when you want motivation with heart."),
        list_block(SECTIONS["inspire"]),
        h2("Women's Day Status for Instagram & WhatsApp"),
        para("Quick women's day status ideas for stories, captions, and chat updates."),
        list_block(SECTIONS["status"]),
        h2("Women's Day Wishes for Friends & Family"),
        para("Personal wishes for the women closest to you."),
        list_block(SECTIONS["friends_family"]),
        h2("Women's Day Message for Office & Professional Use"),
        para("Respectful notes for teams, mentors, and workplace celebrations."),
        list_block(SECTIONS["office"]),
        h2("Short Women's Day Messages for WhatsApp"),
        para("Short copy-ready lines when you need something quick and sincere."),
        list_block(SECTIONS["short"]),
        h2("More Festive & Occasion Reads"),
        para(
            'Explore our other guides including <a href="https://blog.bluestone.com/happy-international-mens-day-best-quotes-wishes-messages/">International Men\'s Day quotes for 2026</a>, '
            '<a href="https://blog.bluestone.com/romantic-valentines-day-wishes-quotes-celebrate-love-in-the-most-beautiful-way/">Valentine\'s hubby quotes for 2027</a>, '
            '<a href="https://blog.bluestone.com/makar-sankranti-quotes-wishes-pongal-and-magh-bihu-festival-greetings/">Pongal wishes in Tamil for 2027</a>, '
            '<a href="https://blog.bluestone.com/26-january-republic-day-wishes-quotes-patriotic-messages/">Republic Day wishes for 2027</a>, and '
            '<a href="https://blog.bluestone.com/happy-fathers-day-wishes-quotes-and-messages-for-every-dad/">Father\'s Day quotes for 2026</a>. '
            'Learn more about <a href="https://en.wikipedia.org/wiki/International_Women%27s_Day">International Women\'s Day on Wikipedia</a>.'
        ),
        faq_html,
        h2("Conclusion"),
        para(
            "The best women's day message keeps gratitude clear and celebration sincere. "
            "Pick a line that fits the woman you are honouring, personalize it, and share it with pride. "
            "Happy International Women's Day 2027!"
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
        "datePublished": "2026-02-16",
        "dateModified": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "author": {"@type": "Person", "name": "Vikas"},
        "publisher": {"@type": "Organization", "name": "BlueStone", "url": "https://www.bluestone.com/"},
        "image": images,
        "mainEntityOfPage": {"@type": "WebPage", "@id": LIVE_URL},
        "keywords": [
            "women's day message",
            "international women's day wishes",
            "happy womens day wishes quotes",
            "womens day quote in english",
            "womens day inspire quotes",
            "women's day status",
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
        "carousel_mid_article": content.index("bs-cf-womensday") < content.index("Frequently Asked Questions"),
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
    assets = ROOT / "output/Week1_Rank20_WomensDay_assets"
    assets.mkdir(parents=True, exist_ok=True)

    product_media = []
    for product in PRODUCTS:
        if not product["png"].exists():
            raise SystemExit(f"Missing SEO Type 2 image: {product['png']}")
        filename = re.sub(r"[^A-Za-z0-9]+", "-", product["name"]).strip("-").lower() + "-carousel-seo.webp"
        webp = assets / filename
        to_carousel_webp(product["png"], webp)
        alt = f"Women's Day 2027 gift idea: {product['name']} from BlueStone"
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
    (ROOT / "output/Week1_Rank20_WomensDay_article.html").write_text(content)
    (ROOT / "output/Week1_Rank20_WomensDay_product_media.json").write_text(json.dumps(product_media, indent=2))

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
