# check_duplicate.py
import imagehash
from PIL import Image
import csv
import os

HASH_CSV = "hashes.csv"
THRESHOLD = 6   # phash Hamming distance threshold; tune from 4-10. lower = stricter

def load_hashes(csvfile):
    data = {}
    with open(csvfile, newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            data[r['filename']] = r['phash']
    return data

def is_duplicate(new_img_path, existing_hashes, threshold=THRESHOLD):
    new_hash = imagehash.phash(Image.open(new_img_path).convert("RGB"))
    for fname, ph in existing_hashes.items():
        dist = new_hash - imagehash.hex_to_hash(ph)
        if dist <= threshold:
            return True, fname, dist
    return False, None, None

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python check_duplicate.py path/to/new_image.jpg")
        exit(1)
    new = sys.argv[1]
    hashes = load_hashes(HASH_CSV)
    dup, matched_fname, d = is_duplicate(new, hashes)
    if dup:
        print(f"Possible duplicate! matched: {matched_fname}, hamming distance={d}")
    else:
        print("No duplicate found.")
