ANIMAL_CLASSES = {
    "dog", "cat", "horse", "cow", "sheep", "bird", "fish"
}


def score_image(
    detected_labels,
    user_tags,
    semantic_similarities,
    confidence_threshold=0.4
):
    matched = []
    missing = []

    detected_text = " ".join(detected_labels)

    for tag in user_tags:
        similarity = semantic_similarities.get(tag, 0)

        # Hard block: mutually exclusive animals
        if tag in ANIMAL_CLASSES:
            for animal in ANIMAL_CLASSES:
                if animal != tag and animal in detected_text:
                    missing.append(tag)
                    break
            else:
                if similarity >= confidence_threshold:
                    matched.append(tag)
                else:
                    missing.append(tag)
        else:
            if similarity >= confidence_threshold:
                matched.append(tag)
            else:
                missing.append(tag)

    score = int((len(matched) / len(user_tags)) * 100) if user_tags else 0

    return {
        "score": score,
        "matched_tags": matched,
        "missing_tags": missing,
        "semantic_similarities": semantic_similarities,
        "confidence_threshold": confidence_threshold
    }
