#!/usr/bin/env python3
"""Publish/Optimize Week 1 Rank 10: Teachers' Day Wishes in English (New post)."""
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

TITLE = "100+ Happy Teachers' Day Wishes, Quotes & Messages in English for 2026"
SLUG = "teachers-day-wishes-in-english"
META_DESC = (
    "Find 100+ Happy Teachers' Day wishes, quotes and messages in English for 2026. "
    "Heartfelt messages from students or parents, short card quotes, WhatsApp status lines. Ready to copy."
)
FOCUS_KW = "teachers day wishes in english"
YOAST_TITLE = "Happy Teachers' Day Wishes, Quotes & Messages 2026 | BlueStone"
LIVE_URL = f"https://blog.bluestone.com/{SLUG}/"

PRODUCTS = [
    {
        "code": "BIIP0550P16",
        "name": "The Aagarna Pendant",
        "url": "https://www.bluestone.com/pendants/the-aagarna-pendant~54965.html",
        "png": ROOT / "ProductImages/seo images/Pendants/The Aagarna Pendant.png",
    },
    {
        "code": "BISW1080P246",
        "name": "The Xarvithis Pendant",
        "url": "https://www.bluestone.com/pendants/the-xarvithis-pendant~156920.html",
        "png": ROOT / "ProductImages/seo images/Pendants/The Xarvithis Pendant.png",
    },
    {
        "code": "BISW1080P132",
        "name": "The Sarvanya Pendant",
        "url": "https://www.bluestone.com/pendants/the-sarvanya-pendant~156927.html",
        "png": ROOT / "ProductImages/seo images/Pendants/The Sarvanya Pendant.png",
    },
    {
        "code": "BISW1080P131",
        "name": "The Thaloria Pendant",
        "url": "https://www.bluestone.com/pendants/the-thaloria-pendant~165041.html",
        "png": ROOT / "ProductImages/seo images/Pendants/The Thaloria Pendant.png",
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
]

SECTIONS = {
    "heartfelt": [
        "To a teacher who values patient guidance, daily support, and student growth. Happy Teachers' Day!",
        "May this Teachers' Day bring you the rest, respect, and deep joy you bring to your classroom daily.",
        "Your lessons went beyond the blackboard, teaching us integrity, courage, and daily kindness. Thank you.",
        "Wishing you a memorable and happy Teachers' Day, filled with the appreciation of all your students.",
        "May the knowledge you share continue to grow in the hearts and actions of the next generation.",
        "So grateful for your guidance, which has served as a constant anchor during my school days.",
        "Let the dedication you show daily be reflected in the success of the students who look up to you.",
        "Warmest wishes for a peaceful and happy Teachers' Day, thank you for making learning a joy.",
    ],
    "quotes": [
        "A teacher affects eternity; he can never tell where his influence stops.",
        "Teaching is not a profession; it's a way of life that shapes the future.",
        "The art of teaching is the art of assisting discovery.",
        "A good teacher is like a candle, consuming itself to light the way for others.",
        "Education is the most powerful weapon which you can use to change the world.",
        "The beautiful thing about learning is that no one can take it away from you.",
        "To teach is to touch a life forever, leaving a legacy of courage and hope.",
        "Grateful for the guidance that shapes our minds and inspires our everyday choices.",
    ],
    "short": [
        "Happy Teachers' Day! Thank you for your daily guidance and support.",
        "Your lessons are the foundation of my success. Happy Teachers' Day 2026!",
        "To a wonderful mentor, wishing you a happy and peaceful holiday.",
        "Thank you for teaching us with patience, clarity, and daily kindness.",
        "Your dedication makes a real difference in the lives of your students.",
        "Wishing you a memorable Teachers' Day celebration. Jai Hind!",
        "To the teacher who always believed in my dreams, thank you.",
        "May your day be filled with rest, respect, and sweet memories.",
    ],
    "creative": [
        "You are the spark that ignited my curiosity and the compass that guided my path.",
        "A classroom with you is not just a room of desks, but a garden of growing minds.",
        "Thank you for turning complex lessons into clean understanding and daily confidence.",
        "Your lessons are like seeds, growing into trees of success, stability, and character.",
        "A teacher's influence is a silent melody that plays throughout a student's life.",
        "Wishing you a bright, happy Teachers' Day, reflecting on the circles of knowledge you create.",
    ],
    "students": [
        "From all of us in class, thank you for making every lesson interesting and accessible.",
        "Happy Teachers' Day! We promise to do our homework and put your guidance into action.",
        "Thank you for listening to our questions with patience and daily kindness.",
        "Your classroom is our favorite place to learn, grow, and build our confidence.",
        "Wishing our favorite teacher a beautiful Teachers' Day, filled with the appreciation you deserve.",
        "From your students, sending gratitude, respect, and warm wishes for a wonderful year ahead.",
    ],
    "parents": [
        "Thank you for partner-guiding our child, helping them build both knowledge and character.",
        "We are grateful for the safety, support, and clarity you offer in your classroom daily.",
        "Wishing you a happy Teachers' Day, reflecting on the positive impact you have on our family.",
        "Your patience with the children makes you a true mentor. Sincere thank you from the parents.",
        "Thank you for keeping open communication and helping our child reach their true potential.",
        "May your dedication bring you the deep respect and progress you earn every single day.",
    ],
    "captions": [
        "A guide, a mentor, a constant support. Jai Hind!",
        "Grateful for the lessons that shaped my mind.",
        "Happy Teachers' Day 2026! Thank you for the spark.",
        "Choosing respect, gratitude, and appreciation today.",
        "To the mentors who make learning a lifetime journey.",
        "Teachers' Day mood: respectful, grateful, inspired.",
        "Lessons that outlast the classroom walls.",
        "To the teacher who believed in me, thank you. Jai Hind!",
        "A quiet guide, a lasting influence. Happy Teachers' Day!",
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
        alt = f"Teachers' Day 2026 gift idea: {product['name']} from BlueStone"
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
    script = script.replace("bs-cf-eid", "bs-cf-teachers")
    return (
        "<!-- wp:html -->\n<style>\n"
        + style
        + '\n</style>\n<div class="bs-cf" id="bs-cf-teachers" data-interval="3200" aria-roledescription="carousel" aria-label="BlueStone Teachers\' Day gift ideas">\n'
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
            "What are the best happy teachers day wishes in english for 2026?",
            "The best happy Teachers' Day wishes focus on gratitude, daily guidance, and support. Try: “Your lessons went beyond the blackboard, teaching us integrity, courage, and daily kindness. Thank you.” These wishes work beautifully for school celebrations and card greetings.",
        ),
        (
            "What is a short heart touching teachers day wishes message?",
            "A short message is: “To the teacher who always believed in my dreams, thank you for your daily support. Happy Teachers' Day 2026!” It is concise, respectful, and easy to share on WhatsApp.",
        ),
        (
            "How do I write a professional teachers day message?",
            "A professional message focus on dedication, integrity, and shared goals: “Warmest wishes for a peaceful and happy Teachers' Day, thank you for your patience and daily support.” Keep the tone respectful and warm.",
        ),
        (
            "What are some famous best teachers day quotes?",
            "Famous quotes focus on the eternal impact of education. For example: “A teacher affects eternity; he can never tell where his influence stops.” These quotes are perfect for card headings and formal tributes.",
        ),
        (
            "What are good teacher's day lines for a card?",
            "Good lines are: “Your lessons are the foundation of my success. Thank you for teaching us with patience, clarity, and daily kindness. Happy Teachers' Day!”",
        ),
        (
            "Can I send a teachers day wishing quote from parents?",
            "Yes! Parents can write: “Thank you for partner-guiding our child, helping them build both knowledge and character. Sincere thank you from the parents.” It shows appreciation for the teacher's role in the family.",
        ),
    ]
    html = [h2("Frequently Asked Questions about Teachers' Day Wishes")]
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
            "Looking for the best <strong>teachers day wishes in english</strong>, quotes, and messages to share in 2026? "
            "Whether you need heartfelt wishes, famous quotes, short lines for card tags, or messages from students and parents, this collection brings them together."
        ),
        para(
            "<strong>TL;DR:</strong> Choose a heartfelt wish for a card, a short quote for a quick text, a dedicated message from students or parents, "
            "or a simple WhatsApp status. Every list is updated for Teachers' Day 2026."
        ),
        para(
            "A teacher represents patience, knowledge, and daily guidance. Sharing a sincere message is a simple way to show deep respect."
        ),
        h2("Heartfelt Wishes for Teachers' Day"),
        para("Send these warm, respectful wishes to your teachers to celebrate their daily support."),
        list_block(SECTIONS["heartfelt"]),
        h2("Inspirational Quotes for Teachers' Day"),
        para("These famous quotes and sayings celebrate the eternal impact of teaching and mentoring."),
        list_block(SECTIONS["quotes"]),
        h2("Short & Sweet Messages for Teachers' Day"),
        para("Keep your greetings simple and elegant with these quick, copy-ready messages."),
        list_block(SECTIONS["short"]),
        h2("Poetic & Creative Wishes"),
        para("Add a creative note to your celebration with these metaphor-rich wishes."),
        list_block(SECTIONS["creative"]),
        h2("A Token of Gratitude for Teachers"),
        para(
            "If you are pairing your wishes with a keepsake, elegant and professional pendants are classic choices. "
            "Choose a simple gold diamond stud or an elegant cluster pendant that they can wear daily as a symbol of your respect. "
            "Here are six approved pendant ideas from the BlueStone collection."
        ),
        carousel,
        h2("Messages from Students"),
        para("These direct messages from classroom students show gratitude and appreciation for class lessons."),
        list_block(SECTIONS["students"]),
        h2("Messages from Parents"),
        para("Parents can share these warm wishes to thank teachers for their patience and child guidance."),
        list_block(SECTIONS["parents"]),
        h2("Teacher's Day Lines for WhatsApp Status & Instagram Captions"),
        para("Keep your social media announcements direct and scanable with these quick lines."),
        list_block(SECTIONS["captions"]),
        h2("More Festive & Occasion Reads"),
        para(
            'Explore our other occasion guides including <a href="https://blog.bluestone.com/heart-touching-love-proposal-quotes-2027/">proposal quotes for 2027</a>, '
            '<a href="https://blog.bluestone.com/happy-holi-wishes-messages-quotes-2027/">Holi wishes for 2027</a>, '
            '<a href="https://blog.bluestone.com/happy-diwali-wishes-messages-quotes-2026/">Diwali wishes for 2026</a>, '
            '<a href="https://blog.bluestone.com/happy-eid-mubarak-wishes-messages-quotes-2027/">Eid wishes for 2027</a>, '
            '<a href="https://blog.bluestone.com/happy-childrens-day-best-wishes-quotes-messages-for-kids/">Children\'s Day quotes for 2026</a>, and '
            '<a href="https://blog.bluestone.com/engagement-quotes/">engagement quotes for 2026</a>.'
        ),
        faq_html,
        h2("Conclusion"),
        para(
            "The best teachers day wishes in english are simple, respectful, and highlight the daily guidance mentors offer. "
            "Choose a message that fits your relationship, personalize it with a name or memory, and share it with gratitude. Happy Teachers' Day 2026!"
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
            "teachers day wishes in english",
            "teachers day message",
            "happy teachers day wishing quotes",
            "happy teachers day wishes quotes",
            "best teachers day quotes",
            "heart touching teachers day wishes",
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
        "carousel_mid_article": content.index("bs-cf-teachers") < content.index("Frequently Asked Questions"),
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
    assets = ROOT / "output/Week1_Rank10_TeachersDay_assets"
    assets.mkdir(parents=True, exist_ok=True)

    product_media = []
    for product in PRODUCTS:
        if not product["png"].exists():
            raise SystemExit(f"Missing approved Type 2 image: {product['png']}")
        filename = re.sub(r"[^A-Za-z0-9]+", "-", product["name"]).strip("-").lower() + "-carousel.webp"
        webp = assets / filename
        to_carousel_webp(product["png"], webp)
        alt = f"Teachers' Day 2026 gift idea: {product['name']} from BlueStone"
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
    (ROOT / "output/Week1_Rank10_TeachersDay_article.html").write_text(content)
    (ROOT / "output/Week1_Rank10_TeachersDay_product_media.json").write_text(
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
