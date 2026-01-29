from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from utils.vision import detect_labels
from utils.ontology import expand_concepts

app = FastAPI()

# ✅ Allow opening index.html directly (file://)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_image(
    image: UploadFile = File(...),
    tags: str = Form(...)
):
    # User tags
    user_tags = [t.strip().lower() for t in tags.split(",") if t.strip()]

    # Vision
    detected_labels = detect_labels(await image.read())
    detected_labels = [l.lower() for l in detected_labels]

    # Ontology expansion
    expanded = expand_concepts(detected_labels)

    # Matching
    matches = []
    for tag in user_tags:
        matches.append({
            "tag": tag,
            "matched": tag in expanded
        })

    return {
        "detected_labels": detected_labels,
        "expanded_concepts": sorted(list(expanded)),
        "matches": matches
    }
