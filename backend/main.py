import logging
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from services.vision_inference import run_vision_model
from utils.semantic import compute_similarity
from utils.scoring import score_image

logging.basicConfig(level=logging.INFO)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
async def analyze_image(
    image: UploadFile = File(...),
    tags: str = Form("")
):
    user_tags = [t.strip().lower() for t in tags.split(",") if t.strip()]

    image_bytes = await image.read()

    detected_labels, raw_predictions, inference_time = run_vision_model(image_bytes)

    semantic_similarities = compute_similarity(
        detected_labels,
        user_tags
    )

    result = score_image(
        detected_labels=detected_labels,
        user_tags=user_tags,
        semantic_similarities=semantic_similarities
    )

    explanation = []

    for tag in result["matched_tags"]:
        explanation.append(f"'{tag}' matches image content semantically.")

    for tag in result["missing_tags"]:
        explanation.append(f"'{tag}' does not semantically match the image.")

    response = {
        **result,
        "detected_labels": detected_labels,
        "raw_predictions": raw_predictions,
        "inference_time_seconds": inference_time,
        "explanation": explanation
    }

    logging.info(response)

    return response
