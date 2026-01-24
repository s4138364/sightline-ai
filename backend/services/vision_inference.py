import time
import logging
import io
from PIL import Image
from transformers import pipeline

logging.basicConfig(level=logging.INFO)

print("🔥 vision_inference.py loaded")

classifier = pipeline(
    "image-classification",
    model="google/vit-base-patch16-224"
)

print("✅ Vision model initialized")


def run_vision_model(image_bytes: bytes):
    start = time.time()

    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    results = classifier(image)

    duration = round(time.time() - start, 3)

    predictions = [
        {
            "label": r["label"].lower(),
            "confidence": float(r["score"])
        }
        for r in results[:5]
    ]

    logging.info(f"Vision predictions: {predictions}")
    return predictions, duration
