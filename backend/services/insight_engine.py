from typing import List
from services.model_inference import run_model


def generate_insight(tags: List[str]) -> dict:
    joined_tags = ", ".join(tags)

    model_result = run_model(joined_tags)
    confidence = model_result["confidence"]

    if confidence > 0.85:
        insight = "High confidence visual quality indicators detected."
    elif confidence > 0.6:
        insight = "Moderate visual quality signals present."
    else:
        insight = "Weak visual signals. Consider improving composition."

    return {
        "score": confidence,
        "insight": insight
    }
