import json
from pathlib import Path

THRESHOLD_FILE = Path("backend/data/thresholds.json")

DEFAULT_THRESHOLDS = {
    "generic": 0.45,
    "color": 0.50,
    "object": 0.55,
    "specific_animal": 0.65
}


def load_thresholds():
    if THRESHOLD_FILE.exists():
        with open(THRESHOLD_FILE, "r") as f:
            return json.load(f)
    return DEFAULT_THRESHOLDS.copy()


def save_thresholds(thresholds):
    THRESHOLD_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(THRESHOLD_FILE, "w") as f:
        json.dump(thresholds, f, indent=2)


def apply_feedback(category: str, was_correct: bool, step: float = 0.02):
    thresholds = load_thresholds()

    current = thresholds.get(category, DEFAULT_THRESHOLDS.get(category, 0.55))

    if was_correct:
        # slightly relax
        new_value = max(0.3, current - step)
    else:
        # tighten
        new_value = min(0.9, current + step)

    thresholds[category] = round(new_value, 3)
    save_thresholds(thresholds)

    return thresholds
