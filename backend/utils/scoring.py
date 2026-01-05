def score_tags(tags: list[str]) -> float:
    if not tags:
        return 0.0

    positive_tags = {"symmetry", "leading lines", "sharp focus", "rule of thirds"}
    matches = sum(1 for tag in tags if tag.lower() in positive_tags)

    return min(1.0, matches / len(positive_tags))