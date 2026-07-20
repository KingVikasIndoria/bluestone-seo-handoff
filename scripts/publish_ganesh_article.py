#!/usr/bin/env python3
"""Publish/Optimize Week 1 Rank 13: Ganesh Chaturthi Wishes (New post)."""
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

TITLE = "100+ Happy Ganesh Chaturthi Wishes, Quotes & Messages in English for 2026"
SLUG = "ganesh-chaturthi-wishes-in-english"
META_DESC = (
    "Explore 100+ Happy Ganesh Chaturthi wishes in english, quotes & messages for 2026. "
    "Features vinayagar chaturthi wishes, ganesh chaturthi quotes, and ganapati quotes. Ready to copy."
)
FOCUS_KW = "ganesh chaturthi wishes in english"
YOAST_TITLE = "Happy Ganesh Chaturthi Wishes, Quotes & Messages | BlueStone"
LIVE_URL = f"https://blog.bluestone.com/{SLUG}/"

PRODUCTS = [
    {
        "code": "BVPJ0935C06",
        "name": "The Shubhlatika Mangalsutra Necklace",
        "url": "https://www.bluestone.com/mangalsutra+chains/the-shubhlatika-mangalsutra-necklace~146084.html",
        "png": ROOT / "ProductImages/seo images/Mangalsutra Chains/The Shubhlatika Mangalsutra Necklace.png",
    },
    {
        "code": "BISP0514C09",
        "name": "The Eirini Mangalsutra",
        "url": "https://www.bluestone.com/mangalsutra+chains/the-eirini-mangalsutra~53179.html",
        "png": ROOT / "ProductImages/seo images/Mangalsutra Chains/The Eirini Mangalsutra.png",
    },
    {
        "code": "BIMA0780C53",
        "name": "The Casma Mangalsutra",
        "url": "https://www.bluestone.com/mangalsutra+chains/the-casma-mangalsutra~93030.html",
        "png": ROOT / "ProductImages/seo images/Mangalsutra Chains/The Casma Mangalsutra.png",
    },
    {
        "code": "BISP0506C05",
        "name": "The Aarabhi Mangalsutra",
        "url": "https://www.bluestone.com/mangalsutra+chains/the-aarabhi-mangalsutra~46940.html",
        "png": ROOT / "ProductImages/seo images/Mangalsutra Chains/The Aarabhi Mangalsutra.png",
    },
    {
        "code": "BISW1080P28",
        "name": "The Thyvarne Pendant",
        "url": "https://www.bluestone.com/pendants/the-thyvarne-pendant~63040.html",
        "png": ROOT / "ProductImages/seo images/Pendants/The Thyvarne Pendant.png",
    },
    {
        "code": "BISW1080P32",
        "name": "The Teshvarya Pendant",
        "url": "https://www.bluestone.com/pendants/the-teshvarya-pendant~63044.html",
        "png": ROOT / "ProductImages/seo images/Pendants/The Teshvarya Pendant.png",
    },
]

SECTIONS = {
    "classic": [
        "Wishing you a very Happy Ganesh Chaturthi! May Lord Ganesha bless you with happiness, wisdom, and peace.",
        "May the divine blessings of Bappa bring joy, health, and prosperity into your home this festive season.",
        "Warmest greetings on Ganesh Chaturthi! Hoping Lord Ganesha guides you through every challenge.",
        "May Lord Ganesha remove all obstacles from your path and bless you with success. Happy Holiday!",
        "Wishing you a beautiful and auspicious Vinayagar Chaturthi! Grateful for the blessings we share.",
        "May the light of Ganesha's wisdom continue to direct your path. Happy Ganesh Chaturthi!",
        "Sending sweet wishes and prayers for your family's safety and joy. Happy Chaturthi!",
        "May Bappa fill your home with sweet modak memories and peaceful gatherings. Jai Hind!",
    ],
    "family": [
        "To my wonderful family, may Lord Ganesha bless our home with unity, strength, and daily happiness.",
        "Wishing my dear parents a happy Ganesh Chaturthi! Grateful for your constant guidance and blessings.",
        "May the presence of Bappa in our home bring positive energy, clean paths, and prosperity. Happy Chaturthi!",
        "To my siblings, wishing you a happy and peaceful festive season. May Bappa fulfill all your dreams.",
        "Sending prayers for our family's health, longevity, and spiritual progress. Happy Ganesh Chaturthi!",
        "Thank you for sharing the sweet moments of Ganesh Chaturthi celebrations with me. Jai Bappa Morya!",
        "May the divine grace of Vinayagar protect our family from all evils. Happy Ganesh Chaturthi!",
        "To my rock and constant supporter, wishing you the happiest and most blessed Ganesh Chaturthi!",
    ],
    "quotes": [
        "May Lord Ganesha destroy all your sorrows, enhance your happiness, and create new paths of success.",
        "In the presence of Ganesha, all obstacles melt away and a clear direction emerges.",
        "The curved trunk, the large ears, and the round belly: Bappa is the keeper of all wisdom.",
        "Ganesha is the lord of new beginnings, the patron of arts and sciences, and the deva of intellect.",
        "May the grace of Vinayagar brighten your mind and bring deep clarity to your thoughts.",
        "Let us pray to Ganesha, the remover of all obstacles, to guide us toward wealth and peace.",
    ],
    "regional": [
        "Wishing you a very Happy Vinayagar Chaturthi! May the divine blessings of Pillayar bring joy and peace.",
        "Happy Ganesh Utsav to all my friends! Let us welcome Bappa with drums, sweet modaks, and open hearts.",
        "Ganesh Chaturthi Shubhechha! May this holy occasion bring light and progress to your career and life.",
        "Vinayagar Chaturthi Nalvazhthukkal! May Lord Ganesha bless you with health, wealth, and spiritual growth.",
        "Hoping the arrival of Ganpati brings success, stability, and great joy to your community. Jai Ganesha!",
        "Sending warm wishes on this holy occasion of Lord Ganesha's birth. May his light cover us all.",
    ],
    "prosperity": [
        "May Lord Ganesha bless you with wealth, progress, and professional success. Happy Ganesh Chaturthi!",
        "Wishing you a highly prosperous Ganesh Chaturthi! May Bappa open new doors of opportunity for you.",
        "May the arrival of Ganpati bring financial stability, good health, and wise investments. Happy Holiday!",
        "To the start of new projects and ventures, may Lord Ganesha guide you with intellect and luck.",
        "Sending prayers for your career growth, business progress, and daily achievements. Happy Chaturthi!",
        "May the blessings of Ganesha grant you both spiritual wealth and material success. Cheers!",
    ],
    "office": [
        "Wishing all our clients and colleagues a very Happy Ganesh Chaturthi! May this festival bring growth to our team.",
        "To my team members, hoping Lord Ganesha blesses our work with coordination, success, and peace.",
        "Happy Ganesh Chaturthi! May this auspicious occasion mark the beginning of great milestones for our office.",
        "Wishing you a peaceful and happy Ganesh Chaturthi! May Bappa remove all professional obstacles.",
        "May the blessings of Lord Ganesha bring luck, clarity, and wealth to all our future collaborations.",
    ],
    "shlokas": [
        "Vakratunda Mahakaya Suryakoti Samaprabha, Nirvighnam Kuru Me Deva Sarvakaryeshu Sarvada. (O Lord Ganesha of the curved trunk and massive body, whose splendor is equal to a million suns, please make all my works free of obstacles, always.)",
        "Pranamya Shirasa Devam Gauri Putram Vinayakam, Bhaktavasam Smarennityam Ayuh Kamartha Siddhaye. (Salutations to Gauri's son, Vinayaka, the divine one who lives in the hearts of his devotees, to bless us with longevity, desires, and success.)",
        "Gajananam Bhuta Ganadhi Sevitam, Kapittha Jambu Phala Sara Bhakshitam. (O elephant-faced Ganesha, served by the celestial attendants, who enjoys the essence of wood-apple and rose-apple fruits.)",
        "Aum Ekadantaya Viddhamahe Vakratundaya Dheemahi Tanno Danti Prachodayat. (We pray to the one-tusked Lord, we meditate on the curved trunk. May the elephant-tusked God guide and inspire us.)",
    ]
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
        alt = f"Ganesh Chaturthi 2026 gift idea: {product['name']} from BlueStone"
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
    script = script.replace("bs-cf-eid", "bs-cf-ganesh")
    return (
        "<!-- wp:html -->\n<style>\n"
        + style
        + '\n</style>\n<div class="bs-cf" id="bs-cf-ganesh" data-interval="3200" aria-roledescription="carousel" aria-label="BlueStone Ganesh Chaturthi gift ideas">\n'
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
            "What are the best happy ganesh chaturthi wishes in english?",
            "The best happy Ganesh Chaturthi wishes focus on blessings, wisdom, and obstacle removal: “Wishing you a very Happy Ganesh Chaturthi! May Lord Ganesha bless you with happiness, wisdom, and peace.” These greetings make beautiful card notes.",
        ),
        (
            "What are the most popular ganesha quotes and ganpati quotes?",
            "A popular quote is: “May Lord Ganesha destroy all your sorrows, enhance your happiness, and create new paths of success.” These quotes are perfect for card headings and social media messages.",
        ),
        (
            "How do I wish someone a happy vinayagar chaturthi?",
            "Write: “Wishing you a very Happy Vinayagar Chaturthi! May the divine blessings of Pillayar bring joy and peace.”",
        ),
        (
            "What is a traditional Sanskrit greeting for Ganesh Chaturthi?",
            "A traditional greeting is: “Vakratunda Mahakaya Suryakoti Samaprabha, Nirvighnam Kuru Me Deva Sarvakaryeshu Sarvada.” This shloka invokes Lord Ganesha to make all our tasks free of obstacles.",
        ),
        (
            "What are some good ganesh chaturthi wishes for wealth and prosperity?",
            "Write: “May Lord Ganesha bless you with wealth, progress, and professional success. Happy Ganesh Chaturthi!”",
        ),
        (
            "Can I gift a gold mangalsutra or pendant for Ganesh Chaturthi?",
            "Yes! Gold mangalsutras and diamond pendants like The Shubhlatika Mangalsutra Necklace or The Thyvarne Pendant make auspicious and lasting festive gifts.",
        ),
    ]
    html = [h2("Frequently Asked Questions about Ganesh Chaturthi Wishes")]
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
            "Looking for the best <strong>ganesh chaturthi wishes in english</strong>, quotes, and greetings to share with your family and friends? "
            "Whether you need short card messages, deep spiritual quotes, regional Vinayagar greetings, or prosperity wishes, this collection has it all."
        ),
        para(
            "<strong>TL;DR:</strong> Copy a quick wish for a card, an emotional quote for a text, a dedicated message for office colleagues, or a traditional Sanskrit shloka. "
            "All lists are updated for Ganesh Chaturthi 2026."
        ),
        para(
            "Auspicious beginnings start with Bappa. Celebrating Ganesh Chaturthi with a sincere message or traditional gold keepsake is a beautiful way to mark this milestone."
        ),
        h2("Classic Happy Ganesh Chaturthi Wishes"),
        para("Keep your greetings direct and scanable with these quick, copy-ready wishes."),
        list_block(SECTIONS["classic"]),
        h2("Heartfelt Blessings for Friends and Family"),
        para("Send these warm, respectful wishes to your family members to thank them for their guidance and trust."),
        list_block(SECTIONS["family"]),
        h2("Popular Ganesha Quotes & Ganpati Quotes"),
        para("These Ganesha quotes and Ganpati quotes celebrate the rare gift of wisdom and removal of obstacles."),
        list_block(SECTIONS["quotes"]),
        h2("Vinayagar Chaturthi Wishes & Regional Greetings"),
        para("Reflect on your shared history, regional roots, and traditions with these regional Vinayagar greetings."),
        list_block(SECTIONS["regional"]),
        h2("Divine Tokens: Auspicious Mangalsutra & Pendant Gift Ideas"),
        para(
            "Ganesh Chaturthi is a time for new beginnings, prosperity, and buying gold. "
            "If you are celebrating this holy season with a family keepsake, traditional diamond mangalsutras or elegant circular pendants make classic choices. "
            "Explore these six approved designs from the BlueStone collection."
        ),
        carousel,
        h2("Ganesh Chaturthi Wishes for Wealth, Prosperity & Success"),
        para("Celebrate your shared success, career milestones, and financial progress with these prosperity wishes."),
        list_block(SECTIONS["prosperity"]),
        h2("Professional Messages for Colleagues & Office"),
        para("Keep your professional connections strong with these warm holiday wishes sent to colleagues and clients."),
        list_block(SECTIONS["office"]),
        h2("Traditional Sanskrit-Inspired Shlokas & Meanings"),
        para("Invoke the divine presence of Vinayaka with these classic Sanskrit shlokas and their English translations."),
        list_block(SECTIONS["shlokas"]),
        h2("More Festive & Occasion Reads"),
        para(
            'Explore our other occasion guides including <a href="https://blog.bluestone.com/heart-touching-love-proposal-quotes-2027/">proposal quotes for 2027</a>, '
            '<a href="https://blog.bluestone.com/happy-holi-wishes-messages-quotes-2027/">Holi wishes for 2027</a>, '
            '<a href="https://blog.bluestone.com/happy-diwali-wishes-messages-quotes-2026/">Diwali wishes for 2026</a>, '
            '<a href="https://blog.bluestone.com/happy-eid-mubarak-wishes-messages-quotes-2027/">Eid wishes for 2027</a>, '
            '<a href="https://blog.bluestone.com/happy-childrens-day-best-wishes-quotes-messages-for-kids/">Children\'s Day quotes for 2026</a>, '
            '<a href="https://blog.bluestone.com/engagement-quotes/">engagement quotes for 2026</a>, '
            '<a href="https://blog.bluestone.com/teachers-day-wishes-in-english/">Teachers\' Day wishes for 2026</a>, '
            '<a href="https://blog.bluestone.com/dussehra-wishes-in-english/">Dussehra wishes for 2026</a>, and '
            '<a href="https://blog.bluestone.com/friendship-day-2023-wishes/">Friendship Day wishes for 2026</a>.'
        ),
        faq_html,
        h2("Conclusion"),
        para(
            "The best ganesh chaturthi wishes in english focus on blessings, wisdom, and prosperity. "
            "Select a message that fits your connection, customize it, and share it with love. Happy Ganesh Chaturthi 2026!"
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
            "ganesh chaturthi wishes in english",
            "vinayagar chaturthi wishes",
            "lord ganesha happy ganesh chaturthi",
            "ganesh chaturthi quotes",
            "ganapti quotes",
            "ganesha quotes",
            "ganpati quotes",
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
        "carousel_mid_article": content.index("bs-cf-ganesh") < content.index("Frequently Asked Questions"),
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
    assets = ROOT / "output/Week1_Rank13_GaneshChaturthi_assets"
    assets.mkdir(parents=True, exist_ok=True)

    product_media = []
    for product in PRODUCTS:
        if not product["png"].exists():
            raise SystemExit(f"Missing approved Type 2 image: {product['png']}")
        filename = re.sub(r"[^A-Za-z0-9]+", "-", product["name"]).strip("-").lower() + "-carousel.webp"
        webp = assets / filename
        to_carousel_webp(product["png"], webp)
        alt = f"Ganesh Chaturthi 2026 gift idea: {product['name']} from BlueStone"
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
    (ROOT / "output/Week1_Rank13_GaneshChaturthi_article.html").write_text(content)
    (ROOT / "output/Week1_Rank13_GaneshChaturthi_product_media.json").write_text(
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
