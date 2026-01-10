from pydantic import BaseModel
from typing import List

class ImageInsightResponse(BaseModel):
    score: int
    matched_tags: List[str]
    missing_tags: List[str]
    detected_labels: List[str]
