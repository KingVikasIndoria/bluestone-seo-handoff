#!/usr/bin/env python3
"""Optimize Week 1 Rank 16: Valentine's Hubby Quotes (WP #18888)."""
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

POST_ID = 18888
TITLE = "100+ Valentine's Hubby Quotes, Wishes & Messages for Husband 2027"
SLUG = "romantic-valentines-day-wishes-quotes-celebrate-love-in-the-most-beautiful-way"
META_DESC = (
    "Find 100+ valentines hubby quotes, valentine quotes for husband, and heart touching "
    "Valentine's Day wishes for husband in 2027. Ready to copy for cards, WhatsApp and Instagram."
)
FOCUS_KW = "valentines hubby quotes"
YOAST_TITLE = "Valentine's Hubby Quotes & Wishes for Husband 2027 | BlueStone"
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
    "short": [
        "Happy Valentine's Day to my husband. You are my calm, my courage, and my favourite forever.",
        "To my hubby, thank you for choosing us every day. Happy Valentine's Day 2027!",
        "My love, you make ordinary mornings feel special. Happy Valentine's Day, husband.",
        "Wishing my husband a Valentine's Day filled with laughter, rest, and quiet love.",
        "Happy Valentine's Day to the man who turned my life into home.",
        "To my hubby: still my favourite person, still my safest place. Happy Valentine's Day.",
        "Husband, your love is my daily blessing. Happy Valentine's Day with all my heart.",
        "Happy Valentine's Day, my love. Grateful for every quiet promise you keep.",
    ],
    "heart": [
        "To my husband, thank you for loving me in the small moments when no one else is watching.",
        "Happy Valentine's Day to the man who holds my hand through every storm and every soft Sunday.",
        "You are not just my husband. You are my best friend, my steady light, and my home.",
        "Heart touching Valentine's Day wishes for husband: may our love stay gentle, honest, and strong.",
        "Dear hubby, every year with you feels like a new beginning I am lucky to share.",
        "I chose you once, and I choose you every day after. Happy Valentine's Day, my husband.",
        "Thank you for the patience, the humour, and the quiet ways you protect our peace.",
        "My husband, your love made ordinary life feel extraordinary. Happy Valentine's Day 2027.",
    ],
    "hubby_quotes": [
        "A good husband is not the one who never fails. He is the one who never stops trying for love.",
        "Valentines hubby quotes start simple: you are my favourite yes, my safest no, and my forever home.",
        "Marriage grows beautiful when a husband listens with his heart, not just his ears.",
        "To my hubby: loving you is the easiest habit I never want to break.",
        "Valentine quotes for husband: your quiet strength makes my world feel steadier every day.",
        "A husband who laughs with you is a treasure. A husband who stays is a blessing.",
        "My hubby is proof that the best love stories are built one ordinary day at a time.",
        "Valentines day quotes for husband should feel true: thank you for being both romance and refuge.",
    ],
    "my_love": [
        "Happy Valentine's Day to my love. You are the reason every ordinary day feels worth celebrating.",
        "Valentines day quotes for my love: thank you for the soft way you stay.",
        "My love, you are my favourite conversation, my calm morning, and my favourite forever.",
        "To my love: distance, time, and noise never change how surely I choose you.",
        "Valentine's day quotes for my love should sound like this: you still feel like home.",
        "My love, your smile is the first place I look when the day feels heavy.",
        "Happy Valentine's Day, my love. Grateful for the life we keep building together.",
        "For my love: every chapter with you is the one I want to reread.",
    ],
    "captions": [
        "Valentine's caption for husband: Still my favourite person. Still my safest place.",
        "Hubby Instagram line: Married my best friend and still choosing him every day.",
        "Status for husband: Love looks like quiet mornings and loud laughter with you.",
        "Caption idea: Not just my husband. My home, my calm, my forever yes.",
        "Valentine reel line: Soft love, strong vows, and a hubby who stays.",
        "Status for my love: Grateful for the man who makes forever feel easy.",
    ],
    "funny": [
        "Happy Valentine's Day, hubby. Thanks for loving me even when I steal the blanket and the last bite.",
        "To my husband: I married you for love, and I stay for the snacks and the jokes.",
        "Valentine wish for hubby: may our WiFi stay strong and our arguments stay short.",
        "Husband, you are my favourite notification, even when you leave socks everywhere.",
    ],
    "long_distance": [
        "Miles apart, still my husband in every heartbeat. Happy Valentine's Day, my love.",
        "Long-distance Valentine's message for husband: our love does not need a shared room to feel close.",
        "Missing you today, hubby. Saving every hug for the day we meet again.",
        "Distance is temporary. Choosing you is forever. Happy Valentine's Day, husband.",
    ],
    "anniversary_tone": [
        "Happy Valentine's Day to my husband of every season: thank you for growing with me.",
        "To the man I married: our love feels newer every year and steadier every day.",
        "Husband, our story is still my favourite one. Happy Valentine's Day 2027.",
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
        alt = f"Valentine's Day 2027 gift idea: {product['name']} from BlueStone"
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
    script = script.replace("bs-cf-eid", "bs-cf-valentines")
    return (
        "<!-- wp:html -->\n<style>\n"
        + style
        + '\n</style>\n<div class="bs-cf" id="bs-cf-valentines" data-interval="3200" aria-roledescription="carousel" aria-label="BlueStone Valentine gift ideas for him">\n'
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
            "What are the best valentines hubby quotes?",
            "The best valentines hubby quotes are short, honest, and personal: "
            "“To my hubby: loving you is the easiest habit I never want to break.” "
            "Pair a quote with one specific memory for a stronger card note.",
        ),
        (
            "What are good valentine quotes for husband?",
            "Try: “Valentine quotes for husband should feel true: thank you for being both romance and refuge.” "
            "Keep the tone warm and grounded rather than overly dramatic.",
        ),
        (
            "How do I write heart touching Valentine's Day wishes for husband?",
            "Start with gratitude, name one quality you love, and close with a blessing. "
            "Example: “Thank you for loving me in the small moments. Happy Valentine's Day, my husband.”",
        ),
        (
            "What are romantic valentines day quotes for my love?",
            "Write: “Valentines day quotes for my love should sound like this: you still feel like home.” "
            "These lines work well for WhatsApp, notes, and Instagram captions.",
        ),
        (
            "Can I send funny Valentine's messages to my husband?",
            "Yes. Light humour works when it still feels affectionate. "
            "Example: “Happy Valentine's Day, hubby. Thanks for loving me even when I steal the blanket.”",
        ),
        (
            "What is a thoughtful Valentine's gift idea for him from BlueStone?",
            "Gold chains, band rings, and bracelets for him such as The Tetyana Gold Chain, "
            "The Jasper Band For Him, or The Volara Bracelet For Him make lasting romantic keepsakes.",
        ),
    ]
    html = [h2("Frequently Asked Questions about Valentine's Hubby Quotes")]
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
            "Looking for the best <strong>valentines hubby quotes</strong>, romantic lines for your husband, "
            "and heart touching Valentine's Day wishes for husband? "
            "Whether you need short WhatsApp notes, emotional valentine quotes for husband, "
            "or valentines day quotes for my love, this collection is ready to copy for Valentine's Day 2027."
        ),
        para(
            "<strong>TL;DR:</strong> Copy a short wish for your hubby, a heart touching message for cards, "
            "a quote for Instagram, or a long-distance note. All lists are refreshed for Valentine's Day 2027."
        ),
        para(
            "Valentine's Day is a beautiful reminder that marriage is built in quiet loyalty as much as in grand romance. "
            "A sincere message, and sometimes a lasting gold keepsake for him, can say what hurried days leave unsaid."
        ),
        h2("Short Valentine's Day Wishes for Husband"),
        para("Keep your greetings direct and scanable with these quick, copy-ready lines for your hubby."),
        list_block(SECTIONS["short"]),
        h2("Heart Touching Valentine's Day Wishes for Husband"),
        para("Send these warmer lines when you want gratitude and emotion to lead the message."),
        list_block(SECTIONS["heart"]),
        h2("Valentine's Hubby Quotes & Valentine Quotes for Husband"),
        para("These valentines hubby quotes and valentine's day quotes for husband celebrate steady, everyday love."),
        list_block(SECTIONS["hubby_quotes"]),
        h2("Valentines Day Quotes for My Love"),
        para("Use these valentines day quotes for my love when your message is for your husband and your favourite person."),
        list_block(SECTIONS["my_love"]),
        h2("A Soft Valentine Gift Idea for Him"),
        para(
            "If you are gifting too, Valentine's Day is a beautiful time to mark lasting love with something he can wear every day. "
            "Gold chains, band rings, and bracelets for him make thoughtful keepsakes beyond flowers and cards. "
            "Explore these six approved designs from the BlueStone collection."
        ),
        carousel,
        h2("Valentine's Captions for Instagram & Status"),
        para("Pair these captions with a favourite photo of your husband or a simple couple reel."),
        list_block(SECTIONS["captions"], ordered=False),
        h2("Funny Valentine's Wishes for Husband"),
        para("Lighten the mood with playful lines that still sound affectionate."),
        list_block(SECTIONS["funny"]),
        h2("Long-Distance Valentine's Messages for Husband"),
        para("Send love across cities with these long-distance notes for your hubby."),
        list_block(SECTIONS["long_distance"]),
        h2("Anniversary-Tone Valentine Lines for Married Love"),
        para("For couples who want Valentine's Day to feel like a quiet anniversary of choosing each other again."),
        list_block(SECTIONS["anniversary_tone"]),
        h2("More Festive & Occasion Reads"),
        para(
            'Explore our other guides including <a href="https://blog.bluestone.com/bhai-dooj-wishes/">Bhai Dooj wishes for 2026</a>, '
            '<a href="https://blog.bluestone.com/happy-fathers-day-wishes-quotes-and-messages-for-every-dad/">Father\'s Day quotes for 2026</a>, '
            '<a href="https://blog.bluestone.com/friendship-day-2023-wishes/">Friendship Day wishes for 2026</a>, '
            '<a href="https://blog.bluestone.com/raksha-bandhan-quotes-in-english/">Raksha Bandhan quotes for 2026</a>, '
            '<a href="https://blog.bluestone.com/happy-diwali-wishes-messages-quotes-2026/">Diwali wishes for 2026</a>, '
            '<a href="https://blog.bluestone.com/engagement-quotes/">engagement quotes for 2026</a>, and '
            '<a href="https://blog.bluestone.com/heart-touching-love-proposal-quotes-2027/">proposal quotes for 2027</a>. '
            'Learn more about <a href="https://en.wikipedia.org/wiki/Valentine%27s_Day">Valentine\'s Day on Wikipedia</a>.'
        ),
        faq_html,
        h2("Conclusion"),
        para(
            "The best valentines hubby quotes focus on gratitude, steadiness, and the everyday love that makes marriage feel like home. "
            "Pick a line that sounds like your husband, personalize it, and share it with warmth. Happy Valentine's Day 2027!"
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
        "datePublished": "2021-02-10",
        "dateModified": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "author": {"@type": "Person", "name": "Vikas"},
        "publisher": {"@type": "Organization", "name": "BlueStone", "url": "https://www.bluestone.com/"},
        "image": images,
        "mainEntityOfPage": {"@type": "WebPage", "@id": LIVE_URL},
        "keywords": [
            "valentines hubby quotes",
            "valentine hubby quotes",
            "valentine's day quotes for husband",
            "valentine quotes for husband",
            "valentines day quotes for husband",
            "heart touching valentines day wishes for husband",
            "valentines day quotes for my love",
            "valentine's day quotes for my love",
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
        "carousel_mid_article": content.index("bs-cf-valentines") < content.index("Frequently Asked Questions"),
        "six_buy_links": content.count(">Buy now<") == 6,
        "faq_schema": '"@type": "FAQPage"' in content,
        "blog_schema": '"@type": "BlogPosting"' in content,
        "no_content_h1": "<h1" not in content.lower(),
        "seo_carousel_paths": "carousel-seo" in content or all(
            "seo" in m or "uploads" in m for m in re.findall(r'<img src="([^"]+)"', content)[:6]
        ),
    }
    failed = [name for name, passed in rules.items() if not passed]
    if failed:
        raise SystemExit(f"Content validation failed: {failed}")
    return rules


def main():
    assets = ROOT / "output/Week1_Rank16_ValentinesHubby_assets"
    assets.mkdir(parents=True, exist_ok=True)

    product_media = []
    for product in PRODUCTS:
        if not product["png"].exists():
            raise SystemExit(f"Missing SEO Type 2 image: {product['png']}")
        filename = re.sub(r"[^A-Za-z0-9]+", "-", product["name"]).strip("-").lower() + "-carousel-seo.webp"
        webp = assets / filename
        to_carousel_webp(product["png"], webp)
        alt = f"Valentine's Day 2027 gift idea: {product['name']} from BlueStone"
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
    (ROOT / "output/Week1_Rank16_ValentinesHubby_article.html").write_text(content)
    (ROOT / "output/Week1_Rank16_ValentinesHubby_product_media.json").write_text(json.dumps(product_media, indent=2))

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
