# BlueStone Image Generation — Complete LLM Handoff

**Purpose:** Everything another LLM needs to generate the 3 Type 3 lifestyle images for a BlueStone SEO blog post and upload them to WordPress.  
**API Used:** **Higgsfield MCP** (`nano_banana_pro`)  
**Output:** 3 WebP images (hero, flatlay, lifestyle) uploaded to WP Media Library  

**Note:** Magnific API is retired for this workflow. Do not use `MAGNIFIC_API_KEY` or `magnific_generate_images.py` for new work.

---

## Files in This Folder

| File | What It Is |
|---|---|
| `HANDOFF_IMAGE_GENERATION.md` | This document — read first |
| `HIGGSFIELD_IMAGE_GENERATION.md` | Visual guide: prompt rules, quality controls, casting |
| `TEMPLATE_type3_prompts.json` | Blank manifest — copy this for every new article |
| `EXAMPLE_fathers_day_prompts.json` | Example manifest shape (update workflow string to Higgsfield) |
| `generate_type3_from_manifest.py` | **Deprecated** Magnific batch helper — do not use for new articles |
| `magnific_generate_images.py` | **Deprecated** Magnific API engine |
| `MAGNIFIC_IMAGE_GENERATION.md` | Stub → points to `HIGGSFIELD_IMAGE_GENERATION.md` |

Canonical copy also lives at:  
`KnowledgeBase/Writing/HIGGSFIELD_IMAGE_GENERATION.md`

---

## Environment Setup

```
WP_USER=blogbluestone
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
WP_SITE=https://blog.bluestone.com
```

Higgsfield auth is via **Cursor MCP** (Higgsfield server). Credits = Higgsfield web/MCP wallet (`balance` tool).  
No Magnific key required.

---

## Step 1: Choose 3 Products and Get CDN URLs

Open `Seo Products - consolidated.csv` (project root). Use `GenderTag` + `height_mm`/`width_mm` in every Type 3 people prompt.  
Pick 3 products (one per slot: hero, flatlay, lifestyle).  
Get their Design Code (e.g. BVEM0663C88).

CDN URL pattern:
```
https://kinclimg{N}.bluestone.com/giproduct/{DESIGN_CODE}_{SKU}_ABCD00-PICS-{ANGLE}-1024-{PRODUCT_ID}.png
```
- N = any digit 0-9 (different mirror subdomains)
- ANGLE = 00000 through 00004 (5 product angles)
- Get 4-5 angles per product (more = better fidelity)

These CDN angles are for **Type 3 reference medias only**.  
Carousel cards must use `ProductImages/seo images/` only.

---

## Step 2: Write the Prompt Manifest JSON

Copy `TEMPLATE_type3_prompts.json`, rename to:
`output/Week1_Rank{N}_{Topic}_type3_prompts.json`

Key fields:
- `workflow`: `Higgsfield MCP nano_banana_pro with CDN product reference medias.`
- `higgsfield.model`: `nano_banana_pro`
- `higgsfield.theme_anchor` / `higgsfield.negative_prompt`
- `slots.hero/flatlay/lifestyle`: `reference_images` + `prompt` + `alt`
- `output`: local WebP paths under `output/magnific_generated/`

---

## Step 3: Generate via Higgsfield MCP

For each product angle URL:
1. `media_import_url` → `media_id`
2. `generate_image` with:
   - model `nano_banana_pro`
   - aspect_ratio `16:9`
   - resolution `2k`
   - medias role `image`
   - prompt = theme_anchor + casting (if people) + slot prompt + `Avoid: ` + negative
3. `job_status` with `sync: true` until completed
4. Download PNG → resize ~1400 wide → WebP quality 82

Optional: `balance` before a batch.

---

## Prompt Formula (adapt per slot)

```
{THEME_ANCHOR}

{CASTING_BLOCK_IF_PEOPLE}

{OCCASION} {SCENE}. A close-up lifestyle shot of {SUBJECT}.
{SUBJECT} wears the identical {PRODUCT_CATEGORY} shown in the reference images (@img1, @img2, @img3, @img4) naturally {ON body part}.
The {product} must be in sharp focus, 100% accurate, and identical in {DESIGN_DETAILS} to the reference images, with zero distortion.
The {product} must be rendered at its actual, natural product scale.
Maintain the exact proportions of the {product} relative to the {body part}, avoiding any oversized, thick, giant, or exaggerated rendering.
This {product} is the single and only piece of jewelry in the entire image. {Others} wear absolutely no other jewelry.
There are absolutely no floating overlays, no separate cutout drawings, and no giant product diagrams anywhere in the image.
Keep the design of these jewelries accurate and do not change it's design.
Add light, shadow and sufficient depth to the jewelleries. Jewelleries in focus.
Hyperrealistic jewelry photography image. Position the jewelries naturally.
Do not change or crop the horizontal composition, fit it in the creative ratio.
Avoid: {NEGATIVE_PROMPT}
• Do not distort or hallucinate the jewelries
```

---

## The 3 Slots

| Slot | Scene | Subject | Product Placement | Lens |
|---|---|---|---|---|
| hero | Warm lifestyle with people | Father hugging child / couple | Worn around neck / on finger | 85mm mid-shot |
| flatlay | Top-down desk / gift scene | No people — props only | On surface, center frame | 100mm macro top-down |
| lifestyle | Action close-up | Man's wrist / hand in motion | On wrist / in hand | 85mm mid-shot |

---

## Standard Theme Anchor

```
High-end commercial jewellery photography, hyper-realistic, HD quality, no distortion of jewellery, identical scale and design, macro-level detail, physically accurate details, natural textures only, no stylization, no illustration. Soft natural window light, warm daylight color temperature, realistic soft shadows, proper shallow depth of field. Shot on high-end DSLR, cinematic realism, 4K resolution, widescreen 16:9 landscape with full frame composition and safe margins. Entire subjects and jewellery fully visible, nothing cropped at frame edges.
```

## Standard Negative Prompt

```
illustration, CGI look, cartoon, fantasy style, over-stylized, plastic glass, fake diamonds, fake gemstones, artificial lighting, studio HDR glow, unreal reflections, blurry jewellery, noise, low detail, AI artifacts, painting, digital art, unreal scale, oversized jewellery, distorted hands, extra fingers, extra bracelets, extra rings, product shot on plain background, cropped faces, cut-off heads, cut-off jewellery, out of frame, readable text, logos, giant rings, exaggerated proportions, dark skin, deep brown skin, heavily tanned skin
```

## Casting block (required for people slots)

```
Casting (required): fair-skinned Indian {SUBJECT} only. Light wheatish to fair North Indian / urban Indian complexion, clear fair skin tones. Do not use deep brown, dark, or heavily tanned skin. Subjects must look ethnically Indian with fair skin.
```

---



## Image SEO (required)

Follow canonical **Image SEO** in `HIGGSFIELD_IMAGE_GENERATION.md`: KW-led WebP filenames, unique alts with primary KW + year, descriptive WP media titles on upload, carousel alts as `{occasion/KW + year} gift idea: {Product Name}`, Gutenberg `sizeSlug: full` only.

## Critical Rules (from Production — Non-Negotiable)

1. FAIR-SKINNED INDIANS (CASTING): In every Type 3 image that shows people (faces, hands, wrists, necks, or any visible skin), cast **fair-skinned Indian** subjects only — light wheatish to fair North Indian / urban Indian complexion. Explicitly state this in the prompt. Do **not** use deep brown, dark, or heavily tanned skin. Add to negatives: `dark skin, deep brown skin, heavily tanned skin`. Flatlay with no people is exempt.

2. PROPORTIONAL SCALE: Always add "The [product] must be rendered at its actual natural scale. Maintain exact proportions relative to [body part], avoid oversized/exaggerated rendering."

3. SINGLE PRODUCT: Always add "This [product] is the single and only piece of jewelry in the entire image. [Others] wear absolutely no other jewelry." + add "extra necklaces, extra rings, extra bracelets" to negative prompt.

4. NO OVERLAYS: Always add "There are absolutely no floating overlays, no cutout drawings, no giant product diagrams anywhere in the image." + add "floating overlays, graphic drawings, cutouts, product diagrams, split screen" to negative prompt.

5. MULTI-ANGLE REFS: Import 4-5 different angles via `media_import_url`. Never just 1 reference.

6. @img1 @img2 IN PROMPT: Must reference images in prompt text matching the medias array order.

7. MCP MEDIA IDS: Never pass raw `https://` URLs into `medias[].value`. Always import first; use role **`image`** (not `image_reference`).

8. MANGALSUTRA ONLY: Add "The AI must replicate the exact metal, exact number of bead stations (if any), their exact colors/count, and precise spacing. No extra black beads added if not visible in references."

---

## Output Location

```
output/magnific_generated/
  {occasion}-hero-2026.webp      → WordPress Featured Image
  {occasion}-flatlay-2026.webp   → Body block at H2 #2
  {occasion}-lifestyle-2026.webp → Body block at H2 #4
```

(Legacy folder name kept so existing patch scripts keep working.)

---

## WordPress Upload (patch script)

Run: `python3 scripts/patch_{occasion}_type3_clean.py`

The script:
1. Fetches live post raw content (GET /wp-json/wp/v2/posts/{id}?context=edit)
2. Strips ALL existing wp:image blocks (prevents duplicates)
3. Strips old schema blocks
4. Uploads each WebP to WP Media Library (POST /wp-json/wp/v2/media)
5. Sets hero as featured_media
6. Injects flatlay before H2 #2, lifestyle before H2 #4
7. Appends FAQ + BlogPosting JSON-LD schema
8. Pushes content update (POST /wp-json/wp/v2/posts/{id})
9. Validates exactly 2 image blocks before pushing

WP_APP_PASSWORD must belong to an Editor or Administrator role account.
