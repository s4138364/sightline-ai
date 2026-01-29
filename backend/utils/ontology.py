ONTOLOGY = {
    "cat": ["animal", "pet"],
    "dog": ["animal", "pet"],
    "car": ["vehicle"],
}

def expand_concepts(labels):
    expanded = set()

    for label in labels:
        expanded.add(label)
        if label in ONTOLOGY:
            expanded.update(ONTOLOGY[label])

    return expanded
