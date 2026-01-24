import time
import logging
import io
import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from utils.ontology import ONTOLOGY

logging.basicConfig(level=logging.INFO)

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

logging.info("✅ CLIP model loaded")


def semantic_score_image(
    image_bytes: bytes,
    user_tags: list[str],
    detected_labels: list[str],
    threshold: float = 0.25
):
    if not user_tags:
        return {
            "score": 0,
            "matched_tags": [],
            "missing_tags": [],
            "similarities": {}
        }

    start = time.time()

    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    inputs = processor(
        text=user_tags,
        images=image,
        return_tensors="pt",
        padding=True
    )

    with torch.no_grad():
        outputs = model(**inputs)

    image_embeds = outputs.image_embeds
    text_embeds = outputs.text_embeds

    image_embeds = image_embeds / image_embeds.norm(dim=-1, keepdim=True)
    text_embeds = text_embeds / text_embeds.norm(dim=-1, keepdim=True)

    similarities = (image_embeds @ text_embeds.T).squeeze(0).tolist()

    matched, missing = [], []
    similarity_map = {}

    for tag, sim in zip(user_tags, similarities):
        boosted = sim

        # 1. Direct detection boost
        if tag in detected_labels:
            boosted = max(boosted, threshold + 0.2)

        # 2. Ontology-based boost (CORRECT)
        for detected in detected_labels:
            parents = ONTOLOGY.get(detected, [])
            if tag in parents:
                boosted = max(boosted, threshold + 0.15)

        similarity_map[tag] = round(boosted, 3)

        if boosted >= threshold:
            matched.append(tag)
        else:
            missing.append(tag)

    score = int((len(matched) / len(user_tags)) * 100)
    duration = round(time.time() - start, 3)

    return {
        "score": score,
        "matched_tags": matched,
        "missing_tags": missing,
        "similarities": similarity_map,
        "confidence_threshold": threshold,
        "semantic_inference_time_seconds": duration
    }
