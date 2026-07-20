# Blog SEO + AEO/GEO Quality Checklist — BlueStone v2

Use this before publishing. Built from Master Prompt v5 + GEO playbook + live workflow decisions.

**Volume note:** Festive plan targets roughly **1k–10k** monthly volume. Low-volume supporting terms can live in H2/FAQ.

---

## A. Intent & brief
- [ ] One clear primary keyword; supporting keywords mapped to H2/FAQ (not new URLs)
- [ ] Search intent matched (wishes = copy-paste lists; guide = how-to; gift = recommendations)
- [ ] Action is **New** (new slug). Ignore sheet `Optimize` — do not edit an old URL for this keyword
- [ ] New slug matches this keyword intent (not a mismatched legacy post)
- [ ] If competitor URL exists: H2 coverage mirrored (structure only, not copied text)
- [ ] **Recency:** use the locked festive year only (**2026** or **2027** per year rule). Do **not** leave old years (2021–2025) in title/body/FAQs/alts except in unrelated internal-link titles for other festivals
- [ ] Supporting KWs mapped to H2/FAQ; near-duplicates (`msg`/`msgs`) share this URL
- [ ] FAQs prefer volume-backed supporting intents; utility FAQs OK as secondary
- [ ] **H2 spine:** ~70–80% volume-backed (higher); competitor-only buckets (funny / long-distance / etc.) lower and shorter

## B. SEO structure
- [ ] Title tag uses primary KW naturally
- [ ] One H1 with primary KW
- [ ] Header hierarchy: H1 → H2 → H3
- [ ] Primary KW in: Page Title, Meta Description, first 100 words, ≥1 image alt
- [ ] Synonyms / supporting keywords used naturally in H2s, lists, FAQs
- [ ] KW density roughly 1–3% (don't force)
- [ ] Meta title ~≤60 chars preferred; meta description ~150–160 chars
- [ ] Slug clean, readable, KW-led
- [ ] Yoast focus keyphrase + SEO title + meta set (API or CMS)

## C. Content & readability
- [ ] Direct answer in first 2–3 sentences + TL;DR near top
- [ ] Intro has no links clutter
- [ ] Opens with opinion, scenario, or clear hook
- [ ] Paragraphs short; lists where intent needs them (required for wishes)
- [ ] Visual break every ~100 words
- [ ] H2/H3 at least every ~300 words
- [ ] **No em/en dashes** and **no `word - word`** (WP texturize → en dash). Use `,` or `:`
- [ ] Ends with one clear next step

## D. Festive wishes posts (80/20)
- [ ] ~80% shareable wish/quote/message lists
- [ ] ~20% brand: ≤1 soft gift CTA + optional trust line
- [ ] Not a product catalogue; no scheme dump on pure wishes posts

## E. AEO / GEO
- [ ] Every major H2 can stand alone as an answer chunk
- [ ] **Visible FAQ HTML** on page (5–10 Qs, 40–80 words) — not schema-only
- [ ] FAQPage JSON-LD + Article/BlogPosting JSON-LD
- [ ] Freshness signal (Last updated / year in title)

## F. Media & links
- [ ] Type 3 prompts JSON written (`output/Week1_Rank{N}_{Topic}_type3_prompts.json`) with theme anchor + negative prompt
- [ ] Type 3 via **Higgsfield MCP** (`nano_banana_pro`): hyper-real lifestyle prompts; CDN refs via `media_import_url` (see `HIGGSFIELD_IMAGE_GENERATION.md`)
- [ ] Type 3 hygiene: lifestyle (not product-on-plain); jewellery visible; no readable text on screens; 16:9; nothing cropped; **fair-skinned Indians only** in people/hand/wrist shots
- [ ] Type 2 AI product images in **mid-article carousel** + Buy now (from `ProductImages/seo images/`)
- [ ] Type 1 raw never used as carousel/CTA hero (reference only)
- [ ] No duplicate images (featured counts)
- [ ] Carousel **not** the last content block; content continues after it
- [ ] Product names + PDP links from SEO CSV; **no prices**
- [ ] ≥4 internal links + ≥1 authoritative external link
- [ ] **Image SEO:** KW-led WebP filenames; unique alts (primary KW in hero); descriptive WP media titles on upload; carousel alts = `{KW/occasion + year} gift idea: {Product Name}`; body alts match media library; featured ≠ body image (see `HIGGSFIELD_IMAGE_GENERATION.md`)

## G. Schemes & policies (only if relevant)
- [ ] Correct CTA; no invented %, fees, eligibility
- [ ] Manual Fact-Check List for every number

## H. Integrity
- [ ] No fake stats, reviews, experts, or “real customer” stories
- [ ] No competitor disparagement / false urgency / medical claims

## I. Final gate
- [ ] Checklist cleared
- [ ] Schema in CMS
- [ ] Live URL on plan sheet = Published
- [ ] claude-seo optional only (not required for festive wishes)
- [ ] Title B noted for same-URL CTR test later (not a second post)
- [ ] **Festive year** = next upcoming festival year if that festival already passed this calendar year
- [ ] Author = named editorial (**Vikas**); byline on page
- [ ] Live page has exactly one **`<h1>`** (fix theme if title is an H2)
- [ ] Featured/hero is WebP (or AVIF), not heavy PNG where avoidable
- [ ] Meta description ~150–160 chars when possible
- [ ] No Classic-block leftovers for restored sections (use `wp:heading` / `wp:list` / `wp:paragraph`)
