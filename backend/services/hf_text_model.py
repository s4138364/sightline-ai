import logging
from transformers import pipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Loading Hugging Face text model...")

classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def run_text_model(text: str) -> float:
    """
    Runs sentiment analysis on input text and returns a confidence score (0–1)
    """
    result = classifier(text)[0]

    score = result["score"]
    return round(score, 2)
