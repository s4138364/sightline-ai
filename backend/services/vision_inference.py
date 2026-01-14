import time
import logging
import io
from PIL import Image
from transformers import pipeline

logging.basicConfig(level=logging.INFO)

print("🔥 vision_inference.py loaded")

# Load once at startup (IMPORTANT)
classifier = pipeline(
    "image-classification",
    model="google/vit-base-patch16-224"
)

print("✅ Vision model initialized")

def run_vision_model(image_bytes: bytes):
    """
    Runs Hugging Face image classification
    Returns (labels, inference_time)
    """

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
