from fastapi import APIRouter, HTTPException, Request, Form, UploadFile, File, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List, Optional
from services.model_service import list_items, add_item, delete_item, infer_model
from models.model_item import ModelItem

router = APIRouter(tags=["models"])
templates = Jinja2Templates(directory="templates")

@router.get("/models", include_in_schema=False)
async def models_page(request: Request, result: Optional[dict] = None):
    items: List[ModelItem] = list_items()
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "items": items, "result": result}
    )

@router.post("/models/add", include_in_schema=False)
async def models_add(
    request: Request,
    type: str = Form(...),
    name: str = Form(...),
    version: str = Form(...)
):
    if not (type.strip() and name.strip() and version.strip()):
        raise HTTPException(status_code=400, detail="All fields are required")
    add_item(type, name, version)
    return RedirectResponse(url="/models", status_code=303)

@router.post("/models/delete", include_in_schema=False)
async def models_delete(request: Request, id: int = Form(...)):
    if not delete_item(id):
        raise HTTPException(status_code=404, detail="Item not found")
    return RedirectResponse(url="/models", status_code=303)

@router.post("/models/infer", include_in_schema=False)
async def models_infer(
    request: Request,
    id: int = Form(...),
    file: UploadFile = File(...)
):
    # 모델 추론 호출
    inference = await infer_model(id, file)
    return RedirectResponse(url=f"/models?result={inference}", status_code=303)