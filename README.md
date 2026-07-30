# BlueStone Article Generation — Codex Pack

Self-contained handoff folder for generating festive SEO articles with Codex (or any external LLM).

**Open this folder as your Codex workspace root.**

---

## Start here

1. Read **`HANDOFF.md`** (project state + paste prompt for Codex)
2. Read **`docs/SOP_ARTICLE_GENERATION.md`** (full runbook)
3. Check **`SEO Strategy 2026.xlsx`** → sheet **`Week 1-2`** for the next rank
4. Set up **`ProductImages/`** (see below — required for carousel + Type 3)
5. Copy **`.env.example`** → **`.env`** and add credentials

---

## Folder map

| Path | Purpose |
|------|---------|
| **`HANDOFF.md`** | Current queue, completed articles, Codex opening prompt |
| **`docs/`** | All writing rules, SOP, master prompt v5, checklist, Type 3 visual guide |
| **`SEO Strategy 2026.xlsx`** | Execution queue (Week 1-2 tab) |
| **`Seo Products - consolidated.csv`** | Canonical SKUs + GenderTag + height/width mm + PDP/CDN (prefer this) |
| **`Seo Products - final products (1).csv`** | Legacy approved list (still OK for download scripts) |
| **`templates/`** | Type 3 prompts template + carousel HTML snippets |
| **`references/`** | Worked examples (Rank 4 Diwali new, Rank 5 Children's Day optimize) |
| **`scripts/`** | Publish, optimize, Type 3 WP patch (Higgsfield MCP for generation) |
| **`output/`** | Generated artifacts go here (create per-article files) |
| **`ProductImages/`** | **You must add this** — see setup below |

---

## ProductImages setup (required)

Carousel (Type 2) and Type 3 prompts need product images. This pack does **not** include the ~420MB `ProductImages/` folder.

**Option A — symlink from parent repo (if both folders sit side by side):**

```bash
cd "article generation seo codex"
ln -s "../ProductImages" ProductImages
```

**Option B — copy from main workspace:**

```bash
cp -R "/Users/vikasindoria/Documents/Geo and Seo/ProductImages" \
      "/Users/vikasindoria/Documents/Geo and Seo/article generation seo codex/ProductImages"
```

See `ProductImages-README.md` for the three image types (raw / seo images / Type 3 generated).

---

## Environment

```bash
cp .env.example .env
# Edit .env:
#   WP_USER=blogbluestone
#   WP_APP_PASSWORD=...
# Type 3 images: Higgsfield MCP in Cursor (no MAGNIFIC_API_KEY)
```

Never commit `.env`.

---

## Read order (docs/)

1. `SOP_ARTICLE_GENERATION.md`
2. `bluestone-blog-master-prompt-v5.md`
3. `competitor-blog-analysis-SKILL.md`
4. `Blog-SEO-AEO-GEO-Checklist-v2.md`
5. `HIGGSFIELD_IMAGE_GENERATION.md`
6. `ARTICLE_WORKFLOW.md`

---

## Typical commands

```bash
# Type 3 images: generate via Higgsfield MCP (see HIGGSFIELD_IMAGE_GENERATION.md),
# then patch WordPress:
python3 scripts/patch_{occasion}_type3_clean.py

# Reference scripts to adapt (do not run blindly — edit products, content, slug)
# Queue policy: New publish only (ignore Optimize). Prefer publish_* templates.
python3 scripts/publish_diwali_article.py           # New publish flow (default)
python3 scripts/publish_bhai_dooj_article.py        # Newer New-publish reference
```

Scripts assume this folder is the **workspace root** (`ProductImages/`, `output/`, `.env` live here).

---

## Live reference posts

| Article | URL | WP ID |
|---------|-----|-------|
| Holi 2027 (gold template) | https://blog.bluestone.com/happy-holi-wishes-messages-quotes-2027/ | 29853 |
| Diwali 2026 (new) | https://blog.bluestone.com/happy-diwali-wishes-messages-quotes-2026/ | 29935 |
| Bhai Dooj (new publish template) | https://blog.bluestone.com/bhai-dooj-wishes/ | 30113 |

Author: **Vikas** (WP user ID `270271338`)
