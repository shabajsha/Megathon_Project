# pipeline_check.py
from check_duplicate import is_duplicate, load_hashes
from feature_match import find_best_match
from combined_pipeline import find_nearest
from ela_tamper import ela_image
from ai_detector import detect_ai
import numpy as np
import cv2

# ---------- New heuristics: blur and crop detection ----------
def compute_blur_score(path: str):
    """Return blur score in [0,1]. Higher = more blurred."""
    try:
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return 0.0
        lap = cv2.Laplacian(img, cv2.CV_64F)
        var = float(np.var(lap))
        # map variance to [0,1] where low variance = high blur score
        # using soft normalization
        score = 1.0 - (var / (var + 100.0))
        return float(max(0.0, min(1.0, score)))
    except Exception:
        return 0.0


def compute_crop_score(path: str):
    """Return crop score in [0,1]. Higher = more likely cropped (content occupies small part).
    Heuristic: compute bounding box of edge pixels and compare its area to image area.
    """
    try:
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return 0.0
        h, w = img.shape[:2]
        # detect edges
        edges = cv2.Canny(img, 50, 150)
        ys, xs = np.where(edges > 0)
        if len(xs) == 0 or len(ys) == 0:
            # fallback: use non-white content
            thresh = cv2.threshold(img, 250, 255, cv2.THRESH_BINARY_INV)[1]
            ys, xs = np.where(thresh > 0)
            if len(xs) == 0:
                return 0.0
        x1, x2 = int(xs.min()), int(xs.max())
        y1, y2 = int(ys.min()), int(ys.max())
        bbox_area = max(1, (x2 - x1 + 1)) * max(1, (y2 - y1 + 1))
        img_area = float(max(1, w * h))
        bbox_ratio = bbox_area / img_area
        # if bounding box area is small, image likely cropped or focused; invert ratio to get crop score
        crop_score = 1.0 - bbox_ratio
        # clamp and scale a bit to reduce false positives
        crop_score = float(max(0.0, min(1.0, (crop_score - 0.05) / 0.95)))
        return crop_score
    except Exception:
        return 0.0

# -------------------------------------------------------------

# thresholds (tune these)
HASH_THRESH = 6
ORB_MIN_MATCH = 10
EMB_SIM_THRESH = 0.88
ELA_DIFF_THRESH = 10  # heuristic, depends on images

def aggregate_decision(new_img_path):
    # 1. hash duplicate
    hashes = load_hashes("hashes.csv")
    dup, matched_fname, hdist = is_duplicate(new_img_path, hashes, threshold=HASH_THRESH)
    hash_score = 1.0 if dup else 0.0

    # 2. feature match
    best_file, score = find_best_match(new_img_path)
    feature_score = min(1.0, score / (ORB_MIN_MATCH * 2))  # normalize to [0,1]

    feature_flag = score >= ORB_MIN_MATCH

    # 3. embeddings
    emb_results = find_nearest(new_img_path, topk=1, device='cpu')
    top_name, cos_sim = emb_results[0]
    emb_flag = cos_sim >= EMB_SIM_THRESH
    emb_score = (cos_sim - EMB_SIM_THRESH) / (1-EMB_SIM_THRESH) if cos_sim >= EMB_SIM_THRESH else 0.0
    emb_score = max(0.0, min(1.0, emb_score))

    # 4. ELA tamper
    ela_img, max_diff = ela_image(new_img_path)
    tamper_flag = max_diff > ELA_DIFF_THRESH
    tamper_score = min(1.0, max_diff / 50.0)  # heuristic normalizer

    # 5. AI-generation detection
    ai_flag, ai_score, ai_reasons = detect_ai(new_img_path)

    # 6. blur and crop heuristics
    blur_score = compute_blur_score(new_img_path)
    crop_score = compute_crop_score(new_img_path)

    # aggregate fraud confidence (weighted)
    # weights: hash (0.35), features (0.20), embeddings (0.20), blur (0.10), crop (0.10), tamper (0.05)
    fraud_conf = (
        0.35 * hash_score
        + 0.20 * feature_score
        + 0.20 * emb_score
        + 0.10 * blur_score
        + 0.10 * crop_score
        + 0.05 * tamper_score
    )
    fraud_conf = float(max(0.0, min(1.0, fraud_conf)))

    # --------- Override / Boost rules (ensure high fraud for critical signals) ---------
    # These are conservative but force higher fraud when strong signals are present.
    # You can tune the thresholds/boosts below.
    BOOSTS = {
        'duplicate_min': 0.95,   # exact/near duplicate -> very high fraud
        'ai_min': 0.85,          # AI-generation above ai_threshold -> high fraud
        'ai_threshold': 0.6,
        'blur_min': 0.75,        # strongly blurred images
        'blur_threshold': 0.6,
        'crop_min': 0.80,        # strongly cropped images (whole image missing)
        'crop_threshold': 0.6,
        'feature_emb_min': 0.95, # both strong feature+embedding match
    }

    if dup:
        fraud_conf = max(fraud_conf, BOOSTS['duplicate_min'])

    if ai_flag and ai_score >= BOOSTS['ai_threshold']:
        fraud_conf = max(fraud_conf, BOOSTS['ai_min'])

    if blur_score >= BOOSTS['blur_threshold']:
        fraud_conf = max(fraud_conf, BOOSTS['blur_min'])

    if crop_score >= BOOSTS['crop_threshold']:
        fraud_conf = max(fraud_conf, BOOSTS['crop_min'])

    if feature_flag and emb_flag:
        fraud_conf = max(fraud_conf, BOOSTS['feature_emb_min'])

    # final clamp
    fraud_conf = float(max(0.0, min(1.0, fraud_conf)))

    result = {
        "duplicate_hash": dup,
        "hash_hamming": int(hdist) if hdist is not None else None,
        "feature_matches": int(score),
        "feature_flag": bool(feature_flag),
        "feature_score": float(feature_score),
        "blur_score": float(blur_score),
        "crop_score": float(crop_score),
        "embedding_top_match": top_name,
        "embedding_cosine": float(cos_sim),
        "embedding_flag": bool(emb_flag),
        "tamper_max_diff": int(max_diff),
        "tamper_flag": bool(tamper_flag),
        "ai_generated": bool(ai_flag),
        "ai_score": float(ai_score),
        "ai_reasons": ai_reasons,
        "fraud_confidence": fraud_conf
    }
    return result

if __name__ == "__main__":
    import sys, json
    if len(sys.argv) < 2:
        print("Usage: python pipeline_check.py path/to/image.jpg")
        exit(1)
    res = aggregate_decision(sys.argv[1])
    # Print only fraud percentage (0-100) as an integer
    pct = int(round(res.get("fraud_confidence", 0.0) * 100.0))
    print(pct)
