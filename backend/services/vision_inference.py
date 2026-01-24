import time
import logging
import io
from PIL import Image
from transformers import pipeline

logging.basicConfig(level=logging.INFO)

# Load once (important for performance)
classifier = pipeline(
    "image-classification",
    model="google/vit-base-patch16-224"
)

logging.info("Vision model initialized")


def run_vision_model(image_bytes: bytes):
    """
    Runs Hugging Face image classification.
    Returns:
        labels: list[str]
        raw_predictions: list[dict]
        inference_time: float
    """
    start = time.time()

    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    results = classifier(image)

    inference_time = round(time.time() - start, 3)

    raw_predictions = [
        {
            "label": r["label"].lower(),
            "confidence": float(r["score"])
        }
        for r in results[:5]
    ]

    labels = [p["label"] for p in raw_predictions]

    logging.info(f"Detected labels: {labels}")
    logging.info(f"Inference time: {inference_time}s")

    return labels, raw_predictions, inference_time
