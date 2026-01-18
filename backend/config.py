import os

HF_MODEL_NAME = os.getenv("HF_MODEL_NAME", "google/vit-base-patch16-224")

CONFIDENCE_THRESHOLD = 0.25