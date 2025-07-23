from pydantic import BaseModel

class ModelItem(BaseModel):
    id: int
    name: str
    type: str
    version: str