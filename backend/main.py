from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from utils.vision import detect_labels
from utils.ontology import expand_concepts

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🧠 In-memory feedback store (Day 31)
feedback_store = []

class Feedback(BaseModel):
    tags: list
    detected_labels: list
    expanded_concepts: list
    matches: list
    correct: bool

@app.post("/analyze")
async def analyze_image(
    image: UploadFile = File(...),
    tags: str = Form(...)
):
    user_tags = [t.strip().lower() for t in tags.split(",") if t.strip()]

    detected_labels = detect_labels(await image.read())
    detected_labels = [l.lower() for l in detected_labels]

    expanded = expand_concepts(detected_labels)

    matches = []
    for tag in user_tags:
        matches.append({
            "tag": tag,
            "matched": tag in expanded
        })

    return {
        "tags": user_tags,
        "detected_labels": detected_labels,
        "expanded_concepts": sorted(list(expanded)),
        "matches": matches
    }

@app.post("/feedback")
async def receive_feedback(feedback: Feedback):
    feedback_store.append(feedback.dict())
    return {"status": "feedback received"}
