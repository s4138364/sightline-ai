from transformers import pipeline

# Load once at startup (important for performance)
classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def run_model(text: str) -> dict:
    result = classifier(text)[0]

    return {
        "label": result["label"],
        "confidence": float(result["score"])
    }
