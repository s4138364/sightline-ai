import torch
import logging
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import io
import time

logging.basicConfig(level=logging.INFO)

# Load once (VERY important)
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

logging.info("✅ CLIP model loaded")


def semantic_score_image(image_bytes: bytes, user_tags: list[str], threshold: float = 0.25):
    """
    Computes semantic similarity between image and user tags using CLIP
    """

    if not user_tags:
        return {
            "score": 0,
            "matched_tags": [],
            "missing_tags": [],
            "similarities": {}
        }

    start = time.time()

    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    # Prepare inputs
    inputs = processor(
        text=user_tags,
        images=image,
        return_tensors="pt",
        padding=True
    )

    with torch.no_grad():
        outputs = model(**inputs)

    # Cosine similarity
    image_embeds = outputs.image_embeds
    text_embeds = outputs.text_embeds

    image_embeds = image_embeds / image_embeds.norm(dim=-1, keepdim=True)
    text_embeds = text_embeds / text_embeds.norm(dim=-1, keepdim=True)

    similarities = (image_embeds @ text_embeds.T).squeeze(0)

    similarities = similarities.tolist()

    matched = []
    missing = []
    similarity_map = {}

    for tag, score in zip(user_tags, similarities):
        similarity_map[tag] = round(score, 3)
        if score >= threshold:
            matched.append(tag)
        else:
            missing.append(tag)

    final_score = int((len(matched) / len(user_tags)) * 100)

    duration = round(time.time() - start, 3)
    logging.info(f"Semantic inference time: {duration}s")

    return {
        "score": final_score,
        "matched_tags": matched,
        "missing_tags": missing,
        "similarities": similarity_map,
        "inference_time_seconds": duration,
        "confidence_threshold": threshold
    }