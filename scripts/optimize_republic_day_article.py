#!/usr/bin/env python3
"""Optimize Week 1 Rank 17: Republic Day Shayari & Wishes (WP #18031)."""
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

POST_ID = 18031
TITLE = "100+ Short Shayari on Republic Day in Hindi, Wishes & Quotes for 2027"
SLUG = "26-january-republic-day-wishes-quotes-patriotic-messages"
META_DESC = (
    "Find 100+ short shayari on republic day in hindi, Republic Day wishes, quotes, "
    "and slogans for 26 January 2027. Ready to copy for WhatsApp, Instagram and cards."
)
FOCUS_KW = "short shayari on republic day in hindi"
YOAST_TITLE = "Short Shayari on Republic Day in Hindi & Wishes 2027 | BlueStone"
LIVE_URL = f"https://blog.bluestone.com/{SLUG}/"

PRODUCTS = [
    {
        "code": "BIMG0635V45",
        "name": "The Shining Star Bracelet",
        "url": "https://www.bluestone.com/bracelets/the-shining-star-bracelet~63731.html",
        "png": ROOT / "ProductImages/seo images/Bracelet/The Shining Star Bracelet.png",
    },
    {
        "code": "BISV0910V12",
        "name": "The Bandhan Bracelet For Him",
        "url": "https://www.bluestone.com/bracelets/the-bandhan-bracelet-for-him~112002.html",
        "png": ROOT / "ProductImages/seo images/Bracelet/The Bandhan Bracelet For Him.png",
    },
    {
        "code": "BVEM0663C88",
        "name": "The Tetyana Gold Chain",
        "url": "https://www.bluestone.com/chains/the-tetyana-gold-chain~124927.html",
        "png": ROOT / "ProductImages/seo images/Chains/The Tetyana Gold Chain.png",
    },
    {
        "code": "BIPM0001H28",
        "name": "The Rohal Huggie Earrings",
        "url": "https://www.bluestone.com/earrings/the-rohal-huggie-earrings~21864.html",
        "png": ROOT / "ProductImages/seo images/Earrings/The Rohal Huggie Earrings.png",
    },
    {
        "code": "BISL0851R28",
        "name": "The Jasper Band For Him",
        "url": "https://www.bluestone.com/rings/the-jasper-band-for-him~93964.html",
        "png": ROOT / "ProductImages/seo images/Rings/The Jasper Band For Him.png",
    },
    {
        "code": "BISV0910V26",
        "name": "The Network Link Bracelet",
        "url": "https://www.bluestone.com/bracelets/the-network-link-bracelet~108784.html",
        "png": ROOT / "ProductImages/seo images/Bracelet/The Network Link Bracelet.png",
    },
]

SECTIONS = {
    "shayari": [
        "तिरंगे की शान में सर झुकाते हैं, गणतंत्र दिवस पर हम भारत माता को नमन करते हैं।",
        "आज़ादी की नींव पर खड़ा है यह गणतंत्र, हर भारतीय दिल में बसता है यह गौरव।",
        "26 जनवरी का दिन लाए खुशियाँ अपार, जय हिंद के नारे गूँजें हर बार।",
        "देश की मिट्टी में छिपा है अभिमान, गणतंत्र दिवस पर बढ़े हमारा सम्मान।",
        "तिरंगा फहराए आसमान में ऊँचा, शांति और एकता का संदेश दे हर दिल को।",
        "वीरों के बलिदान से मिला यह अधिकार, गणतंत्र दिवस पर रखें देश का प्यार।",
        "हिंद की शान, हिंद की पहचान, गणतंत्र दिवस पर झूमें हिंदुस्तान।",
        "एकता में बल है हमारा नारा, गणतंत्र दिवस पर यही है हमारा सहारा।",
        "सूरज सा चमकता रहे भारत का नाम, गणतंत्र दिवस पर यही है हमारा संकल्प महान।",
        "वतन की खातिर हर साँस समर्पित, गणतंत्र के पर्व पर गर्व असीमित।",
    ],
    "short_en": [
        "Happy Republic Day 2027! May the tricolour always guide us toward unity and peace.",
        "Wishing you a proud and joyful Republic Day filled with hope for our nation.",
        "On 26 January, we celebrate the Constitution and the courage that built modern India.",
        "Happy Republic Day! May freedom, justice, and equality stay alive in every heart.",
        "Saluting the heroes who shaped our Republic. Jai Hind!",
        "May this Republic Day renew our promise to serve India with honesty and kindness.",
        "Happy Republic Day wishes to you and your family. Proud to be Indian!",
        "Let the tricolour remind us that diversity is our strength. Happy Republic Day 2027.",
    ],
    "quotes": [
        "Republic Day is not only a celebration. It is a reminder of the Constitution we promised to uphold.",
        "A nation becomes strong when its people choose unity over division every ordinary day.",
        "Freedom is our inheritance. Responsibility is our duty. Happy Republic Day.",
        "The tricolour flies for every Indian who believes in justice, liberty, and equality.",
        "True patriotism is quiet service to the country, not only loud slogans on one day.",
        "On Republic Day we honour the dream of a free, fair, and fearless India.",
    ],
    "slogans": [
        "Unity in diversity is India's true strength. Happy Republic Day!",
        "Jai Hind! Let peace and progress lead our Republic.",
        "One nation, many voices, one shared hope. Happy 26 January!",
        "Proud Indian. Strong Republic. Happy Republic Day 2027.",
        "Serve the nation with honesty. Celebrate Republic Day with pride.",
        "Tricolour in our hearts, courage in our steps. Jai Bharat!",
    ],
    "captions": [
        "Republic Day caption: Tricolour vibes and a grateful heart. Jai Hind!",
        "26 January status: Proud of our Constitution, proud of our people.",
        "Instagram line: Celebrating the Republic that belongs to every Indian.",
        "WhatsApp status: Happy Republic Day 2027. Unity first, always.",
        "Caption idea: From every corner of India, one proud greeting: Jai Hind.",
        "Story text: Honour the past. Build a kinder Republic today.",
    ],
    "kids": [
        "Happy Republic Day, little champ! May you grow up loving India with kindness and courage.",
        "Dear child, the tricolour teaches us to be brave, honest, and caring. Happy Republic Day!",
        "Wishing young India a bright Republic Day filled with learning, play, and pride.",
        "Happy 26 January! May every child feel safe, free, and proud to be Indian.",
    ],
    "office": [
        "Wishing our team a very Happy Republic Day. May we keep building with integrity and respect.",
        "Happy Republic Day to all colleagues and partners. Grateful to serve India through honest work.",
        "On this Republic Day, may our workplace stay united, fair, and forward looking.",
    ],
    "long_distance": [
        "Miles away from home, but India stays in my heart. Happy Republic Day!",
        "Sending Republic Day wishes across the distance. Proud to be Indian wherever we are.",
        "Even far from the parade, the tricolour lives in every greeting we send. Jai Hind!",
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
        alt = f"Republic Day 2027 gift idea: {product['name']} from BlueStone"
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
    script = script.replace("bs-cf-eid", "bs-cf-republic")
    return (
        "<!-- wp:html -->\n<style>\n"
        + style
        + '\n</style>\n<div class="bs-cf" id="bs-cf-republic" data-interval="3200" aria-roledescription="carousel" aria-label="BlueStone Republic Day gift ideas">\n'
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
            "What are some short shayari on republic day in hindi?",
            "Try this short shayari on republic day in hindi: "
            "“तिरंगे की शान में सर झुकाते हैं, गणतंत्र दिवस पर हम भारत माता को नमन करते हैं।” "
            "It works well for WhatsApp and Instagram stories.",
        ),
        (
            "What are good Happy Republic Day wishes for 2027?",
            "A clear wish is: “Happy Republic Day 2027! May the tricolour always guide us toward unity and peace.” "
            "Keep it short if you are sending it in a family group.",
        ),
        (
            "What are popular Republic Day quotes in English?",
            "One strong line is: “Republic Day is not only a celebration. It is a reminder of the Constitution we promised to uphold.” "
            "Pair it with a respectful photo of the tricolour.",
        ),
        (
            "Can you share slogans for Republic Day?",
            "Yes. A ready slogan is: “Unity in diversity is India's true strength. Happy Republic Day!” "
            "Use it for school boards, office posts, and captions.",
        ),
        (
            "How do I write Republic Day quotes in Hindi for Instagram?",
            "Choose one short Hindi shayari, add “जय हिंद”, and keep the caption under two lines. "
            "Example: “देश की मिट्टी में छिपा है अभिमान, गणतंत्र दिवस पर बढ़े हमारा सम्मान।”",
        ),
        (
            "What is a thoughtful Republic Day gift idea from BlueStone?",
            "Star motifs and lasting gold jewellery such as The Shining Star Bracelet or The Bandhan Bracelet For Him "
            "make meaningful keepsakes for patriotic celebrations.",
        ),
    ]
    html = [h2("Frequently Asked Questions about Republic Day Shayari & Wishes")]
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
            "Looking for <strong>short shayari on republic day in hindi</strong>, patriotic Republic Day wishes, "
            "quotes, and slogans for 26 January? "
            "This collection covers Hindi shayari, English greetings, Republic Day quotations, and captions ready for WhatsApp and Instagram."
        ),
        para(
            "<strong>TL;DR:</strong> Copy a short Hindi shayari, a Happy Republic Day wish for 2027, "
            "a slogan for school or office, or a caption for social media. All lists are refreshed for Republic Day 2027."
        ),
        para(
            "Republic Day celebrates the Constitution of India and the promise of justice, liberty, and equality. "
            "A sincere message, and sometimes a lasting keepsake, can make 26 January feel personal and proud."
        ),
        h2("Short Shayari on Republic Day in Hindi"),
        para("These short shayari on republic day in hindi are easy to copy for status updates and festive greetings."),
        list_block(SECTIONS["shayari"]),
        h2("Happy Republic Day Wishes in English"),
        para("Send these clear Happy Republic Day wishes to family, friends, and group chats."),
        list_block(SECTIONS["short_en"]),
        h2("Republic Day Quotes & Quotations in English"),
        para("Use these Republic Day quotes when you want a thoughtful line for cards or captions."),
        list_block(SECTIONS["quotes"]),
        h2("Slogans for Republic Day"),
        para("Short slogans for Republic Day boards, school events, and office posts."),
        list_block(SECTIONS["slogans"], ordered=False),
        h2("A Soft Republic Day Gift Idea"),
        para(
            "If you are gifting on Republic Day, choose something lasting that carries pride and care. "
            "Star motifs, gold chains, and bracelets make thoughtful festive keepsakes. "
            "Explore these six approved designs from the BlueStone collection."
        ),
        carousel,
        h2("Republic Day Captions for Instagram & WhatsApp Status"),
        para("Pair these captions with a respectful tricolour or family celebration photo."),
        list_block(SECTIONS["captions"], ordered=False),
        h2("Republic Day Wishes for Kids"),
        para("Simple wishes children can share in school or family groups."),
        list_block(SECTIONS["kids"]),
        h2("Republic Day Messages for Office & Colleagues"),
        para("Warm professional notes for teams and partners."),
        list_block(SECTIONS["office"]),
        h2("Long-Distance Republic Day Wishes"),
        para("Send pride across cities and countries with these long-distance greetings."),
        list_block(SECTIONS["long_distance"]),
        h2("More Festive & Occasion Reads"),
        para(
            'Explore our other guides including <a href="https://blog.bluestone.com/happy-independence-day-2025-best-wishes-patriotic-quotes-messages/">Independence Day quotes for 2026</a>, '
            '<a href="https://blog.bluestone.com/romantic-valentines-day-wishes-quotes-celebrate-love-in-the-most-beautiful-way/">Valentine\'s hubby quotes for 2027</a>, '
            '<a href="https://blog.bluestone.com/bhai-dooj-wishes/">Bhai Dooj wishes for 2026</a>, '
            '<a href="https://blog.bluestone.com/happy-diwali-wishes-messages-quotes-2026/">Diwali wishes for 2026</a>, '
            '<a href="https://blog.bluestone.com/raksha-bandhan-quotes-in-english/">Raksha Bandhan quotes for 2026</a>, and '
            '<a href="https://blog.bluestone.com/friendship-day-2023-wishes/">Friendship Day wishes for 2026</a>. '
            'Learn more about <a href="https://en.wikipedia.org/wiki/Republic_Day_(India)">Republic Day on Wikipedia</a>.'
        ),
        faq_html,
        h2("Conclusion"),
        para(
            "The best short shayari on republic day in hindi and Republic Day wishes keep pride simple and sincere. "
            "Pick a line that fits your audience, personalize it, and share it with respect. Happy Republic Day 2027. Jai Hind!"
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
        "datePublished": "2024-01-20",
        "dateModified": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "author": {"@type": "Person", "name": "Vikas"},
        "publisher": {"@type": "Organization", "name": "BlueStone", "url": "https://www.bluestone.com/"},
        "image": images,
        "mainEntityOfPage": {"@type": "WebPage", "@id": LIVE_URL},
        "keywords": [
            "short shayari on republic day in hindi",
            "happy republic day wishes",
            "republic day wishes",
            "republic day quotes",
            "republic day quotations in english",
            "slogans for republic day",
            "slogan on republic day",
            "republic day quotes in hindi",
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
        "carousel_mid_article": content.index("bs-cf-republic") < content.index("Frequently Asked Questions"),
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
    assets = ROOT / "output/Week1_Rank17_RepublicDay_assets"
    assets.mkdir(parents=True, exist_ok=True)

    product_media = []
    for product in PRODUCTS:
        if not product["png"].exists():
            raise SystemExit(f"Missing SEO Type 2 image: {product['png']}")
        filename = re.sub(r"[^A-Za-z0-9]+", "-", product["name"]).strip("-").lower() + "-carousel-seo.webp"
        webp = assets / filename
        to_carousel_webp(product["png"], webp)
        alt = f"Republic Day 2027 gift idea: {product['name']} from BlueStone"
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
    (ROOT / "output/Week1_Rank17_RepublicDay_article.html").write_text(content)
    (ROOT / "output/Week1_Rank17_RepublicDay_product_media.json").write_text(json.dumps(product_media, indent=2))

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
