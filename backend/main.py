from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import time

from utils.ontology import normalize_label, expand_concepts
from utils.scoring import score_image
from utils.vision import run_vision_model

app = FastAPI()

# ✅ CORS FIX (THIS IS CRITICAL)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # fine for local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_image(
    image: UploadFile = File(...),
    tags: List[str] = Form(...)
):
    start = time.time()

    image_bytes = await image.read()

    # Vision model
    raw_predictions, inference_time = run_vision_model(image_bytes)

    # Normalize labels
    detected_labels = [
        normalize_label(p["label"])
        for p in raw_predictions
    ]

    # Expand ontology (cat → animal)
    expanded_labels = expand_concepts(detected_labels)

    result = score_image(
        detected_labels=expanded_labels,
        user_tags=[t.lower().strip() for t in tags]
    )

    result["raw_predictions"] = raw_predictions
    result["inference_time_seconds"] = round(inference_time, 3)
    result["semantic_inference_time_seconds"] = round(time.time() - start, 3)

    return result
