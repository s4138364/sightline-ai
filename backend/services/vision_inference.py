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

def run_vision_model(image_bytes: bytes):
    """
    Runs Hugging Face image classification
    Returns list[str] of detected labels
    """
    print("🔥 run_vision_model CALLED")

    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    results = classifier(image)

    # Extract top labels only
    labels = [r["label"].lower() for r in results[:5]]

    logging.info(f"Vision labels: {labels}")

    return labels
