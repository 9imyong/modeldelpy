from pydantic import BaseModel
from enum import Enum

class ModelType(str, Enum):
    CLASSIFICATION = "classification"
    OCR            = "ocr"
    DETECTION      = "detection"

class ModelItem(BaseModel):
    id: int
    type: ModelType
    name: str
    version: str