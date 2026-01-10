import logging
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

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
    user_tags = [t.strip() for t in tags.split(",") if t.strip()]

    # TEMP deterministic labels (AI comes later)
    detected_labels = ["cat", "animal", "pet"]

    result = score_image(detected_labels, user_tags)

    logging.info(f"Tags: {user_tags}")
    logging.info(f"Detected: {detected_labels}")
    logging.info(f"Score result: {result}")

    return result
