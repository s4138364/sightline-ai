from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io


from models.schemas import ImageInsightRequest, ImageInsightResponse
from services.insight_engine import generate_insight
from services.vision_inference import analyze_image

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Sightline AI backend is running"}
    
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze(
    tags: str = Form(...),
    image: UploadFile = File(...)
):
    # Parse tags string → list
    tag_list = [t.strip() for t in tags.split(",") if t.strip()]

    image_bytes = await image.read()
    image_obj = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    image_score = analyze_image(image_obj)
    text_result = generate_insight(tag_list)

    combined_score = round((image_score + text_result["score"]) / 2, 2)

    return {
        "image_score": round(image_score, 2),
        "text_score": round(text_result["score"], 2),
        "combined_score": combined_score,
        "insight": text_result["insight"]
    }
