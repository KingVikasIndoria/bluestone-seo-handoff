#!/usr/bin/env python3
"""Publish/Optimize Week 1 Rank 9: Raksha Bandhan Wishes & Quotes (WP #14317)."""
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

POST_ID = 14317
TITLE = "100+ Happy Raksha Bandhan Quotes, Wishes & Messages for 2026"
SLUG = "raksha-bandhan-quotes-in-english"
META_DESC = (
    "Find 100+ Happy Raksha Bandhan quotes, wishes and messages in English for 2026. "
    "Perfect for brothers, sisters, funny wishes, long-distance cards, WhatsApp and Instagram. Ready to share."
)
FOCUS_KW = "raksha bandhan quotes in english"
YOAST_TITLE = "Happy Raksha Bandhan Quotes, Wishes & Messages 2026 | BlueStone"
LIVE_URL = f"https://blog.bluestone.com/{SLUG}/"

PRODUCTS = [
    {
        "code": "BISV0910V12",
        "name": "The Bandhan Bracelet For Him",
        "url": "https://www.bluestone.com/bracelets/the-bandhan-bracelet-for-him~112002.html",
        "png": ROOT / "ProductImages/raw/Bracelets/The Bandhan Bracelet For Him.jpg",
    },
    {
        "code": "BISV0910V26",
        "name": "The Network Link Bracelet",
        "url": "https://www.bluestone.com/bracelets/the-network-link-bracelet~108784.html",
        "png": ROOT / "ProductImages/raw/Bracelets/The Network Link Bracelet.jpg",
    },
    {
        "code": "BISL0987V71",
        "name": "The Elize Evil Eye Bracelet",
        "url": "https://www.bluestone.com/bracelets/the-elize-evil-eye-bracelet~121012.html",
        "png": ROOT / "ProductImages/raw/Bracelets/The Elize Evil Eye Bracelet.jpg",
    },
    {
        "code": "BIAV0865V25",
        "name": "The Malocchio Charm Holder Bracelet",
        "url": "https://www.bluestone.com/bracelets/the-malocchio-charm-holder-bracelet~95653.html",
        "png": ROOT / "ProductImages/raw/Bracelets/The Malocchio Charm Holder Bracelet.jpg",
    },
    {
        "code": "BIAV0865V24",
        "name": "The Pervinca Charm Holder Bracelet",
        "url": "https://www.bluestone.com/bracelets/the-pervinca-charm-holder-bracelet~103133.html",
        "png": ROOT / "ProductImages/raw/Bracelets/The Pervinca Charm Holder Bracelet.jpg",
    },
    {
        "code": "BIMG0635V45",
        "name": "The Shining Star Bracelet",
        "url": "https://www.bluestone.com/bracelets/the-shining-star-bracelet~63731.html",
        "png": ROOT / "ProductImages/raw/Bracelets/The Shining Star Bracelet.jpg",
    },
]

SECTIONS = {
    "brother": [
        "To my brother, thank you for being the quiet strength and constant support in my life.",
        "May this Rakhi bring you all the success, happiness, and peace of mind you deserve.",
        "Happy Raksha Bandhan, brother! May your journey be smooth and your goals be achieved.",
        "Wishing a wonderful Raksha Bandhan to my brother, who has always kept his promise to protect and support me.",
        "May the bond we share grow stronger and more resilient with every passing Rakhi.",
        "No matter the distance, you are always the first person I count on. Happy Rakhi, bhaiya!",
        "May the thread of Rakhi protect you from all harm and bring daily joy to your life.",
        "To a brother who values family, integrity, and daily kindness. Happy Raksha Bandhan!",
    ],
    "sister": [
        "To my sweet sister, wishing you a happy Raksha Bandhan filled with laughter and peace.",
        "May your life be brightened with new opportunities and lasting joy this Rakhi.",
        "Thank you for being my constant guide, critic, and best friend. Happy Raksha Bandhan, sister!",
        "May this Rakhi bring you confidence, success, and the daily strength to reach your dreams.",
        "Wishing you a beautiful Rakhi celebration, sending love and return gifts your way.",
        "No matter how much we argue, you will always be my favorite sister. Happy Rakhi!",
        "May the blessings of this holy festival keep your life peaceful and secure.",
        "To my sister, sending warm thoughts and wishes for a happy, healthy year ahead.",
    ],
    "short_quotes": [
        "A sibling is a lifelong friend, a shared history, and a promise for the future.",
        "Rakhi is a thread that binds two lives in a circle of love, protection, and daily respect.",
        "Sisters and brothers are as close as hands and feet.",
        "The bond between a brother and sister is a sanctuary in a busy world.",
        "A promise made on Raksha Bandhan is a commitment that outlasts all seasons.",
        "To have a loving sibling is to have a constant anchor in life.",
        "Rakhi purnima wishes remind us of the quiet strength of family ties.",
        "A thread of protection is the strongest shield against life's challenges.",
        "Love is the core, protection is the promise, and family is the circle.",
        "Grateful for the shared stories and the quiet support that needs no words.",
    ],
    "emotional": [
        "May the thread of Rakhi always serve as a reminder of our childhood laughter and shared dreams.",
        "Thank you for standing by me when the world felt complicated. Happy Raksha Bandhan.",
        "Our relationship is built on silent understanding, mutual respect, and infinite care.",
        "Wishing you a meaningful Raksha Bandhan, reflecting on a bond that has shaped who I am today.",
        "No matter where life takes us, the promise of this thread remains unchanged and secure.",
        "May this Raksha Bandhan bring peace to your heart and brightness to your future.",
        "Holding onto our childhood memories, wishing you a warm and emotional Rakhi.",
    ],
    "funny": [
        "Happy Raksha Bandhan! Please accept my wishes and remember that you owe me a return gift.",
        "Congratulations on having the most patient and smart sibling in the world. You are welcome!",
        "Happy Rakhi! May your patience survive my teasing for another year.",
        "Here's to the thread that legally allows me to claim half of your chocolates. Happy Rakhi!",
        "Happy Raksha Bandhan! Let us promise to keep each other's secrets, especially from our parents.",
        "Merry Rakhi! May your pocket be lightened and my gift bag be filled today.",
    ],
    "long_distance": [
        "Miles cannot weaken the promise of this thread. Sending you a warm Rakhi from afar.",
        "Missing the Rakhi ceremony, the sweets, and your teasing. Happy Raksha Bandhan, brother!",
        "Though we are far apart, my prayers for your health and success are always with you.",
        "Sending this Rakhi across the distance, carrying the same love and care as always.",
        "Distance only reminds us how precious our childhood bond truly is. Happy Raksha Bandhan!",
        "Wish I could tie this Rakhi in person today, sending you virtual hugs and blessings.",
    ],
    "purnima": [
        "Wishing you a blessed Rakhi Purnima filled with family gatherings and festive joy.",
        "May the full moon of Rakhi Purnima illuminate your path with peace and prosperity.",
        "Sending sincere Rakhi Purnima wishes to you and your loved ones. Happy Raksha Bandhan!",
        "May this holy day bring clean hopes, positive energy, and spiritual strength to your home.",
        "Grateful to celebrate Rakhi Purnima, reflecting on the protective bonds that keep us secure.",
        "Let the light of the full moon bring peace and daily joy to your family.",
    ],
    "captions": [
        "Thread of protection, bond of a lifetime. Jai Hind!",
        "Happy Raksha Bandhan! Celebrating my constant support system.",
        "Arguments in the morning, Rakhi in the afternoon. Sisterhood at its best.",
        "A quiet promise of safety, protection, and daily respect.",
        "Sibling bond: tested by teasing, secured by love.",
        "Happy Rakhi Purnima! Grateful for the home traditions.",
        "He asked for a simple thread, she gave him a lifetime promise.",
        "Return gifts are ready, and so am I. Happy Raksha Bandhan!",
        "A thread that carries a history of shared laughter.",
        "Bonds that keep us anchored. Happy Rakhi 2026!",
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
        alt = f"Raksha Bandhan 2026 gift idea: {product['name']} from BlueStone"
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
    script = script.replace("bs-cf-eid", "bs-cf-rakhi")
    return (
        "<!-- wp:html -->\n<style>\n"
        + style
        + '\n</style>\n<div class="bs-cf" id="bs-cf-rakhi" data-interval="3200" aria-roledescription="carousel" aria-label="BlueStone Raksha Bandhan gift ideas">\n'
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
            "What are the best raksha bandhan quotes in english for 2026?",
            "The best Raksha Bandhan quotes in English focus on the lifetime commitment between siblings. For example: “Rakhi is a thread that binds two lives in a circle of love, protection, and daily respect.” These quotes work beautifully for card entries or text wishes.",
        ),
        (
            "What is a short happy Rakhi wish for brother?",
            "A short wish is: “To my brother, thank you for being the quiet strength and constant support in my life. Happy Rakhi 2026!” It is direct, personal, and easy to share on WhatsApp.",
        ),
        (
            "How do I wish a happy Rakhi purnima to my family?",
            "For family, you can say: “Wishing you a blessed Rakhi Purnima filled with family gatherings and festive joy.” Sibling ceremonies celebrate the broader supportive circle of the family.",
        ),
        (
            "What is a unique quotation on raksha bandhan in english?",
            "A unique quotation is: “A sibling is a lifelong friend, a shared history, and a promise for the future.” It highlights both childhood memories and the ongoing support that brother-sister relationships offer.",
        ),
        (
            "What is a good caption for a Rakhi post on Instagram?",
            "A popular caption is: “Thread of protection, bond of a lifetime. Happy Raksha Bandhan!” Keeping captions brief allows the photo showing the tied thread to tell the main story.",
        ),
        (
            "What is a warm long-distance Rakhi quote for a brother?",
            "For a long-distance brother, write: “Miles cannot weaken the promise of this thread. Sending you a warm Rakhi and prayers from afar.” It keeps the connection strong regardless of physical distance.",
        ),
    ]
    html = [h2("Frequently Asked Questions about Raksha Bandhan Quotes")]
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
            "Looking for the best <strong>raksha bandhan quotes in english</strong>, wishes, and greetings to share in 2026? "
            "Whether you are wishing a brother or sister, writing a festive card, sending a message across the distance, or looking for an Instagram caption, this collection has you covered."
        ),
        para(
            "<strong>TL;DR:</strong> Pick a warm wish for your brother or sister, a short quotation for a card, an emotional message, "
            "or a dedicated caption for Instagram and WhatsApp status. Every list is updated for Rakshabandhan 2026."
        ),
        para(
            "Raksha Bandhan celebrates a promise of safety, protection, and mutual respect. Sincere words help keep the festive spirit alive."
        ),
        h2("Happy Rakhi Wishes for Brother"),
        para("Send these warm happy Rakhi wishes to your brother to show your appreciation for his support."),
        list_block(SECTIONS["brother"]),
        h2("Sweet Raksha Bandhan Wishes for Sister"),
        para("Celebrate your sister with these sweet Raksha Bandhan wishes and greetings."),
        list_block(SECTIONS["sister"]),
        h2("Short Rakhi Quotes in English"),
        para("These short quotes are perfect for card headings, guest books, or elegant posts."),
        list_block(SECTIONS["short_quotes"]),
        h2("Emotional Raksha Bandhan Messages"),
        para("These emotional messages focus on childhood memories, shared laughter, and the security of family bonds."),
        list_block(SECTIONS["emotional"]),
        h2("A Beautiful Keepsake for Raksha Bandhan"),
        para(
            "If you are pairing your wishes with a token of care, modern gold and diamond bracelets make excellent keepsakes. "
            "Whether it is a classic diamond link bracelet, a traditional charm holder, or a plain gold star style, select something they can wear daily as a reminder of your bond. "
            "Here are six approved bracelet return-gift ideas from the BlueStone collection."
        ),
        carousel,
        h2("Funny and Light-Hearted Rakhi Wishes"),
        para("Keep the sibling teasing alive with these funny Rakhi messages."),
        list_block(SECTIONS["funny"]),
        h2("Long-Distance Rakhi Messages"),
        para("Send these wishes across the distance to let your brother or sister know they are always in your thoughts."),
        list_block(SECTIONS["long_distance"]),
        h2("Rakhi Purnima Wishes & Greetings"),
        para("Celebrate the auspicious day of Rakhi Purnima with these traditional wishes for your family."),
        list_block(SECTIONS["purnima"]),
        h2("Rakhi Quotes for WhatsApp Status & Instagram Captions"),
        para("Keep your social media announcements clean and direct with these quick captions."),
        list_block(SECTIONS["captions"]),
        h2("More Festive & Occasion Reads"),
        para(
            'Explore our other guides including <a href="https://blog.bluestone.com/heart-touching-love-proposal-quotes-2027/">proposal quotes for 2027</a>, '
            '<a href="https://blog.bluestone.com/happy-holi-wishes-messages-quotes-2027/">Holi wishes for 2027</a>, '
            '<a href="https://blog.bluestone.com/happy-diwali-wishes-messages-quotes-2026/">Diwali wishes for 2026</a>, '
            '<a href="https://blog.bluestone.com/happy-eid-mubarak-wishes-messages-quotes-2027/">Eid wishes for 2027</a>, '
            '<a href="https://blog.bluestone.com/happy-childrens-day-best-wishes-quotes-messages-for-kids/">Children\'s Day quotes for 2026</a>, and '
            '<a href="https://blog.bluestone.com/engagement-quotes/">engagement quotes for 2026</a>.'
        ),
        faq_html,
        h2("Conclusion"),
        para(
            "The right raksha bandhan quotes in english are sincere, simple to share, and celebrate a lifelong promise. "
            "Choose a message that fits your relationship, personalize it with a name or memory, and share it with love. Happy Raksha Bandhan 2026!"
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
            "raksha bandhan quotes in english",
            "rakhi purnima wishes",
            "rakhi quotes in english",
            "quotation on raksha bandhan in english",
            "rakhi quotes for brother",
            "rakhi quotation",
            "rakhi quotes",
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
        "carousel_mid_article": content.index("bs-cf-rakhi") < content.index("Frequently Asked Questions"),
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
    assets = ROOT / "output/Week1_Rank9_RakshaBandhan_assets"
    assets.mkdir(parents=True, exist_ok=True)

    product_media = []
    for product in PRODUCTS:
        if not product["png"].exists():
            raise SystemExit(f"Missing approved Type 2 image: {product['png']}")
        filename = re.sub(r"[^A-Za-z0-9]+", "-", product["name"]).strip("-").lower() + "-carousel.webp"
        webp = assets / filename
        to_carousel_webp(product["png"], webp)
        alt = f"Raksha Bandhan 2026 gift idea: {product['name']} from BlueStone"
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
    (ROOT / "output/Week1_Rank9_RakshaBandhan_article.html").write_text(content)
    (ROOT / "output/Week1_Rank9_RakshaBandhan_product_media.json").write_text(
        json.dumps(product_media, indent=2)
    )

    # Post to WP under ID 14317 and slug raksha-bandhan-quotes-in-english (Optimize flow)
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
