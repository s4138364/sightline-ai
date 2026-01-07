import logging
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch


logging.basicConfig(level=logging.INFO)

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def analyze_image(image: Image.Image) -> float:
    logging.info("Running vision inference")
    inputs = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        outputs = model.get_image_features(**inputs)

    # Normalize embedding magnitude as a proxy quality score
    score = outputs.norm().item()

    # Normalize to 0–1 range (rough heuristic)
    normalized = min(score / 50.0, 1.0)

    return normalized
