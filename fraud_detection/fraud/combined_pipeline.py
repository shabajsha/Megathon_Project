# combined_pipeline.py
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import timm, torch, torchvision.transforms as T
import os

EMB_FILE = "embeddings.npy"
FILES_TXT = "filenames.txt"

def load_index():
    embs = np.load(EMB_FILE)
    with open(FILES_TXT) as f:
        files = [x.strip() for x in f.readlines()]
    return embs, files

# model same as compute_embeddings
transform = T.Compose([
    T.Resize((224,224)),
    T.ToTensor(),
    T.Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225])
])
def get_model(device):
    model = timm.create_model('efficientnet_b0', pretrained=True, num_classes=0, global_pool='avg')
    model.eval()
    model.to(device)
    return model

def embed_image(path, model, device):
    img = Image.open(path).convert("RGB")
    x = transform(img).unsqueeze(0).to(device)
    with torch.no_grad():
        feat = model(x).cpu().numpy().squeeze()
    return feat

def find_nearest(new_img_path, topk=3, device='cpu'):
    embs, files = load_index()
    model = get_model(device)
    q = embed_image(new_img_path, model, device).reshape(1,-1)
    sims = cosine_similarity(q, embs).squeeze()
    idxs = sims.argsort()[::-1][:topk]
    results = [(files[i], float(sims[i])) for i in idxs]
    return results

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python combined_pipeline.py path/to/new_image.jpg")
        exit(1)
    res = find_nearest(sys.argv[1], topk=5, device='cpu')
    print("Top matches (filename, cosine_score):")
    for r in res:
        print(r)
