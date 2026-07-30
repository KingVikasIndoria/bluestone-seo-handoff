# Type 3 visual guide — Higgsfield lifestyle images

Use **Higgsfield MCP** (`nano_banana_pro`) for Type 3 concept images: **hero** (featured), **flatlay**, **lifestyle**.  
Type 2 carousel images come from `ProductImages/seo images/` — no AI generation.

**Provider note:** Magnific API is retired for this workflow (no API key / credits). Do not use `MAGNIFIC_API_KEY` or `scripts/magnific_generate_images.py` for new articles.

**Reference articles (approved process):** Rank 16–18 (Valentine’s hubby, Republic Day, Men’s Day) via Higgsfield MCP.

---

## Model

| Setting | Value |
|---|---|
| Provider | **Higgsfield MCP** (`project-0-Geo and Seo-higgsfield` / `https://mcp.higgsfield.ai/mcp`) |
| Tool | `generate_image` |
| Model | `nano_banana_pro` |
| Aspect | `16:9` |
| Resolution | `2k` |
| Count | `1` per slot |
| Credits | Higgsfield **web/MCP** wallet (check with MCP `balance`) — not Cloud API keys |
| Auth | Cursor MCP connection (no `MAGNIFIC_API_KEY`) |

**Reference media flow (required):**

1. `media_import_url` each BlueStone CDN product PNG (`type: "image"`)
2. Pass returned `media_id` in `params.medias[].value`
3. Use role **`image`** (not `image_reference`)
4. Never pass raw `https://` URLs inside `medias[].value`

---

## How to generate (full pipeline)

### When

Generate Type 3 **last** — after article text, carousel, and WP publish/draft.

### Steps

```
1. Finish article + Type 2 SEO carousel
2. Publish / save WP draft
3. Read raw / CDN angles for Type 3 SKUs — note exact materials
4. Write output/Week1_Rank{N}_{Topic}_type3_prompts.json
5. Import CDN refs via Higgsfield media_import_url
6. Generate 3 images via generate_image (nano_banana_pro)
7. Download PNG → resize ~1400px wide → WebP quality ~82
8. Upload + patch featured + in-body images on live post
9. Hygiene check
```

### MCP tools (per slot)

```
balance                          # optional credit check
media_import_url                 # once per CDN angle URL
generate_image                   # submit job
job_status (sync: true)          # poll until completed (text-only clients)
```

### Post-process (local)

```bash
# Download completed PNG URL from job_status → WebP
# Save under output/magnific_generated/ (legacy folder name kept)
#   {occasion}-hero-YYYY.webp
#   {occasion}-flatlay-YYYY.webp
#   {occasion}-lifestyle-YYYY.webp

python3 scripts/patch_{occasion}_type3_clean.py
```

---

## Prompt manifest

File: `output/Week1_Rank{N}_{Topic}_type3_prompts.json`

Recommended fields:

- **`workflow`:** `Higgsfield MCP nano_banana_pro with CDN product reference medias.`
- **`higgsfield.model`:** `nano_banana_pro`
- **`higgsfield.theme_anchor`:** hyper-real block (locked across all 3 slots)
- **`higgsfield.negative_prompt`:** appended in prompt as `Avoid: ...`
- **`slots.*.reference_images`:** 3–5 public CDN angle URLs (import before generate)
- **`slots.*.prompt`:** scene + accurate SKU description + @img1… refs + casting block
- **`slots.*.alt`:** unique alt with occasion year
- **`output`:** local WebP paths

Legacy manifests may still use a `magnific` key — treat that block as theme/negative/model config only; generation is always Higgsfield MCP.

---

## How approved Higgsfield images are generated

### 1. Read product angles first

Open CDN / raw product images and describe **exactly** what you see (metal, link style, stones, scale). Wrong descriptions produce wrong AI output.

### 2. Import references

For each URL in `slots.*.reference_images`:

```
media_import_url({ url: "<cdn png>", type: "image" }) → media_id
```

### 3. Generate

**Order matters.** For people/hero/lifestyle, assemble **scene first**, jewellery second. Do **not** lead with commercial/macro jewellery language (that triggers floating packshot overlays).

```
# PEOPLE slots (hero / lifestyle with skin):
full_prompt = people_theme_anchor + " " + casting_block + " " + people_scene_first + " " + worn_jewellery_block + " Avoid: " + negative_prompt_people

# FLATLAY (no people):
full_prompt = product_theme_anchor + " " + flatlay_slot_prompt + " Avoid: " + negative_prompt
```

**People refs:** import **2 only** (best front + 3/4). More packshot refs increase overlay/collage hallucination.  
**Flatlay refs:** 3–4 angles OK.

Call:

```json
{
  "params": {
    "model": "nano_banana_pro",
    "aspect_ratio": "16:9",
    "resolution": "2k",
    "count": 1,
    "prompt": "<full_prompt>",
    "medias": [
      { "value": "<media_id_1>", "role": "image" },
      { "value": "<media_id_2>", "role": "image" }
    ]
  }
}
```

**Credits / production default:** generate **exactly 3 images per article** (1 hero + 1 flatlay + 1 lifestyle), `count: 1` each. Aim for a first-pass pass using the people-first formula. **Retry a slot only if QA fails** (overlay, wrong scale, extra jewellery, bad casting) — do not generate dual variants by default.

### 4. Post-processing

- Download PNG from job result URL
- Resize to ~1400px wide (keep 16:9)
- Save WebP quality ~82
- Prompt for safe margins so faces/jewellery are not cropped

### 5. WordPress patch

`scripts/patch_{occasion}_type3_clean.py` uploads 3 WebPs, sets featured = hero, replaces in-body `wp:image` blocks, updates schema images/alts.

---

## Prompt Formula

### A) People slots (hero / lifestyle) — SCENE FIRST

Nano Banana often **hallucinates a giant floating packshot** when the prompt leads with “commercial jewellery / macro” and too many product refs — even if you write “no overlays”. Fix: people scene first, worn jewellery second, **2 refs max**.

```
{PEOPLE_THEME_ANCHOR}

{CASTING_BLOCK}

{OCCASION} candid lifestyle photograph, mid-shot of people (not a product ad).
{SCENE with SUBJECTS}. Faces and upper bodies fill most of the frame.
{SUBJECT matching GenderTag} is physically wearing the {product} from reference images (@img1 body_image worn scale, @img2 design only) {ON body part}.
GENDER LOCK: GenderTag from `Seo Products - consolidated.csv` — Male→adult man only; Female→adult woman only; Kids→child only; Unisex→one clear adult wearer. Never put a Male SKU on a woman or Female SKU on a man.
The {product} rests on skin/fabric with a soft contact shadow at EXACT PDP size from the CSV:
height_mm={H} × width_mm={W} (use size_prompt_note: face dims vs bracelet length axis).
BODY_IMAGE SCALE LINE (required): Keep the jewellery size on the person like @img1 body_image (worn ear/neck/wrist/finger scale). Use @img2 only for the jewellery design. Do not make it bigger for visibility.
Jewellery fidelity (campaign hybrid): HD hyperreal metal and stones, 100% identical to refs, zero distortion, exact design and proportions. Controlled soft key light with gentle realistic shadows; proper shallow depth of field. People stay candid; jewellery reads high-end commercial quality without becoming a packshot overlay.
Camera focuses on the people; jewellery is sharp and true but NOT the largest object in the image.
Design fidelity to refs: {DESIGN_DETAILS}. Zero distortion. Size and design must remain 100% identical to the product references.
This is the ONLY jewellery in the image. Bare ears and bare wrists otherwise.
CRITICAL anti-collage: the jewellery is attached to the body, never a floating cutout,
never a giant product diagram composited over the photo, never a packshot overlay.
16:9 landscape, full faces in frame, safe margins.
Avoid: {NEGATIVE_PROMPT_PEOPLE}
```

### B) Flatlay (no people) — product language OK

```
{PRODUCT_THEME_ANCHOR}

{OCCASION} top-down flatlay. Flatlay setting ID: {FLATLAY_SETTING_ID}.
Surface + props: {FLATLAY_SETTING_PROMPT}.
The identical {product} from (@img1, @img2, @img3) rests on the surface at EXACT PDP size (height_mm × width_mm from consolidated CSV), HD hyperreal fidelity, zero distortion, 100% identical design, sharp, full piece visible, centered as hero of the still life but true-to-life scale (do not enlarge for visibility). Controlled soft key + gentle shadows, shallow depth of field, no blown whites.
Props stay secondary; jewellery is the clear subject. No people, no hands.
No floating overlays or cutouts. No readable text, logos, or brand marks on props.
Avoid: {NEGATIVE_PROMPT}
```

### Flatlay setting rotation (mandatory)

Do **not** default every article to warm wood + kraft box + linen. Pick one setting per article from the menu below. Track last settings in `output/product_rotation.json` → `recent_flatlay_settings` and **avoid repeating the same ID on consecutive ranks**.

| Setting ID | Surface | Prop kit (2–4 items, blank/no text) | Best for |
|---|---|---|---|
| `desk-kraft` | warm wood desk | kraft gift box, blank cream card, linen napkin | formal / principal / teachers / default |
| `marble-vanity` | soft marble or stone vanity | blank perfume silhouette (no label), silk ribbon, tiny tray | romantic / her gifts / crush |
| `linen-bedside` | rumpled linen + nightstand edge | closed book (no title), soft lamp glow, dried flower | birthday / evening / soft personal |
| `cafe-tray` | ceramic tray / stoneware | plain espresso cup + saucer, napkin | friendship / status / casual |
| `festive-mantel` | wood shelf or mantel | pine sprig or diya (no logos), blank gift tag | Diwali / Christmas / festive |
| `windowsill-daylight` | painted windowsill | sheer curtain blur, small plant pot, blank envelope | soft daylight editorial |
| `gift-wrapping-station` | kraft paper roll surface (blank) | matte scissors, twine, blank tag | gifting CTA articles |
| `study-desk` | dark wood / matte study desk | closed notebook (no title), plain pen, soft blotter | principal / teachers / academic |

**Occasion defaults (override if last article used the same ID):**
- Principal / teachers / academic → `study-desk` or `desk-kraft`
- Christmas / Diwali / festive → `festive-mantel`
- Birthday / status / friendship → `linen-bedside` or `cafe-tray`
- Romantic / her gifts → `marble-vanity`
- Soft editorial filler → `windowsill-daylight`
- Strong gift CTA → `gift-wrapping-station`

In each Type 3 prompts JSON, set `"flatlay_setting": "<setting_id>"` and write the matching surface/props into the flatlay prompt.

---

## The 3 Slots

| Slot | Scene | Subject | Product Placement | Refs | Lens |
|---|---|---|---|---|---|
| hero | Warm lifestyle with people | Hug / gift / celebration | **Worn** on body, small in frame | **2** (body_image + design) | 85mm mid-shot |
| flatlay | Rotating setting from menu | No people — props only | On surface, center frame, true scale | 3–4 | 100mm top-down |
| lifestyle | Action close-up | Wrist / hand / ear in motion | On wrist / in hand / on ear | **2** (body_image + design) | 85mm mid-shot |

---

## Hyper-real prompt system (campaign hybrid)

Use **different theme anchors** for people vs flatlay. Only change scene/pose per slot.

**Campaign hybrid (locked from 2026-07-20):** people stay **candid lifestyle**; jewellery upgrades to **HD hyperreal commercial fidelity** (exact size/design, no distortion). Controlled soft key + gentle shadows + proper shallow DoF. Ban blown whites / HDR glare. Keep GenderTag + exact mm rules. Do **not** lead people prompts with macro packshot language (that still triggers floating overlays).

### People Theme Anchor (hero + lifestyle with skin)

```
Photoreal candid lifestyle photograph with high-end jewellery commercial fidelity on the worn piece only. Natural skin texture, no illustration, no CGI. Controlled soft key light with gentle fill, realistic soft shadows, proper shallow depth of field (85mm), balanced exposure with no blown whites and no HDR glare. Shot on DSLR, HD quality, 16:9 full frame with safe margins. People are the primary subject and remain candid; the jewellery is a small worn detail that is 100% identical to product refs (exact size, exact design, zero distortion, HD metal and stone detail). Entire faces and worn jewellery fully visible, nothing cropped at frame edges.
```

### Product Theme Anchor (flatlay only)

```
Photoreal high-end jewellery commercial flatlay, HD quality, no distortion of jewellery, identical scale and design (100% match to refs), physically accurate metal and stone detail, natural textures only, no stylization, no illustration. Controlled soft key light with gentle realistic shadows, proper shallow depth of field, balanced exposure with no blown whites and no HDR glare. Shot on DSLR, 16:9 full frame with safe margins. Entire jewellery fully visible, nothing cropped at frame edges.
```

### Standard Negative Prompt — people (append as `Avoid: ...`)

```
floating jewellery overlay, giant pendant collage, product cutout over people, packshot composited on lifestyle photo, oversized necklace covering torso, oversized earrings, statement earrings, fashion runway proportions, exaggerated hoop diameter, jewellery upscaled for visibility, graphic drawings, cutouts, product diagrams, split screen, illustration, CGI look, cartoon, fake diamonds, studio HDR glow, blown whites, overexposed highlights, washed-out lighting, unreal scale, oversized jewellery, distorted jewellery, warped metal, melted stones, wrong design, distorted hands, extra fingers, extra bracelets, extra rings, extra earrings, product shot on plain background, cropped faces, cut-off heads, readable text, logos, dark skin, deep brown skin, heavily tanned skin
```

### Standard Negative Prompt — flatlay

```
illustration, CGI look, cartoon, fantasy style, over-stylized, plastic glass, fake diamonds, fake gemstones, artificial harsh lighting, studio HDR glow, blown whites, overexposed highlights, washed-out lighting, unreal reflections, blurry jewellery, distorted jewellery, warped metal, noise, low detail, AI artifacts, painting, digital art, unreal scale, oversized jewellery, floating overlays, cutouts, product diagrams, readable text, logos, exaggerated proportions
```

### Casting block (required for people slots)

```
Casting (required): fair-skinned Indian {SUBJECT} only. Light wheatish to fair North Indian / urban Indian complexion, clear fair skin tones. Do not use deep brown, dark, or heavily tanned skin. Subjects must look ethnically Indian with fair skin.
```

### Material language

Describe like a product photographer:

- Gold: `polished 18k gold with soft specular highlights, realistic reflection falloff`
- Diamonds: `true diamond brilliance, physically accurate facets`
- Gemstones: `natural stone texture, realistic light refraction`

### Jewellery visibility (always specify)

- **Where:** on wrist, on desk, on neck, on ear
- **Scale:** true-to-life worn scale from CSV mm + refs — **NOT** oversized, **NOT** statement, **NOT** upscaled for visibility
- **Earrings / hoops:** do not exaggerate hoop diameter; keep near earlobe; never jawline-length unless PDP mm truly supports it
- **Focus:** jewellery sharp (HD fidelity) even when small
- **Framing:** entire piece visible, safe margins, nothing cut off
- **Wear:** nested into fabric/skin with soft contact shadows (not floating)

### Body_image scale line (required on every people prompt)

Paste after exact mm. Prefer this short line (category-swap ear/neck/wrist/finger as needed):

```
Keep the jewellery size on the person like @img1 body_image (worn ear/neck/wrist/finger scale). Use @img2 only for the jewellery design. Do not make it bigger for visibility.
```

Earrings example:

```
Keep the earring size on the woman like @img1 body_image (worn ear scale). Use @img2 only for the earring design. Do not make it bigger for visibility.
```

---

## Product references — when / how

| Slot | Product refs | Why |
|---|---|---|
| **Hero / lifestyle (people)** | Import **exactly 2** medias (`role: image`): **(1) `@img1` = `1_body_portrait` / CDN `BP-PICS` body_image** + **(2) `@img2` = front/primary design**. Body_image is **mandatory** for both hero and lifestyle. If no body_image exists for the SKU, **skip that SKU** and pick another — never run people shots from packshots alone. |
| **Flatlay** | Import **3–4** CDN/raw angles as medias (front / side / close-up). Body portrait optional, not required. |
| **Carousel (Type 2)** | Never — use `ProductImages/seo images/` only | Separate pipeline |

Always read the product images even when writing text descriptions — use them for accurate materials + as MCP medias.

---

## Slot requirements

| Slot | Must show | Must NOT show |
|---|---|---|
| **Hero** (featured) | People + jewellery gifted/worn; warm home; occasion mood | Plain product on beige/dark surface |
| **Flatlay** | Lived-in **rotated setting** from flatlay menu + props; jewellery on surface at true scale | Empty catalog shot; same wood+kraft set every time |
| **Lifestyle** | People / hands in action; jewellery on body, sharp | Product flatlay only |

### Hard rules

- No logos, brand names, or readable text
- Phone screens: blank/dark only
- Indian context where relevant
- **Fair-skinned Indians only** in any people/hand/wrist/face shot (light wheatish to fair complexion). State explicitly in prompt; ban deep brown / dark / heavily tanned skin in negatives. Flatlay with no people is exempt.
- 16:9 landscape, full frame
- Never reuse featured image in body
- Carousel cards = SEO images only (never raw/CDN packshots)
- Canva style refs **optional** — not required

---

## Critical Rules (from Production — Non-Negotiable)

1. **FAIR-SKINNED INDIANS (CASTING):** In every Type 3 image that shows people (faces, hands, wrists, necks, or any visible skin), cast **fair-skinned Indian** subjects only — light wheatish to fair North Indian / urban Indian complexion. Explicitly state this in the prompt. Do **not** use deep brown, dark, or heavily tanned skin. Add to negatives: `dark skin, deep brown skin, heavily tanned skin`. Flatlay with no people is exempt.

2. **PROPORTIONAL SCALE (EXACT MM) + BODY_IMAGE LINE:** Before prompting, read `height_mm`, `width_mm`, and `size_prompt_note` from `Seo Products - consolidated.csv`. State exact millimetres. Always include the short body_image line: keep jewellery size on the person like `@img1` body_image (worn scale); use `@img2` only for design; do not make it bigger for visibility. Require HD hyperreal fidelity, 100% identical design, zero distortion. Campaign-hybrid lighting (soft key, gentle shadows, shallow DoF, no blown whites). Oversized jewellery vs body_image/CSV is a QA fail — regenerate.

2b. **GENDER TAG LOCK:** `GenderTag` on the consolidated CSV is mandatory for people shots. Male SKUs (including “For Him”) only on adult men; Female only on adult women; Kids only on children. Wrong-gender wear is a QA fail — regenerate.

3. **SINGLE PRODUCT:** Always add "This [product] is the single and only piece of jewelry in the entire image. [Others] wear absolutely no other jewelry." + add "extra necklaces, extra rings, extra bracelets" to negative prompt.

4. **NO OVERLAYS:** People prompts must say jewellery is **physically worn / on body** with contact shadow. Put anti-collage negatives **first** in Avoid list. Saying “no overlays” alone is not enough if the prompt leads with macro/commercial jewellery language.

5. **REFERENCE COUNT + BODY_IMAGE:** People hero/lifestyle = **2 refs max**. `@img1` = `1_body_portrait` / CDN `BP-PICS` body_image; `@img2` = front/primary design. Body_image is **required** for hero and lifestyle. If missing → **skip the SKU** (do not fall back to packshots). Prompt must use the short body_image scale line. Flatlay = 3–4 angles. Do **not** send 4–5 packshots into a people scene.

6. **@img1 @img2 IN PROMPT:** Must reference images in prompt text matching the medias array order (use `@img1, @img2` for people).

7. **MCP MEDIA IDS:** Never pass raw `https://` URLs into `medias[].value`. Always import first; use role **`image`** (not `image_reference`).

8. **MANGALSUTRA ONLY:** Add "The AI must replicate the exact metal, exact number of bead stations (if any), their exact colors/count, and precise spacing. No extra black beads added if not visible in references."

9. **FLATLAY SETTING ROTATION:** Every Type 3 flatlay must declare a `flatlay_setting` ID from the 8-setting menu. Log it in `output/product_rotation.json` → `recent_flatlay_settings`. Do not reuse the same setting on consecutive ranks. Never default every blog to warm wood + kraft box + linen.

---

## Hygiene checks

| Check | Pass |
|---|---|
| Lifestyle feel | People or lived-in scene |
| Flatlay setting | Setting ID from 8-menu; not same as previous rank; props secondary / no text |
| Jewellery worn (people) | On body — **not** floating cutout / collage |
| Scale | Exact CSV mm + short body_image line (`@img1` worn scale; `@img2` design only; do not enlarge for visibility) |
| Gender | Wearer matches GenderTag (Male/Female/Kids/Unisex) |
| Jewellery visible | Sharp HD fidelity, exact CSV scale, in frame; no blown metal highlights |
| Lighting | Soft key + gentle shadows, shallow DoF, no washed/HDR glare |
| SKU accuracy | 100% identical to product refs (chain, beads, charm colours); zero distortion |
| Casting | Fair-skinned Indians when people/skin visible |
| Single piece | No extra earrings/bangles/rings unless intended |
| Screen text | None readable |
| Aspect | 16:9, nothing cut off |
| Featured ≠ body | Hero not duplicated in content |

---

## Files & scripts

| File | Purpose |
|---|---|
| `output/_template/type3_prompts.json` | Copy per article |
| `output/Week1_Rank{N}_{Topic}_type3_prompts.json` | Article prompts manifest |
| `scripts/patch_{occasion}_type3_clean.py` | Upload + patch WP post |
| `ProductImages/raw/` + CDN angles | Type 3 reference / SKU description |
| `ProductImages/seo images/` | Type 2 carousel only |
| `output/magnific_generated/` | Output WebPs (legacy folder name) |
| `scripts/magnific_generate_images.py` | **Deprecated** — Magnific API only |

---

## After generation

1. Upload WebPs to WordPress (**set alt + media title at upload**, not later as an afterthought)
2. Set `featured_media` = hero ID
3. Insert flatlay + lifestyle as `wp:image` blocks with the same alts
4. Confirm alts match prompts JSON + Image SEO rules below
5. Refresh BlogPosting schema `image` array (hero + body WebPs at minimum)

### Image SEO (required for every festive article)

Do this for **Type 2 carousel** and **Type 3** hero/flatlay/lifestyle.

| Rule | Type 2 (carousel) | Type 3 (hero / flatlay / lifestyle) |
|---|---|---|
| **Format** | WebP ~960×535, quality ~82 | WebP ~1400px wide, 16:9, quality ~82 |
| **Filename** | `{product-slug}-carousel.webp` (lowercase, hyphens) | `{occasion}-{slot}-{year}.webp` e.g. `mothers-day-hero-2027-1.webp` |
| **Alt** | `{Primary KW or occasion + year} gift idea: {Exact Product Name}` | `{Primary KW + year} {slot/scene}, {product if shown}` — unique per image |
| **WP media title** | `{Product Name} carousel — {Occasion} {year}` | `{Primary KW phrase} {year} {Hero\|Flatlay\|Lifestyle}` |
| **Primary KW** | Occasion/KW in every carousel alt | Primary KW in **hero alt at minimum**; vary body alts (do not clone the same string) |
| **Year** | Locked festive year only | Locked festive year only (no 2021–2025 leftovers) |
| **Duplicates** | Never reuse the same file twice | Featured hero **must not** also appear as a body image |

**Also required**
- Upload via WP media API with `alt_text` + `title` in the same request when possible.
- Body `wp:image` `alt=` must match the media library alt.
- Carousel `<img alt="...">` must be KW-led (not bare product name only).
- BlogPosting schema `image` array includes hero + in-body Type 3 URLs (carousel optional).
- No generic alts (`image`, `photo`, `jewellery`, product code alone).

### Gutenberg-safe image block markup (required)

Use **`sizeSlug: "full"`** (and `size-full` on the figure) when the `src` is the original uploaded WebP URL. Canonical form:

```html
<!-- wp:image {"id":123,"sizeSlug":"full","linkDestination":"none"} -->
<figure class="wp-block-image size-full"><img src="https://blog.bluestone.com/wp-content/uploads/.../file.webp" alt="..." class="wp-image-123"/></figure>
<!-- /wp:image -->
```

Do **not** add `width`, `height`, `loading`, or `decoding` on the `<img>`, and do **not** use `sizeSlug: "large"` with the full upload URL. That mismatch makes the block editor show **“Block contains unexpected or invalid content.”**
