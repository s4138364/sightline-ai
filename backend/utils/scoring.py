from utils.feedback import load_thresholds

# ------------------------
# Tag categories
# ------------------------

TAG_CATEGORIES = {
    "animal": "generic",
    "cat": "specific_animal",
    "dog": "specific_animal",
    "horse": "specific_animal",

    "yellow": "color",
    "red": "color",

    "car": "object",
    "tree": "object"
}

ANIMAL_CLASSES = {
    "dog", "cat", "horse", "cow", "sheep", "bird", "fish"
}


# ------------------------
# Threshold logic
# ------------------------

def threshold_for_tag(tag: str) -> float:
    thresholds = load_thresholds()
    category = TAG_CATEGORIES.get(tag, "object")
    return thresholds.get(category, 0.55)


def confidence_band(score: float, threshold: float) -> str:
    if score >= threshold:
        return "strong"
    if score >= threshold - 0.1:
        return "weak"
    return "none"


# ------------------------
# Main scoring
# ------------------------

def score_image(
    detected_labels,
    user_tags,
    semantic_similarities
):
    results = []
    detected_text = " ".join(detected_labels)

    for tag in user_tags:
        similarity = semantic_similarities.get(tag, 0)
        threshold = threshold_for_tag(tag)
        band = confidence_band(similarity, threshold)

        # Mutually exclusive animals
        if tag in ANIMAL_CLASSES:
            for animal in ANIMAL_CLASSES:
                if animal != tag and animal in detected_text:
                    band = "none"
                    similarity = 0
                    break

        results.append({
            "tag": tag,
            "similarity": round(similarity, 3),
            "confidence": band,
            "threshold": threshold,
            "category": TAG_CATEGORIES.get(tag, "object")
        })

    results.sort(key=lambda x: x["similarity"], reverse=True)

    matched = [r["tag"] for r in results if r["confidence"] == "strong"]
    missing = [r["tag"] for r in results if r["confidence"] != "strong"]

    score = int((len(matched) / len(user_tags)) * 100) if user_tags else 0

    return {
        "score": score,
        "matched_tags": matched,
        "missing_tags": missing,
        "ranked_results": results,
        "active_thresholds": load_thresholds()
    }
