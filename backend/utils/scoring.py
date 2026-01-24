def score_image(
    detected_labels: list[str],
    user_tags: list[str],
    raw_predictions: list[dict],
    confidence_threshold: float = 0.25
):
    matched = []
    missing = []
    similarities = {}

    # Map raw labels to confidence
    confidence_map = {
        p["label"].lower(): p["confidence"]
        for p in raw_predictions
    }

    for tag in user_tags:
        if tag in detected_labels:
            matched.append(tag)

            # Find confidences of labels related to this tag
            related_confidences = [
                conf
                for lbl, conf in confidence_map.items()
                if tag in lbl
            ]

            similarities[tag] = max(related_confidences) if related_confidences else 1.0
        else:
            missing.append(tag)
            similarities[tag] = 0.0

    confidence_levels = {}

    for label, conf in confidence_map.items():
        if conf >= 0.5:
            confidence_levels[label] = "high"
        elif conf >= confidence_threshold:
            confidence_levels[label] = "medium"
        else:
            confidence_levels[label] = "low"

    score = int((len(matched) / max(len(user_tags), 1)) * 100)

    return {
        "score": score,
        "matched_tags": matched,
        "missing_tags": missing,
        "similarities": similarities,
        "confidence_levels": confidence_levels,
        "confidence_threshold": confidence_threshold
    }
