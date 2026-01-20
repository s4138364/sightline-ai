import logging
import hashlib
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from utils.semantic_scoring import semantic_score_image

from services.vision_inference import run_vision_model
from utils.scoring import score_image

logging.basicConfig(level=logging.INFO)

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

# Simple in-memory cache
REQUEST_CACHE = {}

@app.post("/analyze")
async def analyze_image(
    image: UploadFile = File(...),
    tags: str = Form("")
):
    user_tags = [t.strip() for t in tags.split(",") if t.strip()]

    image_bytes = await image.read()

    # Cache key based on image + tags
    cache_key = hashlib.sha256(image_bytes + tags.encode()).hexdigest()

    if cache_key in REQUEST_CACHE:
        logging.info("Cache hit")
        return REQUEST_CACHE[cache_key]

    raw_predictions, inference_time = run_vision_model(image_bytes)

    filtered_labels = [
        p["label"]
        for p in raw_predictions
        if p["confidence"] >= 0.25
    ]

    semantic_result = semantic_score_image(image_bytes, user_tags)

    result = {
        **semantic_result,
        "filtered_labels": filtered_labels
    }


    explanation = []

    for tag in result["matched_tags"]:
        explanation.append(f"The image appears to contain '{tag}'.")

    for tag in result["missing_tags"]:
        explanation.append(f"The model did not detect '{tag}'.")

    logging.info(f"Tags: {user_tags}")
    logging.info(f"Detected: {filtered_labels}")
    logging.info(f"Score result: {result}")

    response = {
        **result,
        "inference_time_seconds": inference_time,
        "confidence_threshold": 0.25,
        "raw_predictions": raw_predictions,
        "explanation": explanation
    }

    REQUEST_CACHE[cache_key] = response
    return response
