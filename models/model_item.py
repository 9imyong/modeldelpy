from enum import Enum
from pydantic import BaseModel

class ModelType(str, Enum):
    CLASSIFICATION = "classification"
    OCR            = "ocr"
    DETECTION      = "detection"

class ModelItem(BaseModel):
    id: int
    type: ModelType    # classification, ocr, detection
    name: str
    version: str