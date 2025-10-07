# routers/yolo.py

from fastapi import APIRouter, Request, Form, UploadFile, File, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from services.common_service import get_item
from services.yolo_service import infer_yolo
from models.model_item import ModelType

from services.common_service import list_by_type

router = APIRouter(prefix="/models/yolo", tags=["YOLO"])
templates = Jinja2Templates(directory="templates")

@router.get("/", include_in_schema=False)
async def yolo_list(request: Request):
    # Detection(D#ETECTION) 타입 모델만 필터링
    items = list_by_type(ModelType.DETECTION)
    return templates.TemplateResponse(
        "yolo_detail.html",
        {"request": request, "items": items, "filter": "Detection"}
    )