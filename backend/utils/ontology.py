# Simple ontology graph
ONTOLOGY = {
    "cat": ["animal"],
    "dog": ["animal"],
    "animal": [],
}

def normalize_label(label: str) -> str:
    return label.lower().strip()

def expand_concepts(labels):
    expanded = set(labels)

    for lbl in labels:
        parents = ONTOLOGY.get(lbl, [])
        for p in parents:
            expanded.add(p)

    return list(expanded)
