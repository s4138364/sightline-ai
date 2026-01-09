from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io

from services.insight_engine import generate_insight
from services.vision_inference import analyze_image
from config import settings

app = FastAPI(title=settings.app_name)

# CORS (safe for local dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse("../frontend/index.html")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze(
    tags: str = Form(...),
    image: UploadFile = File(...)
):
    if not tags.strip():
        raise HTTPException(status_code=400, detail="Tags cannot be empty")

    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image")

    tag_list = [t.strip() for t in tags.split(",") if t.strip()]
    if not tag_list:
        raise HTTPException(status_code=400, detail="No valid tags provided")

    try:
        image_bytes = await image.read()
        image_obj = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")

    image_score = analyze_image(image_obj)
    text_result = generate_insight(tag_list)

    combined_score = round((image_score + text_result["score"]) / 2, 2)

    return {
        "image_score": round(image_score, 2),
        "text_score": round(text_result["score"], 2),
        "combined_score": combined_score,
        "insight": text_result["insight"]
    }
