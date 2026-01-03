from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    print("Root endpoint called")
    return {"message": "Sightline AI backend is running"}

@app.get("/health")
def health_check():
    print("Health check called")
    return {"status": "ok"}
