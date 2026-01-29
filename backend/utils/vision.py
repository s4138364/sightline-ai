from PIL import Image
import io

def detect_labels(image_bytes: bytes):
    """
    Day 30 stub vision system.
    Ensures pipeline works end-to-end.
    """

    # Validate image
    Image.open(io.BytesIO(image_bytes))

    # Mock labels (controlled + predictable)
    return [
        "cat",
        "pet"
    ]
