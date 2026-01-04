from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    print("Root endpoint called")
    return {"message": "Sightline AI backend is running"}

@app.get("/health")
def health_check():
    print("Health check called")
    return {"status": "ok"}

@app.post("/analyze")
def analyze(data: dict):
    user_input = data.get("text", "")

    return {
        "original": user_input,
        "length": len(user_input),
        "message": "Text received successfully"
    }
