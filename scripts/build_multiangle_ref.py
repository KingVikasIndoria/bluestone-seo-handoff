#!/usr/bin/env python3
"""
Build a multi-angle composite reference sheet for a product from google_product_feed.csv.

Given a product title, this script:
1. Finds the product in google_product_feed.csv
2. Downloads all angle images from image_link + additional_image_link
3. Creates a single composite contact sheet (grid) with all angles
4. Saves it as a PNG ready to be used as structure_reference
"""
from __future__ import annotations

import csv
import io
import os
import sys
import urllib.request
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
FEED_CSV = ROOT / "google_product_feed.csv"
OUTPUT_DIR = ROOT / "output" / "product_references"


def find_product(title_query: str) -> dict | None:
    """Find a product row in the CSV by partial title match."""
    title_query_lower = title_query.lower().strip()
    with open(FEED_CSV, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if title_query_lower in row.get("title", "").lower():
                return row
    return None


def get_all_image_urls(row: dict) -> list[str]:
    """Extract all unique image URLs from a product row."""
    urls = []
    
    # Primary image
    primary = row.get("image_link", "").strip()
    if primary:
        urls.append(primary)
    
    # Additional images (pipe-separated within a comma-separated field)
    additional = row.get("additional_image_link", "").strip()
    if additional:
        # The field may contain comma-separated groups, each with pipe-separated URLs
        for group in additional.split(","):
            for url in group.strip().split("|"):
                url = url.strip()
                if url and url not in urls:
                    urls.append(url)
    
    return urls


def download_image(url: str) -> Image.Image:
    """Download an image from URL and return as PIL Image."""
    req = urllib.request.Request(url, headers={"User-Agent": "BluestoneSEO/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    return Image.open(io.BytesIO(data)).convert("RGBA")


def create_composite_sheet(images: list[Image.Image], max_cols: int = 3, 
                           cell_size: int = 512, padding: int = 10) -> Image.Image:
    """
    Create a composite contact sheet from multiple angle images.
    All images are resized to fit within cell_size while maintaining aspect ratio,
    then arranged in a grid on a white background.
    """
    n = len(images)
    cols = min(n, max_cols)
    rows = (n + cols - 1) // cols
    
    sheet_w = cols * (cell_size + padding) + padding
    sheet_h = rows * (cell_size + padding) + padding
    sheet = Image.new("RGB", (sheet_w, sheet_h), (255, 255, 255))
    
    for idx, img in enumerate(images):
        row = idx // cols
        col = idx % cols
        
        # Resize to fit cell while maintaining aspect ratio
        img_rgb = img.convert("RGB")
        w, h = img_rgb.size
        scale = min(cell_size / w, cell_size / h)
        new_w = int(w * scale)
        new_h = int(h * scale)
        img_resized = img_rgb.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # Center in cell
        x = padding + col * (cell_size + padding) + (cell_size - new_w) // 2
        y = padding + row * (cell_size + padding) + (cell_size - new_h) // 2
        sheet.paste(img_resized, (x, y))
    
    return sheet


def build_reference(product_title: str, output_name: str = None) -> Path:
    """
    Main function: find product, download all angles, build composite sheet.
    Returns path to the saved composite PNG.
    """
    print(f"Looking up: '{product_title}'...")
    row = find_product(product_title)
    if not row:
        sys.exit(f"Product not found in feed: '{product_title}'")
    
    actual_title = row["title"]
    product_id = row.get("id", "unknown")
    print(f"Found: {actual_title} (ID: {product_id})")
    
    urls = get_all_image_urls(row)
    print(f"Found {len(urls)} image URLs:")
    for i, url in enumerate(urls, 1):
        # Extract the shot type from URL
        if "BP-PICS" in url:
            shot_type = "Body Portrait"
        elif "PICS-00004" in url:
            shot_type = "Main/Hero"
        elif "PICS-00000" in url:
            shot_type = "Front"
        elif "PICS-00001" in url:
            shot_type = "Side/Angle 1"
        elif "PICS-00002" in url:
            shot_type = "Back/Angle 2"
        elif "PICS-00003" in url:
            shot_type = "Close-up/Angle 3"
        else:
            shot_type = "Other"
        print(f"  {i}. [{shot_type}] {url.split('/')[-1][:60]}...")
    
    print(f"\nDownloading {len(urls)} images...")
    images = []
    for i, url in enumerate(urls, 1):
        try:
            img = download_image(url)
            images.append(img)
            print(f"  Downloaded {i}/{len(urls)}: {img.size[0]}x{img.size[1]}")
        except Exception as e:
            print(f"  SKIP {i}/{len(urls)}: {e}")
    
    if not images:
        sys.exit("No images downloaded successfully!")
    
    print(f"\nCompositing {len(images)} angles into reference sheet...")
    sheet = create_composite_sheet(images)
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if output_name is None:
        safe_name = actual_title.lower().replace(" ", "_").replace("'", "")
        output_name = f"{safe_name}_multiangle_ref.png"
    
    out_path = OUTPUT_DIR / output_name
    sheet.save(out_path, "PNG")
    print(f"Saved: {out_path} ({sheet.size[0]}x{sheet.size[1]}, {out_path.stat().st_size // 1024} KB)")
    
    return out_path


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Build multi-angle reference sheet from product feed")
    p.add_argument("--product", required=True, help="Product title (partial match)")
    p.add_argument("--output", help="Output filename (default: auto-generated)")
    args = p.parse_args()
    build_reference(args.product, args.output)
