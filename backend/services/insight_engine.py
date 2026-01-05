from typing import List
from utils.scoring import score_tags


def generate_insight(tags: List[str]) -> dict:
    score = score_tags(tags)

    if score > 0.7:
        insight = "Strong visual composition with clear subject separation."
    elif score > 0.4:
        insight = "Decent image, but composition could have been improved."
    else:
        insight = "Weak visual structure. Consider reframing or simplifying."

    return {
        "score": score,
        "insight": insight
    }