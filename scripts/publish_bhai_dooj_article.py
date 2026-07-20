#!/usr/bin/env python3
"""Publish Week 1 Rank 15: Bhai Dooj Wishes (New post)."""
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

TITLE = "100+ Happy Bhai Dooj Wishes, Quotes & Messages in English for 2026"
SLUG = "bhai-dooj-wishes"
META_DESC = (
    "Explore 100+ Happy Bhai Dooj wishes in english, bhaubeej wish messages, bhai dhooj quotes, "
    "and Instagram captions for 2026. Perfect for brothers, sisters, WhatsApp and cards. Ready to copy."
)
FOCUS_KW = "bhai dooj wishes"
YOAST_TITLE = "Happy Bhai Dooj Wishes, Quotes & Messages 2026 | BlueStone"
LIVE_URL = f"https://blog.bluestone.com/{SLUG}/"

PRODUCTS = [
    {
        "code": "BISV0910V12",
        "name": "The Bandhan Bracelet For Him",
        "url": "https://www.bluestone.com/bracelets/the-bandhan-bracelet-for-him~112002.html",
        "png": ROOT / "ProductImages/seo images/Bracelet/The Bandhan Bracelet For Him.png",
    },
    {
        "code": "BISV0910V26",
        "name": "The Network Link Bracelet",
        "url": "https://www.bluestone.com/bracelets/the-network-link-bracelet~108784.html",
        "png": ROOT / "ProductImages/seo images/Bracelet/The Network Link Bracelet.png",
    },
    {
        "code": "BISL0987V71",
        "name": "The Elize Evil Eye Bracelet",
        "url": "https://www.bluestone.com/bracelets/the-elize-evil-eye-bracelet~121012.html",
        "png": ROOT / "ProductImages/seo images/Bracelet/The Elize Evil Eye Bracelet.png",
    },
    {
        "code": "BIAV0865V25",
        "name": "The Malocchio Charm Holder Bracelet",
        "url": "https://www.bluestone.com/bracelets/the-malocchio-charm-holder-bracelet~95653.html",
        "png": ROOT / "ProductImages/seo images/Bracelet/The Malocchio Charm Holder Bracelet.png",
    },
    {
        "code": "BIMG0635V45",
        "name": "The Shining Star Bracelet",
        "url": "https://www.bluestone.com/bracelets/the-shining-star-bracelet~63731.html",
        "png": ROOT / "ProductImages/seo images/Bracelet/The Shining Star Bracelet.png",
    },
    {
        "code": "BIHM1002V07",
        "name": "The Protector Evil Eye Rakhi",
        "url": "https://www.bluestone.com/adjustable+bracelets/the-protector-evil-eye-rakhi~114521.html",
        "png": ROOT / "ProductImages/seo images/Adjustable Bracelets/The Protector Evil Eye Rakhi.png",
    },
]

SECTIONS = {
    "short": [
        "Wishing you a very Happy Bhai Dooj! May our bond stay strong, joyful, and full of trust.",
        "Happy Bhai Dooj to the best brother in the world. Grateful for your protection and love.",
        "On this Bhai Dooj, I pray for your health, success, and endless happiness. Love you always.",
        "May the tilak of Bhai Dooj bring prosperity and peace into your life. Happy Bhaubeej!",
        "Sending warm Bhai Dooj wishes and sweet blessings for a bright year ahead.",
        "Happy Bhai Dooj! Thank you for being my lifelong friend, guide, and protector.",
        "May Lord Yama bless our sibling bond with longevity and joy. Happy Bhai Dooj 2026!",
        "To my dear brother, wishing you laughter, strength, and success on Bhai Dooj and always.",
    ],
    "brother": [
        "Dear brother, on Bhai Dooj I thank you for every sacrifice, every laugh, and every quiet act of care.",
        "You are my first hero and my forever friend. Happy Bhai Dooj with all my love.",
        "May this Bhai Dooj strengthen the promise that I will always stand by you, just as you stand by me.",
        "Brother, your guidance has shaped who I am. Wishing you health, wealth, and peace this Bhai Dooj.",
        "From childhood fights to adult support, our bond only grows. Happy Bhai Dooj to my rock.",
        "I am lucky to call you my brother. May Bhai Dooj fill your home with joy and sweet moments.",
        "On Bhai Dooj, I pray that every dream you carry finds its way to success. Proud of you always.",
        "Thank you for protecting my smile even when life felt heavy. Happy Bhai Dooj, dear bhaiya.",
    ],
    "english": [
        "Happy Bhai Dooj in English for every card: May our sibling love outshine every challenge this year.",
        "A simple Bhaubeej wish: May your path stay clear, your heart stay light, and your home stay blessed.",
        "Bhai Dooj message for WhatsApp: Grateful for a brother who turns ordinary days into celebrations.",
        "English Bhai Dooj greeting: May the festival of tilak and sweets remind us how rare true siblings are.",
        "Copy-ready Bhai Dooj msg: Wishing you success, safety, and smiles that never fade.",
        "Happy Bhai Dooj wishes in english for family groups: Love, loyalty, and laughter to you always.",
        "Bhaubeej wish for your brother: May every new chapter bring you closer to your goals.",
        "Short Bhai Dooj message in english: You are my blessing, my pride, and my forever friend.",
    ],
    "quotes": [
        "A brother is a friend given by nature, and Bhai Dooj is the day we celebrate that gift openly.",
        "Sibling love is the thread that survives distance, time, and every storm. Happy Bhai Dooj.",
        "On Bhai Dooj we do not just apply tilak; we renew a promise of protection and trust.",
        "Brothers and sisters share memories no one else can understand. Cherish them today and always.",
        "The best bhai dhooj quotes speak from the heart: thank you for being my constant.",
        "Distance may separate us, but Bhai Dooj keeps our bond alive in every message we send.",
        "A sister's prayer on Bhai Dooj: may my brother's courage never fade and his smile never dim.",
        "True siblings do not need perfect words, only honest love. Happy Bhaubeej to mine.",
    ],
    "captions": [
        "Happy Bhai Dooj captions for Instagram: Tilak, sweets, and a brother worth celebrating.",
        "Bhai Dooj status: Some bonds are written in childhood and sealed with love every year.",
        "Caption idea: Not all superheroes wear capes; some share your last name. Happy Bhai Dooj.",
        "Instagram Bhai Dooj line: Same family, same memories, same unconditional love.",
        "Status for Bhai Dooj: Grateful for the one who taught me strength and kindness.",
        "Caption for reels: From pranks to protection, this bond is my favourite story.",
    ],
    "funny": [
        "Happy Bhai Dooj! Thanks for stealing my snacks and still expecting a gift from me.",
        "To my brother: I tolerate you 364 days a year, but today I actually mean the sweet wishes.",
        "Bhai Dooj reminder: I applied tilak, you owe me lifetime loyalty and unlimited chai runs.",
        "Happy Bhaubeej to the guy who knows all my secrets and still chooses to stay related.",
    ],
    "long_distance": [
        "Miles apart but never far in heart. Sending Bhai Dooj wishes across every distance between us.",
        "Even if we cannot share tilak today, my prayers and love reach you wherever you are.",
        "Long-distance Bhai Dooj message: Our bond does not need a shared address to stay strong.",
        "Missing you on Bhai Dooj, brother. Save me a sweet and know I am thinking of you.",
    ],
    "cousins": [
        "Happy Bhai Dooj to my cousin-brother who feels just like real sibling love.",
        "To the cousin who grew up like a brother, wishing you joy, health, and success this Bhaubeej.",
        "Cousin bonds deserve Bhai Dooj wishes too: thank you for every festival memory we share.",
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
        alt = f"Bhai Dooj 2026 gift idea: {product['name']} from BlueStone"
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
    script = script.replace("bs-cf-eid", "bs-cf-bhaidooj")
    return (
        "<!-- wp:html -->\n<style>\n"
        + style
        + '\n</style>\n<div class="bs-cf" id="bs-cf-bhaidooj" data-interval="3200" aria-roledescription="carousel" aria-label="BlueStone Bhai Dooj gift ideas">\n'
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
            "What are the best bhai dooj wishes in english?",
            "The best bhai dooj wishes in english are short, heartfelt lines you can copy for cards or WhatsApp: "
            "“Wishing you a very Happy Bhai Dooj! May our bond stay strong, joyful, and full of trust.” "
            "Keep the tone warm and personal for brothers and sisters.",
        ),
        (
            "What is a good bhaubeej wish for my brother?",
            "Write: “Dear brother, on Bhai Dooj I thank you for every sacrifice and every laugh. "
            "May this festival bring you health, success, and peace.” A bhaubeej wish works best when it mentions protection and gratitude.",
        ),
        (
            "What are popular bhai dhooj quotes for Instagram?",
            "Try: “Sibling love is the thread that survives distance, time, and every storm. Happy Bhai Dooj.” "
            "Pair bhai dhooj quotes with a simple photo and a festive hashtag for captions and status updates.",
        ),
        (
            "How do I write a happy bhai dooj message for WhatsApp?",
            "Keep it under three lines: greeting, one emotional line, and a closing blessing. "
            "Example: “Happy Bhai Dooj! Grateful for your protection and love. May Lord Yama bless our bond.”",
        ),
        (
            "Can I send Bhai Dooj wishes to a cousin?",
            "Yes. Cousin bonds deserve Bhai Dooj wishes too. Write: “Happy Bhai Dooj to my cousin-brother who feels just like real sibling love.”",
        ),
        (
            "What is a thoughtful Bhai Dooj gift idea from BlueStone?",
            "Gold bracelets and adjustable rakhis such as The Bandhan Bracelet For Him or The Protector Evil Eye Rakhi "
            "make meaningful sibling keepsakes that last beyond the festival.",
        ),
    ]
    html = [h2("Frequently Asked Questions about Bhai Dooj Wishes")]
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
            "Looking for the best <strong>bhai dooj wishes</strong>, quotes, and messages to share with your brother or sister? "
            "Whether you need short WhatsApp lines, emotional bhai dhooj quotes, bhaubeej wish notes, or happy bhai dooj captions for Instagram, "
            "this collection covers every sibling moment."
        ),
        para(
            "<strong>TL;DR:</strong> Copy a quick Bhai Dooj wish for a card, a heartfelt message for your brother, "
            "an English bhaubeej line for family chat, or a caption for social media. All lists are updated for Bhai Dooj 2026."
        ),
        para(
            "Bhai Dooj celebrates the protective bond between brothers and sisters. A sincere message, tilak ritual, or a lasting gold bracelet "
            "can turn the festival into a memory your sibling keeps all year."
        ),
        h2("Short Happy Bhai Dooj Wishes for WhatsApp"),
        para("Keep your greetings direct and scanable with these quick, copy-ready bhai dooj msg lines."),
        list_block(SECTIONS["short"]),
        h2("Heartfelt Bhai Dooj Wishes for Your Brother"),
        para("Send these warm, respectful wishes to thank your brother for his protection, guidance, and daily support."),
        list_block(SECTIONS["brother"]),
        h2("Happy Bhai Dooj Messages & Bhaubeej Wishes in English"),
        para("Use these bhai dooj wishes in english for cards, family chats, and festival greetings."),
        list_block(SECTIONS["english"]),
        h2("Emotional Bhai Dooj Quotes & Bhai Dhooj Quotes"),
        para("These bhai dhooj quotes and bhaubeej wish lines celebrate the rare gift of lifelong sibling trust."),
        list_block(SECTIONS["quotes"]),
        h2("A Soft Bhai Dooj Gift Idea (If You Are Gifting Too)"),
        para(
            "Bhai Dooj is a beautiful time to mark sibling love with something lasting. "
            "Gold bracelets and protective rakhis make thoughtful keepsakes that outlast the sweets and tilak. "
            "Explore these six approved designs from the BlueStone collection."
        ),
        carousel,
        h2("Happy Bhai Dooj Captions for Instagram & Status"),
        para("Pair these happy bhai dooj captions for instagram with your favourite sibling photo or reel."),
        list_block(SECTIONS["captions"], ordered=False),
        h2("Funny Bhai Dooj Wishes"),
        para("Lighten the mood with these playful lines for siblings who share inside jokes."),
        list_block(SECTIONS["funny"]),
        h2("Long-Distance Bhai Dooj Messages"),
        para("Send love across cities with these long-distance bhai dooj message ideas."),
        list_block(SECTIONS["long_distance"]),
        h2("Bhai Dooj Wishes for Cousins"),
        para("Include cousin-brothers and cousin-sisters with these warm bhaubeej greetings."),
        list_block(SECTIONS["cousins"]),
        h2("More Festive & Occasion Reads"),
        para(
            'Explore our other guides including <a href="https://blog.bluestone.com/raksha-bandhan-quotes-in-english/">Raksha Bandhan quotes for 2026</a>, '
            '<a href="https://blog.bluestone.com/happy-diwali-wishes-messages-quotes-2026/">Diwali wishes for 2026</a>, '
            '<a href="https://blog.bluestone.com/happy-holi-wishes-messages-quotes-2027/">Holi wishes for 2027</a>, '
            '<a href="https://blog.bluestone.com/friendship-day-2023-wishes/">Friendship Day wishes for 2026</a>, '
            '<a href="https://blog.bluestone.com/ganesh-chaturthi-wishes-in-english/">Ganesh Chaturthi wishes for 2026</a>, '
            '<a href="https://blog.bluestone.com/dussehra-wishes-in-english/">Dussehra wishes for 2026</a>, and '
            '<a href="https://blog.bluestone.com/happy-fathers-day-wishes-quotes-and-messages-for-every-dad/">Father\'s Day quotes for 2026</a>. '
            'Learn more about <a href="https://en.wikipedia.org/wiki/Bhai_Dooj">Bhai Dooj on Wikipedia</a>.'
        ),
        faq_html,
        h2("Conclusion"),
        para(
            "The best bhai dooj wishes focus on gratitude, protection, and shared memories. "
            "Pick a message that fits your bond, personalize it, and share it with love. Happy Bhai Dooj 2026!"
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
            "bhai dooj wishes",
            "bhai dooj wishes in english",
            "bhaubeej wish",
            "bhai dhooj quotes",
            "happy bhai dooj captions for instagram",
            "bhai dooj message",
            "bhai dooj wishes for brother",
            "bhai dooj msg",
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
        "carousel_mid_article": content.index("bs-cf-bhaidooj") < content.index("Frequently Asked Questions"),
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
    assets = ROOT / "output/Week1_Rank15_BhaiDooj_assets"
    assets.mkdir(parents=True, exist_ok=True)

    product_media = []
    for product in PRODUCTS:
        if not product["png"].exists():
            raise SystemExit(f"Missing approved Type 2 image: {product['png']}")
        filename = re.sub(r"[^A-Za-z0-9]+", "-", product["name"]).strip("-").lower() + "-carousel.webp"
        webp = assets / filename
        to_carousel_webp(product["png"], webp)
        alt = f"Bhai Dooj 2026 gift idea: {product['name']} from BlueStone"
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
    (ROOT / "output/Week1_Rank15_BhaiDooj_article.html").write_text(content)
    (ROOT / "output/Week1_Rank15_BhaiDooj_product_media.json").write_text(json.dumps(product_media, indent=2))

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

    manifest_path = ROOT / "output/Week1_Rank15_BhaiDooj_type3_prompts.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["wp_post_id"] = post["id"]
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
