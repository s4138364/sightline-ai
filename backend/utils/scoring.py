def score_image(detected_labels, user_tags):
    detected = [label.lower() for label in detected_labels]
    requested = [tag.lower() for tag in user_tags]

    matched = []
    missing = []

    for tag in requested:
        if any(tag in label for label in detected):
            matched.append(tag)
        else:
            missing.append(tag)

    score = 0
    if requested:
        score = int((len(matched) / len(requested)) * 100)

    return {
        "score": score,
        "matched_tags": matched,
        "missing_tags": missing,
        "detected_labels": detected
    }
