#!/usr/bin/env python3
"""Optimize Week 1 Rank 6: Independence Day quotes in English (WP #14819)."""
import base64
import json
import os
import re
import urllib.request
from datetime import datetime, timezone
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_local_env():
    env_path = ROOT / ".env"
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

POST_ID = 14819
SLUG = "independence-day-quotes-in-english"
TITLE = "100+ Independence Day Quotes in English, Wishes & Messages for 2026"
META_DESC = (
    "Find 100+ Independence Day quotes in English for 2026, with patriotic wishes, "
    "thoughts, WhatsApp messages, proud Indian quotes and captions. Ready to share."
)
FOCUS_KW = "independence day quotes in english"
YOAST_TITLE = "Independence Day Quotes in English 2026 | BlueStone"
LIVE_URL = f"https://blog.bluestone.com/{SLUG}/"

PRODUCTS = [
    {
        "code": "BIMG0635V45",
        "name": "The Shining Star Bracelet",
        "url": "https://www.bluestone.com/bracelets/the-shining-star-bracelet~63731.html",
        "png": ROOT / "ProductImages/seo images/Bracelet/The Shining Star Bracelet.png",
    },
    {
        "code": "BIAV0865V24",
        "name": "The Pervinca Charm Holder Bracelet",
        "url": "https://www.bluestone.com/bracelets/the-pervinca-charm-holder-bracelet~103133.html",
        "png": ROOT / "ProductImages/seo images/Bracelet/The Pervinca Charm Holder Bracelet.png",
    },
    {
        "code": "BIAV0865V25",
        "name": "The Malocchio Charm Holder Bracelet",
        "url": "https://www.bluestone.com/bracelets/the-malocchio-charm-holder-bracelet~95653.html",
        "png": ROOT / "ProductImages/seo images/Bracelet/The Malocchio Charm Holder Bracelet.png",
    },
    {
        "code": "BIPM0001H28",
        "name": "The Rohal Huggie Earrings",
        "url": "https://www.bluestone.com/earrings/the-rohal-huggie-earrings~21864.html",
        "png": ROOT / "ProductImages/seo images/Earrings/The Rohal Huggie Earrings.png",
    },
    {
        "code": "BISA0255D05",
        "name": "The Asya Huggie Earrings",
        "url": "https://www.bluestone.com/earrings/the-asya-huggie-earrings~13494.html",
        "png": ROOT / "ProductImages/seo images/Earrings/The Asya Huggie Earrings.png",
    },
    {
        "code": "BIIP0279S08",
        "name": "The Aleena Huggie Earrings",
        "url": "https://www.bluestone.com/earrings/the-aleena-huggie-earrings~16735.html",
        "png": ROOT / "ProductImages/seo images/Earrings/The Aleena Huggie Earrings.png",
    },
]

SECTIONS = {
    "short_quotes": [
        "Freedom grows stronger when every citizen uses it with care.",
        "A free nation thrives when its people choose courage over comfort.",
        "Let the tricolour remind us that unity is a daily choice.",
        "Independence is a gift from the past and a duty to the future.",
        "Our freedom shines brightest through honest work and kind actions.",
        "India rises when every dream gets room to grow.",
        "Pride in our country begins with respect for one another.",
        "The flag flies high when our values stand firm.",
        "Freedom gives us a voice, responsibility gives it purpose.",
        "Many languages, many traditions, one shared hope.",
        "Remember the sacrifice, celebrate the freedom, build the future.",
        "A stronger India starts with a better choice today.",
        "Patriotism is gratitude expressed through action.",
        "Let every free thought help shape a fairer tomorrow.",
        "Our diversity is not a challenge to solve, but a strength to honour.",
        "Jai Hind is a greeting, a promise, and a call to serve.",
    ],
    "wishes": [
        "Wishing you and your family a peaceful and proud Independence Day 2026.",
        "May 15 August fill your home with gratitude, hope, and togetherness.",
        "Happy Independence Day! May our country keep moving forward with courage.",
        "Sending warm wishes for a day that celebrates freedom and responsibility.",
        "May the tricolour always inspire confidence in your heart.",
        "Happy Independence Day to you and everyone you hold dear.",
        "May we honour our history by creating a kinder future together.",
        "Wishing your family joy, unity, and pride this 15 August.",
        "May the spirit of freedom guide your choices throughout the year.",
        "Here is to an India where every dream has a fair chance.",
        "Happy Independence Day! May peace and progress reach every home.",
        "Let us celebrate the country we love and the future we can build.",
        "May this day renew your faith in unity and shared purpose.",
        "Warm wishes for a meaningful Independence Day filled with gratitude.",
        "May the courage of earlier generations inspire our actions today.",
        "Wishing you a bright 15 August and a hopeful year ahead. Jai Hind!",
    ],
    "thoughts": [
        "Freedom is meaningful when it protects dignity, opportunity, and justice for all.",
        "Independence asks more of us than celebration. It asks us to participate.",
        "A nation moves forward when its citizens listen across their differences.",
        "The best tribute to freedom fighters is a country worthy of their courage.",
        "Progress begins when we pair national pride with everyday responsibility.",
        "Democracy becomes stronger when informed people speak and listen with respect.",
        "Our rights give us freedom. Our duties help that freedom endure.",
        "India's future is built in classrooms, homes, workplaces, and caring communities.",
        "Real patriotism leaves space for hope, questions, and better ideas.",
        "Every generation inherits freedom and decides what it will become next.",
        "Unity does not require sameness. It requires mutual respect.",
        "Independence Day is both a celebration of history and an invitation to contribute.",
    ],
    "proud_indian": [
        "Proud to be an Indian, proud of our diversity, and hopeful for our future.",
        "My roots are Indian, my dreams are limitless, and my heart says Jai Hind.",
        "I carry India's colours with gratitude and its future with hope.",
        "Proud of the land that teaches unity through countless traditions.",
        "Being Indian means finding strength in many voices and one shared home.",
        "My India is bold in spirit, rich in culture, and young in ambition.",
        "Proud to belong to a nation that keeps learning, building, and dreaming.",
        "From every region and language, we bring one country to life.",
        "I celebrate India's past and believe in the future we can shape.",
        "Proud Indian today, responsible citizen every day.",
        "Our stories may differ, but the tricolour belongs to us all.",
        "India is not only where I live. It is a part of how I hope.",
    ],
    "india_quotes": [
        "India's greatest promise lives in the imagination of its people.",
        "Across mountains, coasts, cities, and villages, one hope connects us.",
        "The story of independent India is still being written by all of us.",
        "Our nation becomes stronger when opportunity travels farther.",
        "India's colours hold courage, peace, growth, and purposeful movement.",
        "Let our love for India appear in the care we show its people.",
        "A nation of many traditions can still move with one purpose.",
        "Independent India is a living idea shaped by every generation.",
        "The beauty of India lies in difference held together by belonging.",
        "Let our national pride be generous, thoughtful, and future focused.",
        "India moves ahead when every community is invited to move with it.",
        "May freedom remain the foundation for creativity, dignity, and progress.",
    ],
    "whatsapp": [
        "Happy Independence Day 2026! Proud heart, hopeful mind, Jai Hind.",
        "Freedom in our thoughts, unity in our actions. Happy 15 August!",
        "Saluting the courage that made our freedom possible.",
        "One country, many voices, one shared future. Jai Hind!",
        "May the tricolour always fly high in our hearts.",
        "Grateful for freedom and ready for responsibility.",
        "Happy Independence Day from our family to yours.",
        "Proud of our past, committed to a better tomorrow.",
        "Celebrate freedom with gratitude, kindness, and purpose.",
        "15 August 2026: remember, respect, and rise together.",
        "Today we celebrate India and the possibilities ahead.",
        "Warm Independence Day wishes to you. Jai Hind!",
    ],
    "status": [
        "Tricolour in my heart. Hope in my step.",
        "Free to dream, ready to contribute.",
        "15 August mood: grateful, proud, hopeful.",
        "Unity is our strength. Freedom is our shared legacy.",
        "Indian by birth, hopeful by choice.",
        "Honouring history. Building tomorrow.",
        "A proud heart and a responsible voice.",
        "Celebrating India in all its colour and courage.",
        "Freedom looks best with kindness and purpose.",
        "Many cultures. One country. Endless possibility.",
        "Carrying the tricolour with gratitude.",
        "Jai Hind, today and every day.",
    ],
    "colleagues": [
        "Wishing our team a thoughtful Independence Day filled with shared pride.",
        "May the spirit of freedom inspire integrity and progress in all we do.",
        "Happy Independence Day to colleagues who help turn ideas into impact.",
        "Let us celebrate 15 August with gratitude and renewed purpose.",
        "Wishing everyone a peaceful holiday and a hopeful year for India.",
        "May unity, respect, and responsibility guide our work together.",
        "Happy Independence Day! Here is to building a stronger future as one team.",
        "On this national day, we honour courage and recommit to meaningful work.",
        "Warm 15 August wishes to you and your family.",
        "May our workplaces reflect the fairness and opportunity freedom promises.",
    ],
    "students": [
        "Freedom gives every learner the chance to ask, explore, and create.",
        "Young minds are not only India's future. They are shaping India today.",
        "Learn from history, think independently, and act with kindness.",
        "Let your education become a way to serve the country.",
        "A curious student can become a courageous citizen.",
        "Dream for yourself and make room for others to dream too.",
        "Use your voice wisely, because freedom makes it matter.",
        "Celebrate Independence Day by learning one story from India's freedom movement.",
        "The country needs your questions, your ideas, and your integrity.",
        "Jai Hind! May every classroom become a place where possibility begins.",
    ],
    "cards": [
        "On Independence Day 2026, may we remember that freedom is strengthened by compassion, honesty, and participation. Wishing you a meaningful 15 August.",
        "May this national day fill you with gratitude for the past and confidence in the future we can create together.",
        "As the tricolour rises, may our respect for one another rise with it. Happy Independence Day to you and your family.",
        "Wishing you a day of quiet pride, thoughtful reflection, and renewed hope for India's journey ahead.",
        "May the courage behind our independence inspire us to make brave and generous choices in our own time.",
        "This 15 August, let us celebrate not only where India has been, but also what each of us can help it become.",
        "May freedom continue to open doors for learning, dignity, creativity, and opportunity across our country.",
        "With gratitude for those who came before us and hope for those who follow, warm wishes for Independence Day 2026.",
        "May our shared love for India help us listen better, work together, and build with purpose.",
        "Sending heartfelt Independence Day wishes and the hope that peace, fairness, and progress reach every Indian home.",
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
        alt = f"Independence Day 2026 gift idea: {product['name']} from BlueStone"
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
    script = script.replace("bs-cf-eid", "bs-cf-independence-day")
    return (
        "<!-- wp:html -->\n<style>\n"
        + style
        + '\n</style>\n<div class="bs-cf" id="bs-cf-independence-day" data-interval="3200" aria-roledescription="carousel" aria-label="BlueStone Independence Day gift ideas">\n'
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
            "What are the best Independence Day quotes in English for 2026?",
            "The best Independence Day quotes in English for 2026 are short, sincere, and connected to freedom, unity, or responsibility. Try: “Independence is a gift from the past and a duty to the future.” Choose a line that matches your audience, then add a simple Happy Independence Day or Jai Hind.",
        ),
        (
            "What is a short Happy Independence Day wish for WhatsApp?",
            "A short WhatsApp wish is: “Freedom in our thoughts, unity in our actions. Happy Independence Day 2026!” It fits comfortably on one screen and works for family, friends, and group chats. For a warmer version, add the recipient's name or a brief line wishing peace and progress to their family.",
        ),
        (
            "What is a meaningful Independence Day thought?",
            "A meaningful Independence Day thought is: “Our rights give us freedom. Our duties help that freedom endure.” It moves beyond celebration and reminds readers that independence includes everyday responsibility. This kind of line suits school boards, speeches, professional posts, cards, and thoughtful social media captions.",
        ),
        (
            "What is a good proud to be an Indian quote?",
            "A good proud to be an Indian quote is: “Proud to be an Indian, proud of our diversity, and hopeful for our future.” It expresses belonging without sounding overly formal. You can use it as a WhatsApp status, Instagram caption, school message, or the opening line of an Independence Day card.",
        ),
        (
            "How do I wish family and friends on 15 August?",
            "Wish family and friends with a warm line that combines gratitude and hope. For example: “May 15 August fill your home with gratitude, hope, and togetherness.” Keep the message personal by adding their name or mentioning a value you share, such as unity, kindness, courage, or service.",
        ),
        (
            "What is a good Independence Day status for Instagram?",
            "A good Independence Day status is: “15 August mood: grateful, proud, hopeful.” Short captions are easy to read and work well with a respectful tricolour, flag-hoisting, or community celebration photo. Avoid crowding the image with long text. Put the full message in the caption instead.",
        ),
        (
            "When is Independence Day celebrated in India?",
            "India celebrates Independence Day on 15 August every year. The day marks India's independence in 1947 and is observed through flag-hoisting ceremonies, cultural programmes, speeches, and community events. In 2026, 15 August falls on a Saturday, making it convenient for many families and groups to celebrate together.",
        ),
        (
            "How can I write a respectful Independence Day message for colleagues?",
            "Keep a workplace message inclusive, concise, and focused on shared values. Try: “May the spirit of freedom inspire integrity and progress in all we do. Happy Independence Day 2026.” Avoid political claims or exaggerated language. A calm note about unity, responsibility, respect, or meaningful work usually fits professional channels best.",
        ),
    ]
    html = [h2("Frequently Asked Questions about Independence Day Quotes")]
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
            "Looking for <strong>Independence Day quotes in English</strong> that you can copy and share in 2026? "
            "This collection brings together short patriotic quotes, heartfelt wishes, meaningful thoughts, proud Indian lines, WhatsApp messages, and captions for 15 August."
        ),
        para(
            "<strong>TL;DR:</strong> Choose a short line for WhatsApp, a thoughtful quote for a card or speech, "
            "and a warm wish for family, friends, or colleagues. Every section below is written for Independence Day 2026 and grouped by tone."
        ),
        para(
            "India celebrates Independence Day on <strong>15 August</strong>. The most memorable message is rarely the longest one. "
            "It is the line that feels honest, respects the meaning of freedom, and sounds natural in your voice."
        ),
        h2("Short Independence Day Quotes in English"),
        para("Start here when you want a crisp line for a greeting, school board, speech opening, or social post."),
        list_block(SECTIONS["short_quotes"]),
        h2("Happy Independence Day Wishes for Family and Friends"),
        para("These happy Independence Day wishes balance warmth, national pride, and a hopeful tone."),
        list_block(SECTIONS["wishes"]),
        h2("Independence Day Thoughts on Freedom and Responsibility"),
        para("A meaningful Independence Day thought can turn a greeting into a moment of reflection."),
        list_block(SECTIONS["thoughts"]),
        h2("Proud to Be an Indian Quotes"),
        para("Use these proud to be an Indian quotes for captions, cards, classroom displays, and community messages."),
        list_block(SECTIONS["proud_indian"]),
        h2("India Independence Day Quotes for 2026"),
        para("These India Independence Day quotes celebrate diversity, belonging, opportunity, and shared progress."),
        list_block(SECTIONS["india_quotes"]),
        h2("A Thoughtful Independence Day Gift Idea"),
        para(
            "If you are pairing your message with a keepsake, choose a piece that fits the person's everyday style. "
            "Gold, pearl, gemstone, and star details can complement a simple festive outfit without turning the occasion into a sales moment. "
            "Here are six BlueStone ideas selected from the approved product list."
        ),
        carousel,
        h2("Short Independence Day Messages for WhatsApp"),
        para("These compact 15 August messages are ready for personal chats, family groups, and community updates."),
        list_block(SECTIONS["whatsapp"]),
        h2("Independence Day Status and Captions for Instagram"),
        para("Keep an Independence Day status easy to scan. Let the image carry the scene and the caption carry the thought."),
        list_block(SECTIONS["status"]),
        h2("Independence Day Wishes for Colleagues and Teams"),
        para("Professional messages work best when they are inclusive, respectful, and connected to shared purpose."),
        list_block(SECTIONS["colleagues"]),
        h2("Patriotic Lines for Students and School Speeches"),
        para("Students can use these original lines in assemblies, classroom displays, short speeches, and activity boards."),
        list_block(SECTIONS["students"]),
        h2("Thoughtful Independence Day Messages for Cards and Emails"),
        para("Choose a slightly longer message when you have room to reflect on gratitude, duty, and India's future."),
        list_block(SECTIONS["cards"]),
        h2("How to Choose the Right Independence Day Message"),
        list_block(
            [
                "Match the length to the channel. Use one line for status updates and two or three sentences for cards.",
                "Choose the tone for the recipient. Family messages can feel warm, while workplace messages should stay inclusive.",
                "Use one strong idea. Freedom, unity, gratitude, responsibility, and hope are all clear starting points.",
                "Personalise lightly. Add a name, shared memory, school, city, or community when it feels natural.",
                "Keep flag imagery respectful. For official guidance, refer to the National Portal of India's information on the Indian tricolour.",
            ]
        ),
        h2("More Festive Wishes to Explore"),
        para(
            'Continue with our <a href="https://blog.bluestone.com/happy-holi-wishes-messages-quotes-2027/">Holi wishes for 2027</a>, '
            '<a href="https://blog.bluestone.com/happy-diwali-wishes-messages-quotes-2026/">Diwali wishes for 2026</a>, '
            '<a href="https://blog.bluestone.com/happy-childrens-day-best-wishes-quotes-messages-for-kids/">Children\'s Day quotes for 2026</a>, and '
            '<a href="https://blog.bluestone.com/happy-eid-mubarak-wishes-messages-quotes-2027/">Eid wishes for 2027</a>.'
        ),
        para(
            'For official background, read the <a href="https://www.india.gov.in/explore-india/facts-of-india/independence-day" rel="noopener">National Portal of India Independence Day page</a> '
            'and its <a href="https://knowindia.india.gov.in/my-india-my-pride/indian-tricolor.php" rel="noopener">guide to the Indian tricolour</a>.'
        ),
        h2("Conclusion"),
        para(
            "The best Independence Day quotes in English are sincere, easy to share, and grounded in gratitude. "
            "Pick one line that suits your audience, add a personal note, and share it with respect. Happy Independence Day 2026. Jai Hind!"
        ),
        faq_html,
    ]
    content = "\n\n".join(parts)
    images = [product["src"] for product in product_media]
    faq_page = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_schema}
    blog_posting = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": TITLE,
        "description": META_DESC,
        "datePublished": "2025-08-08",
        "dateModified": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "author": {"@type": "Person", "name": "Vikas"},
        "publisher": {"@type": "Organization", "name": "BlueStone", "url": "https://www.bluestone.com/"},
        "image": images,
        "mainEntityOfPage": {"@type": "WebPage", "@id": LIVE_URL},
        "keywords": [
            "independence day quotes in english",
            "happy independence day wishes",
            "independence day thought",
            "proud to be an indian quote",
            "india independence day quotes",
            "independence day status",
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
        "carousel_mid_article": content.index("bs-cf-independence-day") < content.index("Frequently Asked Questions"),
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
    assets = ROOT / "output/Week1_Rank6_IndependenceDay_assets"
    assets.mkdir(parents=True, exist_ok=True)

    product_media = []
    for product in PRODUCTS:
        if not product["png"].exists():
            raise SystemExit(f"Missing approved Type 2 image: {product['png']}")
        filename = re.sub(r"[^A-Za-z0-9]+", "-", product["name"]).strip("-").lower() + "-carousel.webp"
        webp = assets / filename
        to_carousel_webp(product["png"], webp)
        alt = f"Independence Day 2026 gift idea: {product['name']} from BlueStone"
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
    (ROOT / "output/Week1_Rank6_IndependenceDay_article.html").write_text(content)
    (ROOT / "output/Week1_Rank6_IndependenceDay_product_media.json").write_text(
        json.dumps(product_media, indent=2)
    )

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
    print("updated", post["id"], post["link"])
    print("local_validation", rules)


if __name__ == "__main__":
    main()
