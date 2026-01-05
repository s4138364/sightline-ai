from pydantic import BaseModel
from typing import List



class ImageInsightRequest(BaseModel):
    tags: List[str]


class ImageInsightResponse(BaseModel):
    score: float
    insight: str