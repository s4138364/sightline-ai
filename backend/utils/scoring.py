ANIMAL_CLASSES = {
    "dog", "cat", "horse", "cow", "sheep", "bird", "fish"
}

STRONG_MATCH = 0.55
WEAK_MATCH = 0.40


def confidence_band(score: float) -> str:
    if score >= STRONG_MATCH:
        return "strong"
    if score >= WEAK_MATCH:
        return "weak"
    return "none"


def score_image(
    detected_labels,
    user_tags,
    semantic_similarities
):
    results = []

    detected_text = " ".join(detected_labels)

    for tag in user_tags:
        similarity = semantic_similarities.get(tag, 0)
        band = confidence_band(similarity)

        # Block mutually exclusive animals
        if tag in ANIMAL_CLASSES:
            for animal in ANIMAL_CLASSES:
                if animal != tag and animal in detected_text:
                    band = "none"
                    similarity = 0
                    break

        results.append({
            "tag": tag,
            "similarity": round(similarity, 3),
            "confidence": band
        })

    # Rank tags by similarity
    results.sort(key=lambda x: x["similarity"], reverse=True)

    matched = [r["tag"] for r in results if r["confidence"] == "strong"]
    missing = [r["tag"] for r in results if r["confidence"] != "strong"]

    score = int((len(matched) / len(user_tags)) * 100) if user_tags else 0

    return {
        "score": score,
        "matched_tags": matched,
        "missing_tags": missing,
        "ranked_results": results,
        "thresholds": {
            "strong": STRONG_MATCH,
            "weak": WEAK_MATCH
        }
    }
