# Codex Handoff — BlueStone Festive SEO Blog Engine

**Updated:** 2026-07-20  
**Workspace:** Open this folder (`article generation seo codex`) as Codex root  
**Next task:** Rank 54 birthday wishes for principal live (NEW, body_image scale line). Next start Rank 55 if continuing.  
**Ranks 45–50 live:** first birthday baby girl / mothers day thought / teachers day msg / 2-line dosti status / deepavali Tamil / yari status Hindi.  

**Process updates (2026-07-20):** Canonical product list is `Seo Products - consolidated.csv` (merged GenderTag + height/width mm from `designfiltered2026.csv`). Type 3 must match gender + exact mm. See `docs/product/product-selection-guide.md`.
**Process updates (2026-07-19 evening):** Rotate Type 3/carousel products (no Valeria/Muricelle/Rohal default). Add figcaptions under Type 3 body images. Education posts use paragraphs + short takeaways, not bullets-only. See `.cursor/rules/product-rotation-captions-education.mdc` and `output/product_rotation.json`.
**Rank 54 live:** https://blog.bluestone.com/birthday-wishes-for-principal-2026/ (WP#30645)
**Rank 53 live:** https://blog.bluestone.com/merry-christmas-wishes-quotes-2026/ (WP#30630)
**Rank 52 live:** https://blog.bluestone.com/birthday-status-2026/ (WP#30618)
**Rank 50 live:** https://blog.bluestone.com/yari-status-hindi-2026/ (WP#30571)
**Rank 49 live:** https://blog.bluestone.com/deepavali-wishes-in-tamil-2026/ (WP#30564)
**Rank 48 live:** https://blog.bluestone.com/2-line-dosti-status-in-english-2026/ (WP#30557)
**Rank 47 live:** https://blog.bluestone.com/teachers-day-msg-2026/ (WP#30550)
**Rank 46 live:** https://blog.bluestone.com/mothers-day-thought-2027/ (WP#30543)
**Rank 45 live:** https://blog.bluestone.com/first-birthday-wishes-for-baby-girl-2026/ (WP#30536)
**Rank 30 live:** https://blog.bluestone.com/akshaya-tritiya-quotes-wishes-2027/ (WP#30340)
**Rank 26 live:** https://blog.bluestone.com/gudi-padwa-meaning-2027/ (WP#30296)
**Rank 25 live:** https://blog.bluestone.com/happy-janmashtami-wishes-quotes-2026/ (WP#30285)
**Rank 24 live:** https://blog.bluestone.com/happy-gudi-padwa-in-marathi-2027/ (WP#30274)
**Rank 23 live:** https://blog.bluestone.com/happy-new-year-wishes-for-love-2027/ (WP#30261)  
**Rank 22 live:** https://blog.bluestone.com/mothers-day-wishes-in-english-2027/ (WP#30248)

---

## Policy (mandatory from 2026-07-19)

**New blogs only.** Ignore sheet `Action = Optimize`.

- Always create a **new** WP post with a fresh slug (`publish_*` flow).
- Do **not** patch old BlueStone URLs for remaining queue rows.
- Historical Optimize ranks already completed (5, 6, 8, 9, 14, 16–20) stay as-is — do not redo unless asked.
- See `.cursor/rules/new-blogs-only.mdc` and `.cursor/rules/image-seo.mdc`.

---

## Type 3 credits

Exactly **3** images per article (hero + flatlay + lifestyle), `count: 1` each. Retry only on QA fail. Prefer photoreal candid wording over “hyper-realistic”.

## Image SEO (mandatory)

Canonical: `docs/HIGGSFIELD_IMAGE_GENERATION.md` → **Image SEO**

- WebP filenames; unique KW-led alts; descriptive WP media titles on upload
- Carousel alts: `{KW/occasion + year} gift idea: {Product Name}`
- Type 3: `{occasion}-{hero|flatlay|lifestyle}-{year}.webp` + primary KW in hero alt
- Gutenberg: `sizeSlug: full` only

---

## Paste this as your first Codex / Cursor message

```
Read these fully first:
- article generation seo codex/HANDOFF.md
- KnowledgeBase/Writing/SOP_ARTICLE_GENERATION.md
- KnowledgeBase/Writing/ARTICLE_WORKFLOW.md
- KnowledgeBase/Writing/HIGGSFIELD_IMAGE_GENERATION.md (especially Image SEO)
- KnowledgeBase/Writing/Blog-SEO-AEO-GEO-Checklist-v2.md
- .cursor/rules/new-blogs-only.mdc
- .cursor/rules/carousel-seo-images.mdc
- .cursor/rules/type3-fair-skinned-indians.mdc
- .cursor/rules/image-seo.mdc

Next article: SEO Strategy 2026.xlsx → Week 1-2 → Rank 22
- Primary KW: mother's day wishes in english
- Action: NEW only (ignore Optimize; do NOT edit https://blog.bluestone.com/50-happy-mothers-day-quotes-heartfelt-wishes-for-your-mom/)
- Volume / KD: 8100 / 28
- Supporting KWs (spine first): mother's day wishes in english | mother quotes in english | happy mothers day mom wishes quotes | mothers day status
- Ignore unrelated sheet noise for H2 spine (sunday quotes, ramadan quotes) unless a short parity note fits
- Competitor: https://www.caratlane.com/blog/happy-mothers-day-quotes-wishes-messages/
- Year: 2027 (Mother’s Day 2026 already passed as of Jul 2026)
- Suggested slug: mothers-day-wishes-in-english-2027 (or similar KW-led NEW slug)
- Category: Festive Wishes (+ Quotes & Wishes if useful). Never leave Uncategorized.

Follow Rank 15 / Rank 21 New publish flow (publish_bhai_dooj_article.py / fix_ugadi_rank21_audit.py patterns):
1. Competitor pass → output/Week1_Rank22_MothersDay_Competitor_Analysis.md
2. Brief + draft NEW Mother’s Day wishes pillar (100+ lines if title claims 100+)
3. Pick 6 products from Seo Products CSV (gifts for mom angle)
4. Type 2 carousel WebPs from ProductImages/seo images/ only → upload with Image SEO alts/titles
5. Publish NEW post via WP API (author Vikas, ID 270271338)
6. FAQs 40–80 words each + BlogPosting + FAQPage schema
7. Type 3 prompts → Higgsfield MCP nano_banana_pro → patch (sizeSlug full + Image SEO)
8. Run Checklist v2; no old years (2021–2025); meta title ≤60; meta desc ~150–160
9. Update Week 1-2 Rank 22 in SEO Strategy 2026.xlsx

Hard rules:
- No prices; products only from Seo Products CSV
- Carousel mid-article, never last block
- Image SEO: KW filenames, unique alts, media titles, primary KW in hero alt
- Type 3: fair-skinned Indians only for people/hand/wrist shots
- Gutenberg images: sizeSlug full only
- No em/en dashes; no "word - word"
- Do not redo Ranks 1–21 unless asked

Env: .env with WP_USER, WP_APP_PASSWORD (Higgsfield via Cursor MCP)
Execute end-to-end and report the live URL when done.
```

---

## Rank 22 brief

| Field | Value |
|-------|-------|
| **Rank** | 22 |
| **Action** | **New** |
| **Primary KW** | mother's day wishes in english |
| **Year** | **2027** |
| **Competitor** | https://www.caratlane.com/blog/happy-mothers-day-quotes-wishes-messages/ |
| **Do not touch** | https://blog.bluestone.com/50-happy-mothers-day-quotes-heartfelt-wishes-for-your-mom/ |

---

## WordPress API

| Item | Value |
|------|-------|
| API base | `https://blog.bluestone.com/wp-json/wp/v2/` |
| Author | **Vikas** — `270271338` |
| Festive category | **Festive Wishes** (`festive-wishes`) |
| Auth | `WP_USER` + `WP_APP_PASSWORD` in `.env` |

---

## Reference implementations

| Flow | Script |
|------|--------|
| **New publish** | `scripts/publish_bhai_dooj_article.py` / Diwali publish |
| **Audit / Image SEO example** | `scripts/fix_ugadi_rank21_audit.py` + live Ugadi #30229 |
| **Type 3** | Higgsfield MCP + `docs/HIGGSFIELD_IMAGE_GENERATION.md` |

---

## After publish

Update **SEO Strategy 2026.xlsx → Week 1-2 → Rank 24**: Bluestone Blog URL + Execution Note.  
Then proceed to Rank 25 as **New**.
