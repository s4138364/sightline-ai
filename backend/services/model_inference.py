import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_text(tags: list[str]) -> float:
    logger.info("Running text inference")

    score = min(len(tags) / 5, 1.0)
    return score
