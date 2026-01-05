from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models.schemas import ImageInsightRequest, ImageInsightResponse
from services.insight_engine import generate_insight

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

@app.post("/analyze", response_model=ImageInsightResponse)
def analyze_image(data: ImageInsightRequest):
    result = generate_insight(data.tags)
    return result
