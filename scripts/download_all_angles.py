import csv
import re
import urllib.request
import urllib.error
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

ROOT = Path("/Users/vikasindoria/Documents/Geo and Seo/article generation seo codex")

def get_product_id(link):
    if not link:
        return None
    m = re.search(r'~(\d+)\.html', link)
    if m:
        return m.group(1)
    return None

def get_all_image_urls(row):
    urls = []
    primary = row.get("image_link", "").strip()
    if primary:
        urls.append(primary)
    
    additional = row.get("additional_image_link", "").strip()
    if additional:
        for group in additional.split(","):
            for url in group.strip().split("|"):
                url = url.strip()
                if url and url not in urls:
                    urls.append(url)
    return urls

def download_file(url, dest_path):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "BluestoneSEO/1.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            dest_path.write_bytes(r.read())
        return True
    except Exception as e:
        print(f"Error downloading {url} to {dest_path.name}: {e}")
        return False

def download_product_angles(name, category, pid, feed_row):
    urls = get_all_image_urls(feed_row)
    if not urls:
        return 0
        
    product_dir = ROOT / "ProductImages" / "raw" / category / name
    product_dir.mkdir(parents=True, exist_ok=True)
    
    downloaded = 0
    for idx, url in enumerate(urls):
        ext = ".png"
        if url.lower().endswith(".jpg") or url.lower().endswith(".jpeg"):
            ext = ".jpg"
            
        # Determine descriptive suffix based on naming convention
        if idx == 0:
            filename = f"0_primary{ext}"
        else:
            if "BP-PICS" in url:
                filename = f"{idx}_body_portrait{ext}"
            elif "PICS-00000" in url:
                filename = f"{idx}_front{ext}"
            elif "PICS-00001" in url:
                filename = f"{idx}_side_1{ext}"
            elif "PICS-00002" in url:
                filename = f"{idx}_back{ext}"
            elif "PICS-00003" in url:
                filename = f"{idx}_close_up{ext}"
            else:
                filename = f"{idx}_angle{ext}"
                
        dest_path = product_dir / filename
        if download_file(url, dest_path):
            downloaded += 1
            
    print(f"Downloaded {downloaded} angles for {name} ({pid})")
    return downloaded

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
    tasks = []
    with open(approved_csv, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("Design Name")
            category = row.get("DesignCategory")
            link = row.get("Link")
            pid = get_product_id(link)
            
            if not pid:
                continue
                
            feed_row = feed_map.get(pid)
            if not feed_row:
                continue
                
            tasks.append((name, category, pid, feed_row))
            
    print(f"Starting downloads for {len(tasks)} products...")
    total_downloaded = 0
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [
            executor.submit(download_product_angles, name, category, pid, feed_row)
            for name, category, pid, feed_row in tasks
        ]
        for f in futures:
            total_downloaded += f.result()
            
    print(f"\nDone! Downloaded {total_downloaded} total angle images across {len(tasks)} products.")

if __name__ == "__main__":
    main()
