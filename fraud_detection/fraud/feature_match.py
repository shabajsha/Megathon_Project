# feature_match.py
import cv2
import os
from tqdm import tqdm
import numpy as np

IMAGES_DIR = "images"  # same images folder
MIN_MATCH_COUNT = 10  # if >= this many good matches => likely same image

def orb_match(img1_path, img2_path):
    img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)
    if img1 is None or img2 is None:
        return 0
    orb = cv2.ORB_create(2000)
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)
    if des1 is None or des2 is None:
        return 0
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)
    good = [m for m in matches if m.distance < 60]  # 60 is heuristic
    return len(good)

def find_best_match(new_img):
    files = [f for f in os.listdir(IMAGES_DIR) if f.lower().endswith((".jpg",".jpeg",".png"))]
    best = ("", 0)
    for f in files:
        score = orb_match(new_img, os.path.join(IMAGES_DIR, f))
        if score > best[1]:
            best = (f, score)
    return best

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python feature_match.py path/to/new_image.jpg")
        exit(1)
    new = sys.argv[1]
    best_file, score = find_best_match(new)
    print(f"Best match: {best_file}, ORB good matches: {score}")
    if score >= MIN_MATCH_COUNT:
        print("Likely reused/edited image.")
    else:
        print("No strong feature-based match.")
