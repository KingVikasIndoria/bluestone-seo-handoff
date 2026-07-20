#!/usr/bin/env python3
"""
Generate Type 3 concept images via Magnific API.

Usage:
  # Single image
  python3 scripts/magnific_generate_images.py \\
    --prompt "..." --out output/my-hero.webp --size landscape_16_9

  # Article preset (Diwali example)
  python3 scripts/magnific_generate_images.py --preset diwali-2026

  # Batch from JSON
  python3 scripts/magnific_generate_images.py --config output/article_images.json

Requires MAGNIFIC_API_KEY in .env or environment.
Docs: KnowledgeBase/Writing/MAGNIFIC_IMAGE_GENERATION.md
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API_BASE = "https://api.magnific.com"

MODELS = {
    "z-image": {
        "create": "/v1/ai/text-to-image/z-image",
        "status": "/v1/ai/text-to-image/z-image/{task_id}",
        "size_key": "image_size",
    },
    "mystic": {
        "create": "/v1/ai/mystic",
        "status": "/v1/ai/mystic/{task_id}",
        "size_key": "aspect_ratio",
    },
    "nano-banana-pro": {
        "create": "/v1/ai/text-to-image/nano-banana-pro",
        "status": "/v1/ai/text-to-image/nano-banana-pro/{task_id}",
        "size_key": "aspect_ratio",
    },
}

PRESETS = {
    "diwali-2026": [
        {
            "name": "diwali-hero-mood-2026",
            "model": "mystic",
            "structure_reference": "ProductImages/raw/Pendants/The Thyvarne Pendant.jpg",
            "prompt": (
                "Editorial hero for Happy Diwali 2026 blog. Warm golden evening still life: "
                "the exact gold diamond pendant from structure reference on a wooden tray with "
                "lit diyas, marigold garlands, soft bokeh fairy lights, amber and deep blue tones, "
                "photorealistic, no text, no logos, no people, 16:9 landscape, magazine quality"
            ),
            "filename": "diwali-hero-mood-2026.webp",
        },
        {
            "name": "diwali-flatlay-phone-2026",
            "model": "mystic",
            "structure_reference": "ProductImages/raw/Pendants/The Thyvarne Pendant.jpg",
            "prompt": (
                "Top-down flatlay for Diwali 2026 blog, widescreen horizontal layout. "
                "Left side: black smartphone with completely blank dark screen, no text, no letters. "
                "Right side: the exact gold diamond pendant from the structure reference on cream linen. "
                "Between them: small clay diya lamps and orange marigold petals. "
                "Photorealistic product photography, soft natural light, no logos, "
                "no readable text anywhere, 16:9 landscape"
            ),
            "filename": "diwali-flatlay-phone-2026.webp",
        },
        {
            "name": "diwali-lifestyle-family-2026",
            "model": "mystic",
            "structure_reference": "ProductImages/raw/Earrings/The Asya Huggie Earrings.jpg",
            "prompt": (
                "Lifestyle photo: Indian woman celebrating Diwali on a home balcony at night, "
                "wearing the exact diamond huggie earrings from structure reference, holding a diya, "
                "warm smile, traditional festive attire, soft golden light, photorealistic, "
                "respectful, no logos, no readable text, 16:9 landscape"
            ),
            "filename": "diwali-lifestyle-family-2026.webp",
        },
    ],
}


def load_env():
    env_path = ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip("'\""))


def api_key() -> str:
    load_env()
    key = os.environ.get("MAGNIFIC_API_KEY")
    if not key:
        sys.exit("MAGNIFIC_API_KEY not set. Add to .env or export in shell.")
    return key


def request_json(method: str, url: str, body: dict | None = None) -> dict:
    headers = {
        "Content-Type": "application/json",
        "x-magnific-api-key": api_key(),
        "User-Agent": "BluestoneSEO/1.0",
    }
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        msg = e.read().decode("utf-8", "replace")
        raise RuntimeError(f"HTTP {e.code} {url}: {msg}") from e


def encode_image_reference(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


MYSTIC_SIZES = {
    "landscape_16_9": "widescreen_16_9",
    "16:9": "widescreen_16_9",
    "widescreen_16_9": "widescreen_16_9",
}


def create_task(
    model: str,
    prompt: str,
    size: str,
    structure_ref: Path | str | None = None,
    style_ref: Path | str | None = None,
    structure_strength: int = 50,
    style_adherence: int = 35,
    reference_images: list[Path | str] | None = None,
) -> str:
    cfg = MODELS[model]
    body: dict = {"prompt": prompt}
    if model == "z-image":
        body["image_size"] = size
        body["output_format"] = "png"
        if structure_ref or style_ref:
            print("  WARNING: z-image ignores structure/style refs; use --model mystic")
    else:
        if model == "nano-banana-pro":
            body["aspect_ratio"] = "16:9"
            body["resolution"] = "2K"
            # nano-banana-pro supports reference_images array
            if not reference_images and structure_ref:
                reference_images = [structure_ref]
            if reference_images:
                body["reference_images"] = []
                for p in reference_images:
                    if not p:
                        continue
                    if isinstance(p, str) and (p.startswith("http://") or p.startswith("https://")):
                        mime_type = "image/png"
                        if p.lower().endswith((".jpg", ".jpeg")):
                            mime_type = "image/jpeg"
                        elif p.lower().endswith(".webp"):
                            mime_type = "image/webp"
                        body["reference_images"].append({
                            "image": p,
                            "mime_type": mime_type
                        })
                    else:
                        from pathlib import Path as LPath
                        p_path = LPath(p) if isinstance(p, str) else p
                        if p_path.exists():
                            b64_data = base64.b64encode(p_path.read_bytes()).decode("ascii")
                            mime_type = "image/png"
                            if p_path.suffix.lower() in [".jpg", ".jpeg"]:
                                mime_type = "image/jpeg"
                            elif p_path.suffix.lower() == ".webp":
                                mime_type = "image/webp"
                            body["reference_images"].append({
                                "image": f"data:{mime_type};base64,{b64_data}",
                                "mime_type": mime_type
                            })
        else:
            body["aspect_ratio"] = MYSTIC_SIZES.get(size, "widescreen_16_9")
            body["model"] = "realism"
            if structure_ref and structure_ref.exists():
                body["structure_reference"] = encode_image_reference(structure_ref)
                body["structure_strength"] = structure_strength
            if style_ref and style_ref.exists():
                body["style_reference"] = encode_image_reference(style_ref)
                body["adherence"] = style_adherence

    resp = request_json("POST", API_BASE + cfg["create"], body)
    return resp["data"]["task_id"]


def poll_task(model: str, task_id: str, timeout_sec: int = 180) -> list[str]:
    cfg = MODELS[model]
    url = API_BASE + cfg["status"].format(task_id=task_id)
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        resp = request_json("GET", url)
        data = resp["data"]
        status = data["status"]
        if status == "COMPLETED":
            urls = data.get("generated") or []
            if not urls:
                raise RuntimeError(f"Task {task_id} completed but no images returned")
            return urls
        if status == "FAILED":
            raise RuntimeError(f"Task {task_id} failed: {json.dumps(data)}")
        time.sleep(3)
    raise TimeoutError(f"Task {task_id} timed out after {timeout_sec}s")


def download_url(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "BluestoneSEO/1.0"})
    with urllib.request.urlopen(req, timeout=120) as r:
        dest.write_bytes(r.read())


def crop_landscape_16_9(im, target_width: int = 1400):
    from PIL import Image

    w, h = im.size
    if w / h > 16 / 9 + 0.01:
        new_w = int(h * 16 / 9)
        x0 = (w - new_w) // 2
        im = im.crop((x0, 0, x0 + new_w, h))
    elif w / h < 16 / 9 - 0.01:
        new_h = int(w * 9 / 16)
        y0 = (h - new_h) // 2
        im = im.crop((0, y0, w, y0 + new_h))
    if im.width != target_width:
        ratio = target_width / im.width
        im = im.resize((target_width, int(im.height * ratio)), Image.Resampling.LANCZOS)
    return im


def compose_prompt(prompt: str, negative_prompt: str | None = None, theme_anchor: str | None = None) -> str:
    parts = []
    if theme_anchor:
        parts.append(theme_anchor.strip())
    parts.append(prompt.strip())
    if negative_prompt:
        parts.append(f"Avoid: {negative_prompt.strip()}")
    return " ".join(parts)


def to_webp(png_path: Path, webp_path: Path, max_width: int = 1400, force_landscape: bool = False) -> tuple[int, int]:
    from PIL import Image

    im = Image.open(png_path).convert("RGB")
    if force_landscape:
        im = crop_landscape_16_9(im, max_width)
    elif im.width > max_width:
        ratio = max_width / im.width
        im = im.resize((max_width, int(im.height * ratio)), Image.Resampling.LANCZOS)
    webp_path.parent.mkdir(parents=True, exist_ok=True)
    im.save(webp_path, "WEBP", quality=82, method=6)
    return im.size


def generate_one(
    prompt: str,
    out_path: Path,
    model: str = "z-image",
    size: str = "landscape_16_9",
    structure_ref: Path | str | None = None,
    style_ref: Path | str | None = None,
    structure_strength: int = 50,
    style_adherence: int = 35,
    negative_prompt: str | None = None,
    theme_anchor: str | None = None,
    reference_images: list[Path | str] | None = None,
) -> Path:
    full_prompt = compose_prompt(prompt, negative_prompt=negative_prompt, theme_anchor=theme_anchor)
    refs = []
    if style_ref:
        if isinstance(style_ref, str):
            refs.append(f"style={style_ref.split('/')[-1]}")
        elif style_ref.exists():
            refs.append(f"style={style_ref.name}")
    if structure_ref:
        if isinstance(structure_ref, str):
            refs.append(f"structure={structure_ref.split('/')[-1]}")
        elif structure_ref.exists():
            refs.append(f"structure={structure_ref.name}")
    if reference_images:
        for r in reference_images:
            if isinstance(r, str) and (r.startswith("http://") or r.startswith("https://")):
                refs.append(f"ref={r.split('/')[-1]}")
            else:
                from pathlib import Path as LPath
                r_path = LPath(r) if isinstance(r, str) else r
                if r_path.exists():
                    refs.append(f"ref={r_path.name}")
    ref_note = f" ({', '.join(refs)})" if refs else ""
    print(f"Generating ({model}): {out_path.name}{ref_note}")
    task_id = create_task(
        model,
        full_prompt,
        size,
        structure_ref=structure_ref,
        style_ref=style_ref,
        structure_strength=structure_strength,
        style_adherence=style_adherence,
        reference_images=reference_images,
    )
    print(f"  task_id={task_id}")
    urls = poll_task(model, task_id)
    png_tmp = out_path.with_suffix(".png")
    download_url(urls[0], png_tmp)
    w, h = to_webp(png_tmp, out_path, force_landscape=(model == "mystic"))
    png_tmp.unlink(missing_ok=True)
    print(f"  saved {out_path} ({w}x{h}, {out_path.stat().st_size // 1024} KB)")
    return out_path


def hygiene_check_image(path: Path) -> list[str]:
    """Basic Type 3 hygiene checks before WP upload."""
    issues: list[str] = []
    try:
        from PIL import Image
        import io

        im = Image.open(path).convert("RGB")
        w, h = im.size
        if w < 800 or h < 450:
            issues.append(f"Resolution low: {w}x{h} (expect >= 800x450)")
        if im.getextrema()[0] == im.getextrema()[1] == (0, 0):
            issues.append("Image appears fully black")
    except Exception as e:
        issues.append(f"Could not open image: {e}")
        return issues

    # OCR on center crop (phone-screen zone in flatlays)
    try:
        import pytesseract
        from PIL import Image

        im = Image.open(path).convert("RGB")
        w, h = im.size
        crop = im.crop((int(w * 0.25), int(h * 0.1), int(w * 0.75), int(h * 0.9)))
        text = pytesseract.image_to_string(crop).strip()
        if len(text) >= 4:
            cleaned = "".join(ch for ch in text if ch.isalnum() or ch.isspace())
            if len(cleaned.replace(" ", "")) >= 4:
                issues.append(f"Readable text detected in center crop: {text[:80]!r}")
    except ImportError:
        pass
    except Exception as e:
        issues.append(f"OCR check skipped: {e}")

    return issues


def resolve_ref(path_str: str | None) -> Path | str | None:
    if not path_str:
        return None
    if path_str.startswith("http://") or path_str.startswith("https://"):
        return path_str
    p = Path(path_str)
    if not p.is_absolute():
        p = ROOT / p
    return p


def run_preset(name: str, out_dir: Path, model: str, only: str | None = None) -> list[dict]:
    if name not in PRESETS:
        sys.exit(f"Unknown preset: {name}. Available: {', '.join(PRESETS)}")
    out_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for item in PRESETS[name]:
        if only and item["name"] != only:
            continue
        out = out_dir / item["filename"]
        struct_path = resolve_ref(item.get("structure_reference"))
        style_path = resolve_ref(item.get("style_reference"))
        item_model = item.get("model", model)
        generate_one(
            item["prompt"],
            out,
            model=item_model,
            structure_ref=struct_path,
            style_ref=style_path,
            structure_strength=item.get("structure_strength", 50),
            style_adherence=item.get("style_adherence", 35),
            negative_prompt=item.get("negative_prompt"),
            theme_anchor=item.get("theme_anchor"),
        )
        issues = hygiene_check_image(out)
        if issues:
            print("  HYGIENE WARNINGS:")
            for issue in issues:
                print(f"    - {issue}")
        results.append(
            {
                "name": item["name"],
                "path": str(out),
                "prompt": item["prompt"],
                "structure_reference": item.get("structure_reference"),
                "style_reference": item.get("style_reference"),
                "hygiene": issues,
            }
        )
    manifest = out_dir / "magnific_manifest.json"
    manifest.write_text(json.dumps(results, indent=2))
    print(f"Manifest: {manifest}")
    return results


def run_config(config_path: Path, model: str) -> None:
    items = json.loads(config_path.read_text())
    for item in items:
        out = Path(item["out"])
        if not out.is_absolute():
            out = ROOT / out
        
        ref_imgs = None
        if "reference_images" in item:
            ref_imgs = [resolve_ref(r) for r in item["reference_images"] if r]

        generate_one(
            item["prompt"],
            out,
            model=item.get("model", model),
            size=item.get("size", "landscape_16_9"),
            structure_ref=resolve_ref(item.get("structure_reference")),
            style_ref=resolve_ref(item.get("style_reference")),
            structure_strength=item.get("structure_strength", 50),
            style_adherence=item.get("style_adherence", 35),
            negative_prompt=item.get("negative_prompt"),
            theme_anchor=item.get("theme_anchor"),
            reference_images=ref_imgs,
        )


def main():
    p = argparse.ArgumentParser(description="Generate Type 3 images via Magnific API")
    p.add_argument("--prompt", help="Text prompt")
    p.add_argument("--out", help="Output .webp path")
    p.add_argument("--model", default="z-image", choices=list(MODELS))
    p.add_argument("--size", default="landscape_16_9", help="z-image: landscape_16_9; mystic: 16:9")
    p.add_argument("--structure-ref", help="Type 1 raw JPG/PNG for Mystic structure_reference (jewellery SKU)")
    p.add_argument("--style-ref", help="Canva style ref JPG/PNG for Mystic style_reference (mood/layout)")
    p.add_argument("--structure-strength", type=int, default=50, help="Mystic structure_strength 0-100")
    p.add_argument("--style-adherence", type=int, default=35, help="Mystic adherence when style_ref set (lower=more style transfer)")
    p.add_argument("--negative-prompt", help="Appended as 'Avoid: ...' (Magnific has no separate negative field)")
    p.add_argument("--theme-anchor", help="Fixed campaign anchor prepended to prompt")
    p.add_argument("--preset", help=f"Preset batch: {', '.join(PRESETS)}")
    p.add_argument("--only", help="Generate single item from preset by name")
    p.add_argument("--out-dir", default="output/magnific_generated", help="Output dir for presets")
    p.add_argument("--reference-images", nargs="*", help="List of reference images for Nano Banana Pro (Gemini 3)")
    p.add_argument("--config", help="JSON list of {prompt,out,...}")
    args = p.parse_args()

    if args.preset:
        run_preset(args.preset, ROOT / args.out_dir, args.model, only=args.only)
        return
    if args.config:
        run_config(Path(args.config), args.model)
        return
    if not args.prompt or not args.out:
        p.error("Provide --prompt and --out, or --preset, or --config")

    out = Path(args.out)
    if not out.is_absolute():
        out = ROOT / out
    ref = resolve_ref(args.structure_ref)
    style = resolve_ref(args.style_ref)
    ref_imgs = None
    if args.reference_images:
        ref_imgs = [resolve_ref(r) for r in args.reference_images if r]
    generate_one(
        args.prompt,
        out,
        model=args.model,
        size=args.size,
        structure_ref=ref,
        style_ref=style,
        structure_strength=args.structure_strength,
        style_adherence=args.style_adherence,
        negative_prompt=args.negative_prompt,
        theme_anchor=args.theme_anchor,
        reference_images=ref_imgs,
    )


if __name__ == "__main__":
    main()
