# BlueStone Article Workflow (canonical)

SEO is built into Master Prompt v5 + Checklist v2. **Do not use claude-seo to draft.**

---

## Pipeline (every plan row)

**Policy (2026-07-19):** **New blogs only.** Ignore sheet `Action = Optimize`. Always publish a fresh WP post/slug. Do not patch old BlueStone URLs for remaining queue rows. Completed historical Optimize posts stay as-is.

1. Pick plan row (primary + supporting KWs, competitor URL, volume/KD). Treat Action as **New**.
2. Competitor analysis skill → filled artifact (structure / gaps only, never copy)
3. Article Brief (v5 template): next upcoming festival year, one **new** URL for near-duplicates, 80/20 wishes
4. Draft with `bluestone-blog-master-prompt-v5.md`
5. Soft CTA: 5–6 SKUs from `Seo Products - final products (1).csv` (PDP `Link`, **no prices**)
6. Images (see Image system below)
7. Push WordPress **new post** via API (`publish_*` scripts)
8. Yoast via API (focus keyphrase, SEO title, meta description)
9. Polish: KW in intro, alts, inclusive language, ≥4 internal + ≥1 external, **dash rules**
10. Visible FAQ HTML (5–10 Qs) + FAQPage + BlogPosting JSON-LD
11. Checklist v2 pass/fail
12. Publish + live URL on plan sheet
13. Title A live; Title B = same-URL CTR rewrite later (never a second post)

---

## H2 / section strategy

| Priority | Source | Placement |
|---|---|---|
| **Spine (~70–80%)** | Volume-backed supporting KWs from plan / URL group | Higher H2s + most FAQs |
| **Parity (~20–30%)** | Competitor buckets with no/weak volume (funny, long-distance, colleagues, etc.) | Lower, shorter; keep for coverage |
| **Never** | Soft buckets as separate URLs | Stay on this pillar URL |

One **new** URL covers the full Semrush/CaratLane cluster. Near-duplicates (`msg` / `msgs`) share that new URL. Do not reopen an old Optimize target for the same intent.

---

## Festive year rule (mandatory)

Use the **next upcoming edition** of the festival in title, slug, H1, body, FAQs, alts, and meta.

- If today’s date is **after** that festival in the current calendar year, publish/refresh as **next year** (e.g. Holi mid-March → from April onward use Holi **2027**, not 2026).
- On refresh: update slug (`…-2027`), all visible year mentions, Yoast title/meta, schema `dateModified`, featured/hero alts.
- Keep a **301** from the old year URL to the new slug (Yoast “redirect old URL” on slug change, or Redirection plugin).
- Re-check before the season (usually 6–8 weeks out) and bump `dateModified` again.

## E-E-A-T / author

- Author display name: **Vikas** (WP user).
- On-page byline only when useful for EEAT/SEO: short form `By Vikas, BlueStone Editorial` (no extra marketing sentence).
- Do **not** add a “Last updated: …” line in the body unless there is a clear editorial need; prefer Yoast/schema `dateModified` for freshness.
- Do not leave posts as anonymous `blogbluestone` on festive SEO articles.

## H1 / post title (Creatio theme)

Site-wide single template (`creatio//single`, customized WP template id **29900**) uses **`<!-- wp:post-title {"level":1,...} /-->`** above the featured image.

- Do **not** hide `.wp-block-post-title` with article CSS.
- Do **not** inject a duplicate content `<h1>` for the post title.
- Verify one `<h1>` on the live HTML (the theme post title).

## Hero / LCP

Prefer **WebP** (or AVIF) for featured/hero; set meaningful alt; avoid large PNGs for photo/graphic heroes.

- No em dashes (`—`) or en dashes (`–`)
- **Do not write `word - word`** (spaces around hyphen): WordPress `wptexturize` turns it into an en dash on the live page. Use `,` or `:` instead  
  Example: `keep it light and wearable, something that works after the colours wash off.`
- Next upcoming festival year in title/body/FAQs/alts (see festive year rule above)
- No prices in blogs; no fake stats; no competitor digs

---

## Image system (3 types)

| Type | What | Folder | Use |
|---|---|---|---|
| **1. Raw** | kinclimg / studio, accurate jewellery | `ProductImages/raw/` | Reference **only** when generating Type 2 or 3 with jewellery |
| **2. AI product** | Styled product shot of same SKU | `ProductImages/seo images/` | **Carousel + Buy now** (mid-article) |
| **3. AI concept** | **Higgsfield MCP** (`nano_banana_pro`) | Featured + in-body atmosphere |

Rules:
- Never use the same image twice in one article (featured counts)
- Carousel = Type 2 only, **mid-article** with soft gift CTA, **never last block**
- After carousel: tips / links / conclusion / **visible FAQs** still required
- Type 3: generate via **Higgsfield MCP** (`HIGGSFIELD_IMAGE_GENERATION.md`). Run **after** text publish; patch images last.
- For Type 3: read Type 1 raw JPGs for accurate SKU description in prompts. Skip `--structure-ref` for people/lifestyle scenes (approved Rank 5 workflow).

### Image SEO (mandatory)

Full table: `HIGGSFIELD_IMAGE_GENERATION.md` → **Image SEO**.

Minimum bar every publish:
1. **WebP** filenames: Type 3 `{occasion}-{slot}-{year}.webp`; Type 2 `{product-slug}-carousel.webp`
2. **Unique alts** with locked festive year + product/scene; **primary KW in hero alt**
3. **Carousel alts:** `{occasion/KW + year} gift idea: {Product Name}`
4. **WP media library titles** descriptive (not `IMG_1234` / bare slug only)
5. Set `alt_text` + `title` on media upload; keep body `wp:image` alts in sync
6. Gutenberg Type 3 blocks: `sizeSlug: full` only (no `large` + width/height/loading)

---

## Soft CTA / carousel

- ~80% shareable wishes / ~20% brand
- One mid-article gift section + coverflow carousel (Type 2, 16:9, product name + **Buy now**)
- Trust line OK (shipping / 30-day) without scheme dump on pure wishes posts

---

## Optional QA (not default)

| Tool | When |
|---|---|
| Checklist v2 | **Every article** |
| claude-seo `/seo` or `/geo` | Hard head terms or rank/CTR stall only. Skip most festive listicles |
| WP “Improve with AI” | Avoid |

---

## Key files

| Asset | Path |
|---|---|
| Master prompt | `KnowledgeBase/Writing/bluestone-blog-master-prompt-v5.md` |
| Checklist | `KnowledgeBase/Writing/Blog-SEO-AEO-GEO-Checklist-v2.md` |
| Competitor skill | `KnowledgeBase/Writing/competitor-blog-analysis-SKILL.md` |
| This workflow | `KnowledgeBase/Writing/ARTICLE_WORKFLOW.md` |
| Products CSV | `Seo Products - final products (1).csv` |
| Week plan | [SEO Strategy 2026.xlsx](file:///Users/vikasindoria/Documents/Geo%20and%20Seo/SEO%20Strategy%202026.xlsx) (Sheet: "Week 1-2") |
| Type 1 raw | `ProductImages/raw/` |
| Type 2 AI product | `ProductImages/seo images/` |
| Schemes / policies | `KnowledgeBase/Schemes/`, `KnowledgeBase/Policies/` |
