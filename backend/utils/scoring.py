def score_image(detected_labels, user_tags):
    """
    detected_labels: list[str]
    user_tags: list[str]
    """

    matched = []
    missing = []

    for tag in user_tags:
        if any(tag.lower() in label.lower() for label in detected_labels):
            matched.append(tag)
        else:
            missing.append(tag)

    score = 0
    if user_tags:
        score = int((len(matched) / len(user_tags)) * 100)

    return {
        "score": score,
        "matched_tags": matched,
        "missing_tags": missing,
        "detected_labels": detected_labels
    }
