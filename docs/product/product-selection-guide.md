# Approved SEO products — selection guide

**Canonical file (use this):** `Seo Products - consolidated.csv`  
Paths: pack root, `docs/product/`, and workspace root.

Sources merged:
- `Seo Products - final products (1).csv` — CDN image, price, category, PDP link
- `image-generation-handoff/designfiltered2026.csv` — **GenderTag**, **height_mm**, **width_mm**

**74 SKUs.** Keep the legacy CSV for download scripts if needed; for article + Type 3 work prefer **consolidated**.

| Column | Use |
|---|---|
| `Design Code` / `Design Name` | SKU identity; carousel alts / captions |
| `GenderTag` | `Female` / `Male` / `Kids` / `Unisex` — **who wears it in Type 3 people shots** |
| `height_mm` / `width_mm` | Exact PDP face (or length) for Type 3 scale prompts |
| `size_prompt_note` | How to phrase scale (face vs bracelet length) |
| `DesignCategory` | Occasion fit + `ProductImages/seo images/{Category}/` path |
| `Image link` / `Link` | CDN packshot + PDP (no prices in article body) |
| `seo_image_path_hint` | Expected SEO PNG path for Type 2 carousel |

## Gender casting (mandatory for Type 3 people)

| GenderTag | Wearer in hero / lifestyle |
|---|---|
| **Male** | Adult fair-skinned **Indian man** only (e.g. Serenity / Talisman For Him, For Him bracelets, men’s bands/chains) |
| **Female** | Adult fair-skinned **Indian woman** only |
| **Kids** | Fair-skinned Indian **child** (kids evil-eye bracelets) |
| **Unisex** | Either adult gender if occasion fits; still one clear wearer |

Never put a **Male**-tagged SKU on a woman (or Female on a man). Name cues like “For Him” must match `GenderTag`.

## Exact size in Type 3 prompts

1. Read `height_mm` + `width_mm` + `size_prompt_note` from consolidated CSV before writing prompts.
2. State exact mm in the prompt (e.g. `30.87 mm tall × 15.91 mm wide`).
3. Add a body-relative cue from `size_prompt_note`:
   - **Face pieces** (most pendants, rings, earrings): face height/width vs shirt button / finger / earlobe.
   - **Long bracelets / anklets / some chains:** one axis ≥ ~100 mm is usually **length**, not “giant height” — use the small axis as worn thickness/width.
4. Campaign hybrid: candid people + HD hyperreal jewellery fidelity (exact design, zero distortion); controlled soft key, gentle shadows, shallow DoF; no blown whites / HDR glare; never catalog-giant overlay. People refs: `@img1` body_image + `@img2` design. Short scale line: Keep the jewellery size on the person like @img1 body_image (worn scale). Use @img2 only for the jewellery design. Do not make it bigger for visibility.
5. **Flatlay setting rotation:** pick a setting ID from the 8-menu in `docs/HIGGSFIELD_IMAGE_GENERATION.md` and log it in `output/product_rotation.json` → `recent_flatlay_settings`. Do not repeat the same setting on consecutive ranks.
5. Missing width (Yfel necklace): estimate carefully from refs and say “natural necklace scale”; do not invent fake mm.

## Category counts
| DesignCategory | Count |
|---|---|
| Rings | 14 |
| Bracelets | 13 |
| Pendants | 13 |
| Earrings | 8 |
| Mangalsutra Chains | 7 |
| Bangles | 6 |
| Necklaces / Chains | 3 each |
| Kids / Adjustable / other | smaller |

Gender mix (consolidated): **Female 55 · Male 16 · Kids 2 · Unisex 1**.

## Wishes posts (default)
Pick **5–6 carousel SKUs** (Type 2) + **3 Type 3 SKUs** (hero / flatlay / lifestyle).  
Rotate categories; occasion fit wins. See `.cursor/rules/product-rotation-captions-education.mdc`.

Carousel and Type 3 overlap **at most 1 SKU** when the library allows.

## Occasion → category + gender map
| Occasion | Prefer | Gender note |
|---|---|---|
| Holi | Earrings, Pendants, Bracelets | Mostly Female |
| Diwali | Pendants, Earrings, Bangles, Chains | Female default; Male only for him-gifts |
| Rakhi | Adjustable / Kids / Evil Eye / For Him bracelets | Brother → **Male**; kids → **Kids** |
| Eid | Earrings, Pendants, Bangles | Female |
| Proposal / engagement | Rings, Pendants | Match recipient gender |
| Wedding / anniversary | Rings, Mangalsutra, Bangles, Necklaces | Mangalsutra → Female |
| Men’s / mama ji / him gifts | Bracelets / Rings / Pendants / Chains **For Him** | **Male** only |
| Newborn / kids | Kids Bracelets + protective evil-eye | **Kids** |
| Friendship / everyday | Pendants, Earrings, Charms | Usually Female; Unisex OK |

## Always cite in briefs
`Design Code | Design Name | GenderTag | height_mm × width_mm | DesignCategory | Link`  
(Do **not** put selling prices in published body copy.)
