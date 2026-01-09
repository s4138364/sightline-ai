import logging
from services.hf_text_model import run_text_model

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_text(tags: list[str]) -> float:
    logger.info("Running Hugging Face text inference")

    combined_text = " ".join(tags)
    score = run_text_model(combined_text)

    return score
