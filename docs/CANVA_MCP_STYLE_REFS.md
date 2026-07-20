# Canva MCP → optional style refs for Type 3

Use **Canva** (optional) for festive **mood/composition** refs. Final photoreal Type 3 images are generated with **Higgsfield MCP** (`HIGGSFIELD_IMAGE_GENERATION.md`) using BlueStone CDN product angles.

## 1. Connect Canva MCP (one-time)

Project config: `.cursor/mcp.json`

```json
{
  "mcpServers": {
    "canva": {
      "command": "npx",
      "args": ["-y", "mcp-remote@latest", "https://mcp.canva.com/mcp"]
    }
  }
}
```

1. **Restart Cursor** (required after adding MCP).
2. Open **Cursor Settings → MCP** and confirm `canva` appears.
3. On first Canva tool use, complete **OAuth in browser** (your Canva account).
4. Requires a Canva account (Pro helps for some export features).

Docs: https://www.canva.dev/docs/mcp/

## 2. Fetch style references (per article)

In Agent chat, after MCP is connected:

```
Search Canva templates for "[occasion] india festive" (e.g. children's day, republic day).
Pick 3 templates:
  - hero mood (wide, props/colors, minimal text)
  - flatlay layout (top-down composition)
  - lifestyle (people/celebration scene)
Export each as PNG/JPG to output/style_refs/[occasion-slug]/
Name: hero-style.jpg, flatlay-style.jpg, lifestyle-style.jpg
Do NOT use templates with large readable headline text — mood only.
```

Or manually: search on canva.com/templates, export thumbnails to `output/style_refs/<occasion>/`.

## 3. Build manifest

Copy `output/style_refs/_template/manifest.json` or run:

```bash
python3 scripts/canva_style_refs.py init --occasion childrens-day-2026 \
  --query "children's day india celebration"
```

Edit `structure_ref` per slot to match article product shortlist from CSV.

## 4. Generate Type 3 (Higgsfield MCP)

Follow `HIGGSFIELD_IMAGE_GENERATION.md`:

1. Import CDN product angles with Higgsfield `media_import_url`
2. `generate_image` with `nano_banana_pro`, 16:9, 2k, medias role `image`
3. Download → WebP → `scripts/patch_{occasion}_type3_clean.py`

Canva exports are optional mood cues in the written prompt — not required.

## 5. Hygiene before WP upload

See `HIGGSFIELD_IMAGE_GENERATION.md`:

- No readable text on phones/banners
- Jewellery matches structure ref SKU
- 16:9 landscape
- Style ref = layout/colors only (not copy Canva headlines into output)

## Reference roles

| Ref | Source | Magnific param | Controls |
|---|---|---|---|
| Style (optional) | Canva template export | Prompt mood only / optional ref | Colors, layout, festive props |
| Structure | BlueStone CDN product angles | Higgsfield `media_import_url` → medias role `image` | Exact jewellery shape/SKU |
| Prompt | Written | `generate_image` prompt | Photorealistic, hygiene rules, occasion |

## Troubleshooting

| Issue | Fix |
|---|---|
| Canva MCP not in tool list | Restart Cursor; check `.cursor/mcp.json` |
| OAuth fails | Re-auth in MCP settings; check Canva plan |
| Output looks like illustration | Lower `--style-adherence` (25–35); add "photorealistic photograph" to prompt |
| Wrong jewellery | Raise `--structure-strength` (50–65); verify raw JPG path |
| Gibberish phone text | Blank screen in prompt; never ask for message text on screen |
