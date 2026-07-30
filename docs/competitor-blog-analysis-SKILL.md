---
name: competitor-blog-analysis
description: >-
  Analyzes a competitor jewellery blog page (especially CaratLane) to produce a
  BlueStone writing outline. Captures H2 structure, list style, FAQs, CTAs,
  products, schema signals, SERP gaps, and a no-copy brief. Use when the user
  asks for a competitor pass, CaratLane outline, Rank/Week blog prep, structure
  benchmark, or before drafting a festive wishes/gift/education post.
---

# Competitor Blog Analysis (BlueStone)

Run this **before drafting** any festive or gift blog that has a competitor URL (usually CaratLane). Queue policy: **New posts only** (ignore Optimize).

**Output goal:** a complete **outline + gap map + BlueStone brief inputs** — never plagiarized copy.

## When to use
- Week 1–N plan row has a `CaratLane URL`
- User says “competitor pass”, “analyze CL page”, “outline from CaratLane”
- Before writing with Master Prompt v5

## Inputs required
| Input | Source |
|---|---|
| Competitor URL | Plan `CaratLane URL` |
| Primary keyword | Plan row |
| Supporting keywords | Plan row (top ~8) + full pool if available |
| Article type | festive wishes / gift / education / calendar |
| BlueStone product list | `Seo Products - consolidated.csv` (GenderTag + mm sizes; legacy: `Seo Products - final products (1).csv`) |

## Hard rules
1. **Structure only** — extract outline, patterns, intents. Do **not** copy sentences, wish lists, or product blurbs.
2. **One URL model** — competitor ranks one page for many variants; BlueStone does the same.
3. **Recency** — BlueStone draft uses **2026** only, even if competitor shows older years.
4. **80/20 for wishes** — competitor may push products hard; BlueStone wishes posts stay ~80% shareable / ~20% brand.
5. Products for BlueStone CTAs come **only** from the approved product CSV — never invent SKUs.

---

## Workflow

### Step 1 — Fetch the page
- Open/fetch the competitor URL (full article body).
- Also note title tag, H1, meta description if available.
- Skim related posts / tags / category.

### Step 2 — Fill the analysis template (mandatory sections)
Produce the output in the **Output template** below. Skip a section only if truly N/A (mark `N/A`).

### Step 3 — Map to BlueStone outline
Convert competitor H2s into a **BlueStone H2 plan** that:
- Covers the same intent buckets
- Adds gaps (missing WhatsApp / captions / year / FAQs)
- Places supporting keywords into H2 or FAQ
- Places **1 soft product CTA** (wishes) or stronger CTAs (gift guides) using approved products

### Step 4 — Hand off
Return analysis + ready-to-paste **Article Brief** for Master Prompt v5.

---

## What to extract (comprehensive checklist)

### A. SERP / page identity
- [ ] Full URL + slug
- [ ] H1 (exact)
- [ ] Implied title formula (Number+Emotion? Occasion+Wishes+Year?)
- [ ] Category / tags
- [ ] Author / date / “last updated” if shown
- [ ] Approximate word count / list count (e.g. “75 wishes”)

### B. Intent & audience
- [ ] Primary search intent (messages / quotes / gifts / how-to / dates)
- [ ] Secondary intents covered
- [ ] Who it’s for (family, friends, WhatsApp, Instagram, etc.)

### C. Structure map (most important)
For every H2 (and major H3):
- Heading text
- Section type: intro | list | tips | products | FAQ | CTA | other
- Approx item count in lists
- List style: numbered / bullets / cards
- Tone of that section (traditional / funny / religious / short)

### D. List & content patterns
- [ ] Total wish/quote/message count
- [ ] Bucket types present (short, heartfelt, funny, family, status, religious…)
- [ ] Intro pattern (story / definition / direct answer?)
- [ ] Conclusion pattern
- [ ] TOC present?

### E. Keyword / entity coverage
- [ ] Which of **our supporting keywords** appear as headings or strong phrases?
- [ ] Which supporting KWs are **missing** (BlueStone opportunity)?
- [ ] Near-duplicates treated as one page? (msg/msgs, wish/wishes)

### F. FAQ / PAA layer
- [ ] On-page FAQs? (questions listed)
- [ ] Implied FAQ themes even without an FAQ block
- [ ] Suggest 5–10 BlueStone FAQs mapped to **volume-backed** supporting KWs first

### G. Commerce / CTA map
- [ ] Where product modules appear (after which H2)
- [ ] How many product embeds / “shop now” blocks
- [ ] Gift-guide / collection links vs single SKUs
- [ ] Mid-article vs end CTA
- [ ] Soft vs hard sell intensity (score 1–5)

### H. Trust / policy / brand extras
- [ ] Any trust lines (returns, certification)?
- [ ] Internal links to related festive posts
- [ ] External links?

### I. Technical / AEO signals (lightweight)
- [ ] Question-style headings?
- [ ] Tables?
- [ ] Schema hints if visible (FAQ, Article)
- [ ] Passage-friendly short blocks? (yes/no)
- [ ] Image types (lifestyle / product / graphics)

### J. Strengths & weaknesses
- [ ] What likely helps them rank?
- [ ] What’s thin, outdated, or over-commercial?
- [ ] Year freshness?
- [ ] Mobile scanability?

### K. BlueStone beat plan
- [ ] Sections to **match**
- [ ] Sections to **add** (gaps)
- [ ] Sections to **skip** or soften (over-sell)
- [ ] Title options for 2026
- [ ] Recommended slug
- [ ] Product picks from approved CSV (see Product selection)

---

## Product selection (from approved CSV)

File: `Seo Products - consolidated.csv` (or legacy `Seo Products - final products (1).csv`)  
Columns: Design Code, Design Name, Image link, ItemCategory, sellingPrice, DesignCategory

**Wishes posts (80/20):** pick **5–6 products**, preferably **2 categories**, mid-article soft CTA only.

| Occasion / angle | Prefer DesignCategory |
|---|---|
| Holi / colorful festive | Earrings, Pendants, Bracelets (lighter/fashionable) |
| Diwali / prosperity | Pendants, Earrings, Bangles, Chains |
| Rakhi / sibling | Adjustable Bracelets, Kids Bracelets, Evil Eye pieces, Bracelets |
| Eid | Earrings, Pendants, Bangles |
| Proposal / engagement / Valentine | Rings, Pendants |
| Wedding / anniversary | Rings, Mangalsutra Chains, Bangles, Necklaces |
| Men’s gifting | Bracelets For Him, Rings For Him, Pendants For Him |
| Kids / Children’s Day | Kids Bracelets |
| Everyday / friendship | Pendants, Earrings, Charms (accessible price if possible) |

**Rules**
- Always include Design Code + Design Name + Image link in the brief.
- Prefer mix of price bands when possible (not only ultra-premium).
- For wishes: do **not** dump 8+ products.
- Never invent products outside the CSV.

---

## Output template (always use)

```markdown
# Competitor Blog Analysis

## Meta
- Competitor URL:
- Primary KW (ours):
- Article type:
- Analyzed on:

## A. Page identity
- H1:
- Title formula guess:
- List scale:
- Category/tags:

## B. Intent
- Primary:
- Secondary:

## C. Structure map
| # | Heading | Type | Items | Notes |
|---|---|---|---|---|
| 1 | ... | list | 10 | short WhatsApp |

## D. CTA / commerce map
| Placement | What | Intensity 1–5 |
|---|---|---|
| After H2 X | product grid | 4 |

## E. Supporting KW coverage
| Supporting KW | On competitor? | BlueStone placement |
|---|---|---|
| holi caption | yes/no | H2 Captions |

## F. FAQ candidates (BlueStone)
1. ... (from KW: ...)
2. ...

## G. Gaps to beat
- ...

## H. BlueStone outline (do not copy competitor text)
1. H1: ...
2. TL;DR
3. H2: ...
4. ...
5. Soft product CTA (5–6 SKUs)
6. FAQs
7. Conclusion

## I. Approved products for this post
| Design Code | Name | Category | Price | Why fit |
|---|---|---|---|---|
| ... | ... | Earrings | ... | Holi festive |

## J. Ready Article Brief (paste into v5)
(see brief block below)
```

### Ready Article Brief block

```
Primary keyword:
Article type: [festive wishes | gift guide | education | comparison | calendar]
Action: New
Competitor / CaratLane URL:
Supporting keywords:
Year to use: 2026
Required CTAs: [none | soft-products | gift-collection | Gold Mine | Gold Reserve | Old Gold Exchange | 30-day/LTE]
Products (from approved CSV):
- CODE | Name | Category | image URL
- CODE | Name | Category | image URL
Collection URL (if any):
BlueStone H2 outline:
- ...
Extra notes: one URL for msg/msgs variants; no copied competitor copy; 2026 only
```

---

## Definitions (for the analyst)

### What is the “brief”?
The **Article Brief** is the short handoff block after analysis. It tells the writer/AI exactly what to write (keyword, outline, CTAs, products). It is **not** the article itself.

### What are “Required CTAs”?
CTAs = calls to action in the article. Choose what the draft must include:

| Value | Meaning |
|---|---|
| `none` | No commerce (rare) |
| `soft-products` | 5–6 approved products, light mention (default for wishes) |
| `gift-collection` | Link a collection PLP if provided |
| `Gold Mine` / `Gold Reserve` / `Old Gold Exchange` | Scheme links when topic fits |
| `30-day/LTE` | Trust/policy line for buying confidence |

Wishes default: **`soft-products`** (+ optional `30-day/LTE` one-liner if gifting is mentioned).

---

## Done criteria
Analysis is complete only if:
- [ ] Structure map has all major H2s
- [ ] Supporting KWs mapped to H2/FAQ
- [ ] Gaps listed
- [ ] BlueStone outline written
- [ ] 5–6 approved products selected (for wishes) with codes
- [ ] Ready Article Brief filled
