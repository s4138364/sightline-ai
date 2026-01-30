from PIL import Image
import io

def detect_labels(image_bytes: bytes):
    Image.open(io.BytesIO(image_bytes))

    return [
        "cat",
        "pet"
    ]
