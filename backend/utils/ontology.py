# backend/utils/ontology.py

# Simple ontology graph
ONTOLOGY = {
    "cat": {"animal", "mammal"},
    "dog": {"animal", "mammal"},
    "bird": {"animal"},
    "car": {"vehicle"},
    "truck": {"vehicle"},
}

def normalize_label(label: str) -> str:
    """
    Reduce model labels like:
    'egyptian cat' -> 'cat'
    'tabby, tabby cat' -> 'cat'
    """
    label = label.lower()

    if "cat" in label:
        return "cat"
    if "dog" in label:
        return "dog"
    if "bird" in label:
        return "bird"
    if "car" in label:
        return "car"
    if "truck" in label:
        return "truck"

    return label


def expand_concepts(detected_labels: list[str]) -> list[str]:
    """
    Expand detected labels using ontology
    """
    expanded = set()

    for label in detected_labels:
        base = normalize_label(label)
        expanded.add(base)

        if base in ONTOLOGY:
            expanded.update(ONTOLOGY[base])

    return list(expanded)
