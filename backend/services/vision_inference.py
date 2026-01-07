import logging
from PIL import Image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_image(image: Image.Image) -> float:
    logger.info("Running vision inference")

    # Placeholder logic (Day 12+ will improve this)
    width, height = image.size
    score = min((width * height) / 1_000_000, 1.0)

    return score
