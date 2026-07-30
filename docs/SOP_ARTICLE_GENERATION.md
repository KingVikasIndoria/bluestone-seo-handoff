# SOP: End-to-End Blog Article Generation Playbook (Final)

**Version:** 2026-07-16  
**Client:** BlueStone (Indian jewellery)  
**Workspace:** `/Users/vikasindoria/Documents/Geo and Seo`

---

## How to use this document

This is the **primary runbook** for any agent drafting and publishing festive SEO articles.

**Read order:**
1. **This SOP** (execution steps)
2. **`SEO Strategy 2026.xlsx` → Sheet `Week 1-2`** (what to write next)
3. **`bluestone-blog-master-prompt-v5.md`** (how to draft)
4. **`competitor-blog-analysis-SKILL.md`** (competitor pass template)
5. **`Blog-SEO-AEO-GEO-Checklist-v2.md`** (pre-publish QA gate)
6. **`ARTICLE_WORKFLOW.md`** (canonical rules reference)
7. **`CODEX_HANDOFF.md`** (project state, pitfalls, WP setup)

**Do not use claude-seo to draft.** Checklist v2 is mandatory before publish.

---

## Single source of truth

| What | Where |
|---|---|
| **Execution queue** | `SEO Strategy 2026.xlsx` → **`Week 1-2`** |
| **Later queue** | Same workbook → **`Week 3-4`** |
| **Keyword clusters** | Sheet **`33 Groups festive`** / **`Keywords Grouping festive`** |
| **Approved products** | `Seo Products - consolidated.csv` (legacy: `Seo Products - final products (1).csv`) |
| **Type 1 raw (reference)** | `ProductImages/raw/<category>/` |
| **Type 2 carousel images** | `ProductImages/seo images/<category>/` |
| **Gold reference post** | Holi WP **#29853** → https://blog.bluestone.com/happy-holi-wishes-messages-quotes-2027/ |
| **Carousel HTML template** | `output/_holi_carousel_snippet.html` (extend to 5–6 cards) |

After every publish, **update the target row in `Week 1-2`** (URL, slug, execution note). Do not rely on a separate CSV as the master plan.

---

## WordPress API setup

Set credentials in the shell environment only (never commit to git or xlsx):

```bash
export WP_USER='blogbluestone'
# Type 3 images: Higgsfield MCP in Cursor (no MAGNIFIC_API_KEY)
```

| Item | Value |
|---|---|
| API base | `https://blog.bluestone.com/wp-json/wp/v2/` |
| Festive author | **Vikas** (WP user ID **`270271338`**) |
| Theme | Creatio; single template customized **`wp_id` 29900** |
| Post title | Renders as **`<h1>` above featured image** site-wide |

---

## Hard rules (never break)

### Festive year
Use the **next upcoming edition** of the festival in title, slug, H1, body, FAQs, alts, meta, and schema.

- If today's date is **after** that festival in the current calendar year → use **next year** (e.g. Eid Mar 2026 passed → write **Eid 2027**).
- On slug change from an old year URL → set up **301 redirect** (Yoast redirect or Redirection plugin).
- Re-check ~6–8 weeks before the season and bump schema `dateModified`.

### One URL model
Near-duplicates share one pillar URL (`eid msg` / `eid msgs` / `eid message` = same post). Do not spin separate posts.

### H2 strategy
| Priority | Share | Placement |
|---|---|---|
| **Volume spine** | ~70–80% | Higher H2s + most FAQs (WhatsApp, family, friends, captions, quotes, greetings) |
| **Competitor parity** | ~20–30% | Lower, shorter (funny, long-distance, colleagues, romantic) |

### Commerce (80/20)
- ~80% shareable wishes / ~20% brand
- **One** mid-article soft gift section + coverflow carousel
- Carousel **never** the last block; continue with tips, links, conclusion, **visible FAQs**
- **No prices** anywhere in the article

### Formatting
- **No em dashes (`—`) or en dashes (`–`)**
- **No spaced hyphens** (` word - word `): WordPress `wptexturize` converts them to en dashes. Use `,` or `:`.
- **No "Last updated: …"** in the body (use schema `dateModified` only)

### H1 / title (theme fix applied)
- Theme post title = single **`<h1>` above the hero**
- **Do not** hide `.wp-block-post-title` with CSS
- **Do not** inject a duplicate `<h1>` inside post content
- Optional byline in content: `By Vikas, BlueStone Editorial`

### Images (3 types)
| Type | Source | Use |
|---|---|---|
| **1 Raw** | `ProductImages/raw/` | Reference only when generating jewellery in Type 2/3 |
| **2 AI product** | `ProductImages/seo images/` | Mid-article carousel + Buy now |
| **3 AI concept** | Generated per article | Featured + in-body mood/lifestyle |

Image rules:
- Never reuse the same image twice (featured counts)
- Type 2 = carousel only; Type 1 raw never as carousel hero
- Type 3: show BlueStone jewellery **when it fits the scene**. Read **Type 1 raw JPGs** for accurate SKU description in prompts. Structure ref optional (skip for people/lifestyle scenes). No invented/fake jewellery.
- Convert to **WebP**; hero/featured prefer WebP for LCP

### Title A / Title B
- Ship **Title A** on publish
- **Title B** = same-URL CTR rewrite later (never a second post for the same intent)

### Content integrity
- No competitor copy; structure only from competitor pass
- No fake stats, no competitor digs
- Products/SKUs only from approved CSV

### Known bug (Holi incident)
When splicing carousel HTML in scripts, **always** use:

```python
content = content[:m.start()] + car + content[m.end():]   # colon required
```

Using `content[m.end()]` (no colon) **truncates the entire article** after the carousel (FAQs and sections vanish). Never run greedy regex over whole post bodies.

---

## Pipeline overview

```
Week 1-2 row → Competitor pass → Brief → Draft (v5) → Type 2 carousel WebPs → WP **new** publish → Yoast → FAQs + schema → Checklist v2 → Higgsfield Type 3 (last) → Upload images → Patch post → Live audit → Update xlsx
```

---

## Step 0: Pick the plan row

### 0.1 Open workbook
- File: **`SEO Strategy 2026.xlsx`**
- Sheet: **`Week 1-2`**
- Pick the next row with empty **Bluestone Blog URL** (e.g., Rank 7 = Engagement Quotes)

### 0.2 Copy from the row
- Primary Keyword
- Supporting Keywords (pipe-separated)
- Action: **always treat as New** (ignore `Optimize` on the sheet)
- Suggested URL Slug (override with year rule if needed; create a **new** slug, do not reuse an old Optimize URL)
- CaratLane URL
- Volume, KD (for outline weight only)

**Policy (2026-07-19):** Publish new posts only. Do not patch existing BlueStone URLs for remaining Week 1-2 rows. Historical Optimize ranks already shipped stay as-is.

### 0.3 Lock the target year
Example for Eid (July 2026): **2027** everywhere.  
Suggested slug: `happy-eid-mubarak-wishes-messages-quotes-2027`

---

## Step 1: Competitor structure pass

Follow **`competitor-blog-analysis-SKILL.md`**. Save artifact, e.g. `output/Week1_Rank{N}_{Topic}_Competitor_Analysis.md`.

Extract only:
- Title/H1 formula
- H2/H3 buckets and list sizes
- CTA/product placement
- FAQ presence
- Gaps vs BlueStone (WhatsApp, captions, year, FAQs)

**Never copy** competitor sentences, wish lists, or product blurbs.

For Eid, competitor: https://www.caratlane.com/blog/eid-mubarak-wishes-ramadan-mubarak-wishes-quotes/  
Existing analysis: `output/Week1_Rank2_Eid_Competitor_Analysis.md`

---

## Step 2: Build the 1-page brief

Include:
- **Title A** (with target year)
- **Meta title** (≤60 chars preferred)
- **Meta description** (~150–160 chars)
- **Slug**
- **TL;DR** (2–4 lines)
- **Ordered H2 map** (spine first, parity lower)
- **5–10 FAQs** mapped to supporting keywords first
- **Commerce plan:** one soft gift H2 + 5–6 product carousel mid-article

Draft the article using **`bluestone-blog-master-prompt-v5.md`** (`soft-products` = 5–6 SKUs).

---

## Step 3: Product selection (Type 2 carousel)

### 3.1 Rules
- Source: **`Seo Products - consolidated.csv`** (GenderTag + height_mm/width_mm required for Type 3)
- Count: **exactly 5–6 products** in the coverflow carousel
- Each card: Type 2 WebP image + product name (plain text) + black **Buy now** → live PDP
- No prices

### 3.2 Eid 2027 locked SKUs (6 products)

| # | Product | Design code | Category | PDP |
|---|---|---|---|---|
| 1 | The Rohal Huggie Earrings | BIPM0001H28 | Earrings | https://www.bluestone.com/earrings/the-rohal-huggie-earrings~21864.html |
| 2 | The Valeria Rose Pendant | BIHS1145P21 | Pendants | https://www.bluestone.com/pendants/the-valeria-rose-pendant~181266.html |
| 3 | The Shining Star Bracelet | BIMG0635V45 | Bracelets | https://www.bluestone.com/bracelets/the-shining-star-bracelet~63731.html |
| 4 | The Liza Ring | BIAR0097R07 | Rings | https://www.bluestone.com/rings/the-liza-ring~7623.html |
| 5 | The Gigi Ring | BINS0639R18 | Rings | https://www.bluestone.com/rings/the-gigi-ring~64382.html |
| 6 | The Asya Huggie Earrings | BISA0255D05 | Earrings | https://www.bluestone.com/earrings/the-asya-huggie-earrings~13494.html |

For other articles, pick 5–6 occasion-fit SKUs from the CSV (earrings, pendants, bangles for Eid per product-selection guide).

### 3.3 Carousel placement
- One H2 such as *A soft Eid gift idea (if you are gifting too)*
- Carousel **mid-article**, after family/friends spine sections, **before** captions/quotes/parity buckets
- After carousel: more H2s, tips, internal links, conclusion, visible FAQs

### 3.4 Carousel HTML
- Base template: `output/_holi_carousel_snippet.html` (currently 3 cards; **extend to 6** for Eid)
- Reference live implementation: Holi post **#29853**
- When editing via script, use safe splice (see Hard rules above)

---

## Step 4: Images

### 4.1 Type 2 (carousel) — SEO images only
- Source PNG: **`ProductImages/seo images/<Category>/<Exact Product Name>.png`** only
- **Never** use `ProductImages/raw/` or CDN raw packshots for carousel cards (raw is for Type 3 reference only)
- Convert to **WebP**, **960×535** (16:9), quality ~82; filename `{product-slug}-carousel.webp`
- Alt format: `{Primary KW or occasion + year} gift idea: The [Product Name]` (include year)
- WP media title: `{Product Name} carousel — {Occasion} {year}`
- Upload to WP with `alt_text` + `title`; record media IDs in `output/Week1_Rank{N}_{Topic}_product_media.json`
- Full Image SEO table: `HIGGSFIELD_IMAGE_GENERATION.md`

**Eid assets ready (3 of 6):** `output/Week1_Rank2_Eid_assets/`  
Still needed: Liza Ring, Gigi Ring, Asya Huggie WebPs.

### 4.2 Type 3 (concept: hero + 2 in-body)

**Visual guide:** `HIGGSFIELD_IMAGE_GENERATION.md` (Higgsfield MCP; Magnific retired).

**Pipeline:** Article first → CDN product angles → write hyper-real prompts → Higgsfield MCP → patch WP.

1. Finish article text + Type 2 carousel; publish/save WP draft
2. Collect 3–5 CDN product angles per Type 3 SKU; note exact materials
3. Write `output/Week1_Rank{N}_{Topic}_type3_prompts.json` (copy template)
4. Higgsfield MCP: `media_import_url` → `generate_image` (`nano_banana_pro`, 16:9, 2k) → WebP
5. Upload + patch featured + body images (`scripts/patch_{occasion}_type3_clean.py`)

Generate **3 concept images** via **Higgsfield MCP**:
- **`theme_anchor`** + **`negative_prompt`** locked in manifest (hyper-real campaign block)
- **Detailed lifestyle prompt** per slot + `@img1…` matching imported medias
- **Fair-skinned Indians** for people/hand/wrist slots
- Canva style refs **optional**

See `HIGGSFIELD_IMAGE_GENERATION.md`. Auth via Cursor MCP (no Magnific key).

1. **Hero / featured** — people + jewellery gifted/worn; warm home; 85mm mid-shot
2. **Flatlay** — lived-in desk + props; 100mm macro top-down
3. **Lifestyle** — action close-up; jewellery on wrist, sharp focus; 85mm mid-shot

**When to run:** Generate Type 3 **last**, after draft/publish. Upload to WP and patch post (featured + body blocks).

Type 3 rules:
- Default model: **nano_banana_pro** + hyper-real theme anchor + negative prompt
- Convert to **WebP** (~1400px wide, 16:9, q~82); filename `{occasion}-{hero|flatlay|lifestyle}-{year}.webp`
- Unique alts with **primary KW + year + scene/product**; set WP media `title` + `alt_text` on upload (see Image SEO in `HIGGSFIELD_IMAGE_GENERATION.md`)
- **Phone screens:** blank/dark only (never prompt for greeting text)
- No logos, no competitor branding, no fake product renders
- Never reuse featured image in the body
- Gutenberg body blocks: `sizeSlug: full` only (no `large` + width/height/loading)
- Run hygiene checks (see `HIGGSFIELD_IMAGE_GENERATION.md`)

---

## Step 5: Draft the article

### 5.1 Opening
- Direct answer in first 2–3 sentences
- TL;DR near top (bullets OK)
- Primary keyword in first 100 words

### 5.2 Body structure (Eid example)
**Spine (higher):**
- Short Happy Eid Messages for WhatsApp
- Heartfelt Eid Mubarak Wishes for Family
- Happy Eid Messages for Friends
- Religious & Inspirational Eid Wishes
- **Soft gift H2 + 5–6 product carousel**
- Eid Captions for Instagram & Status
- Eid Quotes & Happy Eid Quotations

**Parity (lower, shorter):**
- Romantic Eid Mubarak Wishes
- Eid Wishes for Long-Distance Loved Ones
- Happy Eid Wishes for Colleagues
- Funny Eid Mubarak Wishes

**Close:**
- How to pick the right Eid message (tips)
- More festive wishes to explore (internal links)
- Conclusion
- **Frequently Asked Questions** (visible HTML)

### 5.3 List quality
- 40–75+ distinct lines across sections (not padding)
- Mix one-liners (WhatsApp) and 2–3 line messages
- No near-duplicate rephrasing

### 5.4 Links
- **≥4 internal** festive posts (Holi 2027, Diwali, Rakhi, New Year, etc.)
- **≥1 external** authoritative (e.g. Wikipedia Eid)

### 5.5 Byline (optional, recommended)
Centered paragraph: `By Vikas, BlueStone Editorial`

---

## Step 6: FAQs + JSON-LD

### 6.1 Visible FAQs (HTML)
- Heading: **Frequently Asked Questions about [Topic]**
- **5–10 questions**; answers **40–80 words**; answer in first sentence
- Map to supporting keywords first, e.g.:
  - What are some short Happy Eid messages for WhatsApp?
  - What is a good Eid caption for Instagram?
  - What are the best Eid Mubarak wishes for 2027?
  - How do you write a heartfelt Eid wish for family?

### 6.2 JSON-LD (end of post content)
Embed two blocks in `<!-- wp:html -->`:

1. **FAQPage** — mirrors visible FAQs  
2. **BlogPosting** — headline, description, author `{@type: Person, name: Vikas}`, datePublished, dateModified, mainEntityOfPage (live URL), keywords, image array (hero + body + carousel WebPs)

Yoast also outputs an `@graph` (Article, WebPage, etc.). Both are fine.

---

## Step 7: WordPress publish

### 7.1 Upload media
`POST /wp/v2/media` for hero, 2 body images, 5–6 carousel WebPs.

### 7.2 Create post (draft first)
```json
{
  "title": "75+ Happy Eid Mubarak Wishes, Messages & Quotes for 2027",
  "slug": "happy-eid-mubarak-wishes-messages-quotes-2027",
  "status": "draft",
  "author": 270271338,
  "featured_media": <hero_media_id>,
  "content": "<Gutenberg block markup>",
  "excerpt": "<meta description>",
  "meta": {
    "_yoast_wpseo_focuskw": "happy eid msg",
    "_yoast_wpseo_title": "Happy Eid Mubarak Wishes, Messages & Quotes 2027 | BlueStone",
    "_yoast_wpseo_metadesc": "<150-160 char description>"
  }
}
```

### 7.3 Content blocks checklist
- Gutenberg blocks (not Classic HTML soup)
- Byline paragraph (if used)
- Intro + TL;DR
- All H2 sections + numbered/bullet lists
- Mid-article carousel (5–6 products)
- Visible FAQ section
- JSON-LD scripts
- **No** injected H1; **no** CSS hiding post title

### 7.4 Publish
Set `status: publish`. Hard-refresh live URL with cache-bust (`?v=1`).

---

## Step 8: Live audit (must pass)

- [ ] Exactly **one `<h1>`** in DOM = theme post title **above** featured image
- [ ] All planned H2 sections present (spine + parity)
- [ ] Carousel mid-article with **5–6 products**; Buy now links work
- [ ] Sections **after** carousel (tips, links, conclusion, FAQs)
- [ ] Visible **Frequently Asked Questions** at bottom
- [ ] **FAQPage** + **BlogPosting** JSON-LD parse cleanly
- [ ] Images WebP with unique alts
- [ ] Author Vikas; byline if used
- [ ] No body "Last updated"
- [ ] No em/en dashes; no `word - word`
- [ ] No prices
- [ ] Primary KW in title, meta, intro, hero alt; Image SEO (filenames, unique alts, media titles)
- [ ] Images WebP with unique KW-led alts (see HIGGSFIELD Image SEO)

Run full **`Blog-SEO-AEO-GEO-Checklist-v2.md`** and save pass artifact if desired (`output/Week1_Rank{N}_{Topic}_Checklist_v2.md`).

---

## Step 9: Update planning workbook

Open **`SEO Strategy 2026.xlsx` → `Week 1-2`**. Update the target row:

| Column | What to fill |
|---|---|
| **Bluestone Blog URL** | Full published URL |
| **Suggested URL Slug** | Final slug if changed |
| **Execution Note** | Publish date, WP post ID, year, author, Yoast KW, schema OK, product SKUs used, any fixes |

Do not overwrite other rows (Holi Rank 1 already synced).

---

## Step 10: What comes next

After Eid (Rank 2), proceed to **Rank 3** in `Week 1-2` (`propose a girl`) using this same SOP.

---

## Current project state (as of 2026-07-16)

| Article | Rank | Status |
|---|---|---|
| Holi 2027 | 1 | **Published** — WP#29853, live, H1 theme fix applied |
| Eid 2027 | 2 | **Not published** — competitor analysis done; 3/6 carousel WebPs ready |
| propose a girl | 3 | Not started |

**Next agent task:** Complete Eid end-to-end from Step 2 onward; read `CODEX_HANDOFF.md` for WP credentials and pitfalls.

---

## Quick copy-paste prompt for a new agent

```
Read KnowledgeBase/Writing/SOP_ARTICLE_GENERATION.md fully.
Read SEO Strategy 2026.xlsx → Week 1-2 → Rank 2 (Eid).
Use output/Week1_Rank2_Eid_Competitor_Analysis.md and competitor-blog-analysis-SKILL.md.
Draft with bluestone-blog-master-prompt-v5.md.
Build 6-product carousel (extend output/_holi_carousel_snippet.html).
Generate 3 Type 3 WebP images (jewellery from Type 1 raw ref if shown).
Publish via WP API (author 270271338). Run Blog-SEO-AEO-GEO-Checklist-v2.md.
Update Week 1-2 row for Rank 2 in SEO Strategy 2026.xlsx.
Do not redo Holi unless asked. Read CODEX_HANDOFF.md for env vars and the carousel splice bug.
```
