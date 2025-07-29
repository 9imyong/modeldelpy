from fastapi import APIRouter, Request, Form, File, UploadFile, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from services.common_service import get_item
from services.ocr_service import infer_ocr

router = APIRouter(prefix="/models/ocr", tags=["OCR"])
templates = Jinja2Templates(directory="templates")

@router.get("/{id}", include_in_schema=False)
async def detail(request: Request, id: int):
    item = get_item(id)
    if not item or item.type.value != "ocr":
        raise HTTPException(status_code=404)
    return templates.TemplateResponse("ocr_detail.html", {"request": request, "item": item})

@router.post("/infer", include_in_schema=False)
async def infer(request: Request, id: int = Form(...), file: UploadFile = File(...)):
    result = await infer_ocr(file)
    return RedirectResponse(url=f"/models/ocr/{id}?result={result}", status_code=303)
