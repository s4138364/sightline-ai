def score_image(detected_labels, user_tags):
    detected = set(label.lower() for label in detected_labels)
    requested = set(tag.lower() for tag in user_tags)

    matched = detected.intersection(requested)
    missing = requested.difference(detected)

    score = 0
    if requested:
        score = int((len(matched) / len(requested)) * 100)

    return {
        "score": score,
        "matched_tags": list(matched),
        "missing_tags": list(missing),
        "detected_labels": list(detected)
    }
