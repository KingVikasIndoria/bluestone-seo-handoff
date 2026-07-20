#!/usr/bin/env python3
"""Generate Type 3 images from article prompt manifest (raw jewellery + prompts)."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    p = argparse.ArgumentParser(description="Batch Type 3 from article prompts JSON")
    p.add_argument("--manifest", required=True, help="Path to type3_prompts.json")
    p.add_argument("--only", choices=["hero", "flatlay", "lifestyle"], help="Generate one slot")
    args = p.parse_args()

    manifest_path = Path(args.manifest)
    if not manifest_path.is_absolute():
        manifest_path = ROOT / manifest_path
    if not manifest_path.exists():
        sys.exit(f"Manifest not found: {manifest_path}")

    data = json.loads(manifest_path.read_text())
    mag = data.get("magnific", {})
    model = mag.get("model", "mystic")
    structure_strength = str(mag.get("structure_strength", 55))
    theme_anchor = mag.get("theme_anchor")
    negative_prompt = mag.get("negative_prompt")

    slots = data.get("slots", {})
    outputs = data.get("output", {})
    results = []

    for slot, cfg in slots.items():
        if args.only and slot != args.only:
            continue
        ref_key = "structure_reference" if "structure_reference" in cfg else "structure_ref"
        struct_raw = cfg.get(ref_key)
        if struct_raw is None:
            struct_path = None
        else:
            struct_path = ROOT / struct_raw
            if not struct_path.exists():
                sys.exit(f"Missing structure ref: {struct_path}")
        slot_structure_strength = str(cfg.get("structure_strength", structure_strength))
        out_path = Path(outputs.get(slot, f"output/magnific_generated/{data['occasion']}-{slot}.webp"))
        if not out_path.is_absolute():
            out_path = ROOT / out_path

        cmd = [
            sys.executable,
            str(ROOT / "scripts/magnific_generate_images.py"),
            "--model",
            model,
        ]
        if struct_path is not None:
            cmd.extend(
                [
                    "--structure-ref",
                    str(struct_path),
                    "--structure-strength",
                    slot_structure_strength,
                ]
            )
        ref_imgs = cfg.get("reference_images")
        if ref_imgs:
            cmd.append("--reference-images")
            for r in ref_imgs:
                if r.startswith("http://") or r.startswith("https://"):
                    cmd.append(r)
                else:
                    r_path = ROOT / r
                    if not r_path.exists():
                        sys.exit(f"Missing reference image: {r_path}")
                    cmd.append(str(r_path))
        cmd.extend(
            [
            "--prompt",
            cfg["prompt"],
            "--out",
            str(out_path),
            ]
        )
        slot_theme = cfg.get("theme_anchor", theme_anchor)
        slot_negative = cfg.get("negative_prompt", negative_prompt)
        if slot_theme:
            cmd.extend(["--theme-anchor", slot_theme])
        if slot_negative:
            cmd.extend(["--negative-prompt", slot_negative])
        style_ref = cfg.get("style_ref")
        if style_ref:
            style_path = Path(style_ref)
            if not style_path.is_absolute():
                style_path = manifest_path.parent / style_ref
            if style_path.exists():
                cmd.extend(
                    [
                        "--style-ref",
                        str(style_path),
                        "--style-adherence",
                        str(mag.get("style_adherence", 35)),
                    ]
                )
        print(f"Generating {slot}...")
        subprocess.run(cmd, cwd=str(ROOT), check=True)
        results.append({"slot": slot, "out": str(out_path), "prompt": cfg["prompt"]})

        # Archive prompts to central archive.json
        archive_path = ROOT / "output/magnific_prompts_archive.json"
        archive_data = []
        if archive_path.exists():
            try:
                archive_data = json.loads(archive_path.read_text())
            except Exception:
                pass
        from datetime import datetime
        archive_data.append({
            "timestamp": datetime.now().isoformat(),
            "manifest": manifest_path.name,
            "occasion": data.get("occasion"),
            "wp_post_id": data.get("wp_post_id"),
            "slot": slot,
            "prompt": cfg["prompt"],
            "theme_anchor": slot_theme,
            "negative_prompt": slot_negative,
            "output_path": str(out_path.relative_to(ROOT) if out_path.is_relative_to(ROOT) else out_path)
        })
        archive_path.write_text(json.dumps(archive_data, indent=2) + "\n")

    summary = manifest_path.with_name(manifest_path.stem + "_generation_results.json")
    summary.write_text(json.dumps(results, indent=2) + "\n")
    print(f"Done. {len(results)} image(s) → {summary}")


if __name__ == "__main__":
    main()
