# ela_tamper.py
from PIL import Image, ImageChops, ImageEnhance
import os
import numpy as np

def ela_image(path, quality=90):
    orig = Image.open(path).convert('RGB')
    temp_path = "_temp_ela.jpg"
    orig.save(temp_path, 'JPEG', quality=quality)
    compressed = Image.open(temp_path)
    ela = ImageChops.difference(orig, compressed)
    extrema = ela.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    if max_diff == 0:
        scale = 1
    else:
        scale = 255.0 / max_diff
    ela = ImageEnhance.Brightness(ela).enhance(scale)
    return ela, max_diff

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python ela_tamper.py path/to/image.jpg")
        exit(1)
    ela_img, max_diff = ela_image(sys.argv[1])
    ela_img.show()
    print("Max diff:", max_diff)
