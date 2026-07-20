import csv
import re
import urllib.request
import os
from pathlib import Path

ROOT = Path("/Users/vikasindoria/Documents/Geo and Seo/article generation seo codex")

def get_product_id(link):
    if not link:
        return None
    # e.g. https://www.bluestone.com/mangalsutra+chains/the-ninetta-mangalsutra-necklace~97026.html
    m = re.search(r'~(\d+)\.html', link)
    if m:
        return m.group(1)
    return None

def main():
    approved_csv = ROOT / "Seo Products - final products (1).csv"
    feed_csv = ROOT / "google_product_feed.csv"
    
    # 1. Map feed IDs to rows
    print("Loading Google product feed...")
    feed_map = {}
    with open(feed_csv, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            fid = row.get("id")
            if fid:
                feed_map[fid] = row
    print(f"Loaded {len(feed_map)} products from feed.")
    
    # 2. Iterate approved products and download raw images
    count = 0
    missing = []
    with open(approved_csv, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("Design Name")
            category = row.get("DesignCategory")
            link = row.get("Link")
            pid = get_product_id(link)
            
            if not pid:
                print(f"Could not parse ID from link for product: {name} ({link})")
                continue
                
            feed_row = feed_map.get(pid)
            if not feed_row:
                print(f"Product ID {pid} ({name}) not found in Google product feed.")
                missing.append(name)
                continue
                
            image_url = feed_row.get("image_link")
            if not image_url:
                print(f"No image_link found for product ID {pid} ({name})")
                continue
                
            # Determine extension from image_url
            ext = ".png"
            if image_url.lower().endswith(".jpg") or image_url.lower().endswith(".jpeg"):
                ext = ".jpg"
                
            dest_dir = ROOT / "ProductImages" / "raw" / category
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest_file = dest_dir / f"{name}{ext}"
            
            print(f"Downloading {name} ({pid}) to {dest_file.relative_to(ROOT)}...")
            try:
                req = urllib.request.Request(image_url, headers={"User-Agent": "BluestoneSEO/1.0"})
                with urllib.request.urlopen(req, timeout=30) as response:
                    dest_file.write_bytes(response.read())
                count += 1
            except Exception as e:
                print(f"Error downloading {name}: {e}")
                
    print(f"\nDone! Downloaded {count} raw images.")
    if missing:
        print(f"Missing products: {missing}")

if __name__ == "__main__":
    main()
