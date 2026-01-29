def score_image(detected_labels, user_tags):
    detected_set = set(detected_labels)
    user_set = set(user_tags)

    matched = sorted(detected_set & user_set)
    missing = sorted(user_set - detected_set)

    score = int((len(matched) / len(user_set)) * 100) if user_set else 0

    return {
        "score": score,
        "matched_tags": matched,
        "missing_tags": missing,
        "detected_labels": sorted(detected_set)
    }
