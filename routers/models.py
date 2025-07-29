from fastapi import APIRouter, HTTPException, Request, Form, File, UploadFile
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List, Optional, Dict, Any
from services.common_service import list_items, add_item, delete_item, list_by_type, get_item
from models.model_item import ModelItem, ModelType

router = APIRouter(prefix="/models", tags=["Models"])
templates = Jinja2Templates(directory="templates")

@router.get("/", include_in_schema=False)
async def models_page(request: Request):
    items: List[ModelItem] = list_items()
    return templates.TemplateResponse("dashboard.html", {"request": request, "items": items})

@router.post("/add", include_in_schema=False)
async def models_add(
    request: Request,
    type: ModelType = Form(...),
    name: str = Form(...),
    version: str = Form(...)
):
    add_item(type, name, version)
    return RedirectResponse(url="/models/", status_code=303)

@router.post("/delete", include_in_schema=False)
async def models_delete(request: Request, id: int = Form(...)):
    if not delete_item(id):
        raise HTTPException(status_code=404, detail="Item not found")
    return RedirectResponse(url="/models/", status_code=303)

@router.get("/type/{model_type}", include_in_schema=False)
async def models_by_type(request: Request, model_type: ModelType):
    items = list_by_type(model_type)
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "items": items, "filter": model_type.value}
    )

@router.get("/{id}", include_in_schema=False)
async def model_detail(request: Request, id: int, result: Optional[Dict[str, Any]] = None):
    item = get_item(id)
    if not item:
        raise HTTPException(status_code=404, detail="Model not found")
    return templates.TemplateResponse(
        "model_detail.html",
        {"request": request, "item": item, "result": result}
    )

@router.post("/infer", include_in_schema=False)
async def models_infer(
    request: Request,
    id: int = Form(...),
    file: UploadFile = File(...)
):
    item = get_item(id)
    if not item:
        raise HTTPException(status_code=404, detail="Model not found")
    if item.type == ModelType.OCR:
        from services.ocr_service import infer_ocr
        result = await infer_ocr(file)
    elif item.type == ModelType.DETECTION:
        from services.yolo_service import infer_yolo
        result = await infer_yolo(file)
    else:
        result = {"error": "Unsupported model type"}
    return RedirectResponse(url=f"/models/{id}?result={result}", status_code=303)