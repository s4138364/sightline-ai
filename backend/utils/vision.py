import time

def run_vision_model(image_bytes):
    start = time.time()

    # Fake predictions for testing
    predictions = [
        {"label": "egyptian cat", "confidence": 0.55},
        {"label": "tabby cat", "confidence": 0.28},
        {"label": "tiger cat", "confidence": 0.08},
    ]

    return predictions, time.time() - start
