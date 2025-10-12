# compute_hashes.py
import os
from PIL import Image
import imagehash
import csv
from tqdm import tqdm

IMAGES_DIR = "images"  # place your 'damage' images here
OUT_CSV = "hashes.csv"

hash_funcs = {
    "ahash": imagehash.average_hash,
    "phash": imagehash.phash,
    "dhash": imagehash.dhash
}

def compute_hashes_for_image(path):
    im = Image.open(path).convert("RGB")
    results = {}
    for name, fn in hash_funcs.items():
        results[name] = str(fn(im))
    return results

def main():
    rows = []
    files = sorted([f for f in os.listdir(IMAGES_DIR) if f.lower().endswith((".png",".jpg",".jpeg"))])
    for fname in tqdm(files, desc="hashing images"):
        path = os.path.join(IMAGES_DIR, fname)
        hs = compute_hashes_for_image(path)
        row = {"filename": fname}
        row.update(hs)
        rows.append(row)

    # write CSV
    with open(OUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["filename"] + list(hash_funcs.keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved hashes to {OUT_CSV}")

if __name__ == "__main__":
    main()
