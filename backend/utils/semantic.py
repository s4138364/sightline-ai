from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load once (VERY important)
model = SentenceTransformer("all-MiniLM-L6-v2")


def compute_similarity(detected_labels, user_tags):
    """
    Computes semantic similarity between detected labels and user tags.

    Returns:
        dict[tag] = max cosine similarity score
    """
    if not detected_labels or not user_tags:
        return {}

    label_embeddings = model.encode(detected_labels)
    tag_embeddings = model.encode(user_tags)

    similarity_matrix = cosine_similarity(tag_embeddings, label_embeddings)

    similarities = {}

    for i, tag in enumerate(user_tags):
        similarities[tag] = float(similarity_matrix[i].max())

    return similarities
