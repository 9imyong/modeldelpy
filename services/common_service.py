from typing import List, Optional
from models.model_item import ModelItem, ModelType

# 메모리 기반 저장소 (예시)
_items: List[ModelItem] = []
_next_id = 1

def list_items() -> List[ModelItem]:
    return _items

def add_item(type: ModelType, name: str, version: str) -> ModelItem:
    global _next_id
    item = ModelItem(id=_next_id, type=type, name=name, version=version)
    _items.append(item)
    _next_id += 1
    return item

def get_item(item_id: int) -> Optional[ModelItem]:
    return next((m for m in _items if m.id == item_id), None)

def list_by_type(model_type: ModelType) -> List[ModelItem]:
    return [m for m in _items if m.type == model_type]

def delete_item(item_id: int) -> bool:
    global _items
    for i, itm in enumerate(_items):
        if itm.id == item_id:
            del _items[i]
            return True
    return False