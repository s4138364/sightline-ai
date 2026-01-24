import logging
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from services.vision_inference import run_vision_model
from utils.scoring import score_image
from utils.ontology import expand_concepts

logging.basicConfig(level=logging.INFO)

app = FastAPI()

# --- CORS ---
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
    # -------------------------
    # 1. Parse user tags
    # -------------------------
    user_tags = [t.strip().lower() for t in tags.split(",") if t.strip()]

    # -------------------------
    # 2. Run vision inference
    # -------------------------
    image_bytes = await image.read()
    raw_predictions, inference_time = run_vision_model(image_bytes)

    # Extract labels only
    raw_labels = [p["label"] for p in raw_predictions]

    # -------------------------
    # 3. Ontology expansion
    # -------------------------
    expanded_labels = expand_concepts(raw_labels)

    # -------------------------
    # 4. Score image
    # -------------------------
    result = score_image(
        detected_labels=expanded_labels,
        user_tags=user_tags,
        raw_predictions=raw_predictions
    )

    confidence_explanations = []

    for tag in result["matched_tags"]:
        conf = result["similarities"].get(tag, 0)

        if conf >= 0.5:
            confidence_explanations.append(
                f"High confidence match for '{tag}'."
            )
        elif conf >= result["confidence_threshold"]:
            confidence_explanations.append(
                f"Moderate confidence match for '{tag}'."
            )
        else:
            confidence_explanations.append(
                f"Low confidence match for '{tag}'."
            )


    # -------------------------
    # 5. Build explanation
    # -------------------------
    explanation = []

    for tag in result["matched_tags"]:
        explanation.append(f"The image appears to contain '{tag}'.")

    for tag in result["missing_tags"]:
        explanation.append(f"The model did not detect '{tag}'.")

    # -------------------------
    # 6. Logging
    # -------------------------
    logging.info(f"User tags: {user_tags}")
    logging.info(f"Raw labels: {raw_labels}")
    logging.info(f"Expanded labels: {expanded_labels}")
    logging.info(f"Score result: {result}")

    # -------------------------
    # 7. Response
    # -------------------------
    return {
        **result,
        "raw_predictions": raw_predictions,
        "detected_labels": expanded_labels,
        "inference_time_seconds": inference_time,
        "explanation": explanation,
        "confidence_explanation": confidence_explanations
    }
