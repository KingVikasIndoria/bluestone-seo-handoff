# ProductImages

## Three image types

| Type | What | Where | Use |
|---|---|---|---|
| **1. Raw** | kinclimg / studio, accurate jewellery | `raw/<DesignCategory>/` | Reference only when generating Type 2 or 3 with jewellery |
| **2. AI product** | Styled AI product of same SKU | `seo images/<category>/` | Carousel + Buy now (mid-article) |
| **3. AI concept** | Mood / festival / hero / lifestyle | Per-article generation | Featured + in-body atmosphere |

```
Article
├── Type 3 → mood / hero / lifestyle
└── Type 2 → mid-article carousel + Buy now
Type 1 → reference only (never carousel)
```

## Inventory
- Type 1: `raw/` — 74/74 from CSV `Image link`
- Type 2: `seo images/` — 74/74 SEO products
- Type 3: Holi has existing assets; **generation rules from Article 2 (Eid)**

## Rules
- Filename stem = exact Design Name from SEO products CSV
- No prices; PDP from CSV `Link`
- Never reuse the same image twice in one article
- Compress large Type 2 PNGs before WP upload (~1920 long edge, JPEG q85)
