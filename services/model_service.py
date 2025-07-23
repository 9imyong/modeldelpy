from typing import List, Optional, Any
from models.model_item import ModelItem
from fastapi import UploadFile

_items: List[ModelItem] = []
_next_id = 1

def list_items() -> List[ModelItem]:
    return _items

def add_item(type: str, name: str, version: str) -> ModelItem:
    global _next_id
    item = ModelItem(id=_next_id, type=type, name=name, version=version)
    _items.append(item)
    _next_id += 1
    return item

def delete_item(item_id: int) -> bool:
    for i, itm in enumerate(_items):
        if itm.id == item_id:
            del _items[i]
            return True
    return False

async def infer_model(item_id: int, file: UploadFile) -> dict:
    result = {
        "model_id": item_id,
        "filename": file.filename,
        "prediction": f"pred_{file.filename}",
        "confidence": 0.85
    }
    return result