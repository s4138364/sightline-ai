import time

print("🔥 vision_inference.py loaded")

import logging
from PIL import Image
from transformers import pipeline
import io

logging.basicConfig(level=logging.INFO)

# Load once (IMPORTANT for performance)
classifier = pipeline(
    "image-classification",
    model="google/vit-base-patch16-224"
)

print("✅ Vision model initialized")

def run_vision_model(image_bytes: bytes):
    """
    Runs Hugging Face image classification
    Returns list[str] of detected labels
    """
    print("🔥 run_vision_model CALLED")

    start = time.time()

    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    
    results = classifier(image)

    duration = round(time.time() - start, 3)
    logging.info(f"Inference time: {duration}s")

    labels = [
        {
            "label": r["label"].lower(),
            "confidence": float(r["score"])
        }
        for r in results[:5]
    ]

    return labels, duration
  
