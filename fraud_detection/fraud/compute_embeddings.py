# compute_embeddings.py
import os
import torch
import torchvision.transforms as T
from PIL import Image
import numpy as np
from tqdm import tqdm
import timm  # high-quality pretrained models
import argparse

IMAGES_DIR = "images"
OUT_EMB = "embeddings.npy"
OUT_FILES = "filenames.txt"

def get_model(device):
    model = timm.create_model('efficientnet_b0', pretrained=True, num_classes=0, global_pool='avg')
    model.eval()
    model.to(device)
    return model

transform = T.Compose([
    T.Resize((224,224)),
    T.ToTensor(),
    T.Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225])
])

def compute_embeddings(device='cpu'):
    device = torch.device(device)
    model = get_model(device)
    files = sorted([f for f in os.listdir(IMAGES_DIR) if f.lower().endswith((".jpg",".jpeg",".png"))])
    embs = []
    for f in tqdm(files, desc="computing embeddings"):
        path = os.path.join(IMAGES_DIR, f)
        img = Image.open(path).convert("RGB")
        x = transform(img).unsqueeze(0).to(device)
        with torch.no_grad():
            feat = model(x).cpu().numpy().squeeze()
        embs.append(feat)
    embs = np.stack(embs)
    np.save(OUT_EMB, embs)
    with open(OUT_FILES, "w") as fh:
        fh.write("\n".join(files))
    print("Saved embeddings and filenames.")

if __name__ == "__main__":
    import sys
    dev = 'cpu'
    if len(sys.argv) > 1:
        dev = sys.argv[1]
    compute_embeddings(device=dev)
