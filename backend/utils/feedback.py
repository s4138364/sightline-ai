import json
import os

FEEDBACK_FILE = "feedback.json"


def _load():
    if not os.path.exists(FEEDBACK_FILE):
        return {}
    with open(FEEDBACK_FILE, "r") as f:
        return json.load(f)


def _save(data):
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(data, f, indent=2)


def record_feedback(tag: str, accepted: bool):
    data = _load()

    if tag not in data:
        data[tag] = {
            "accepted": 0,
            "rejected": 0
        }

    if accepted:
        data[tag]["accepted"] += 1
    else:
        data[tag]["rejected"] += 1

    _save(data)


def get_threshold_for_tag(tag: str):
    data = _load()
    stats = data.get(tag)

    if not stats:
        return None

    total = stats["accepted"] + stats["rejected"]
    if total == 0:
        return None

    acceptance_rate = stats["accepted"] / total

    # Adaptive threshold
    if acceptance_rate > 0.8:
        return 0.2
    if acceptance_rate < 0.3:
        return 0.4

    return 0.25
