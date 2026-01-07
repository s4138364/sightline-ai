from services.model_inference import analyze_text

def generate_insight(tags: list[str]) -> dict:
    score = analyze_text(tags)

    if score > 0.7:
        insight = "Strong alignment between visual content and intent."
    elif score > 0.4:
        insight = "Moderate relevance detected."
    else:
        insight = "Weak or unclear relevance."

    return {
        "score": score,
        "insight": insight
    }
