from fastapi import UploadFile
from io import BytesIO
from PIL import Image
import pytesseract

async def infer_ocr(file: UploadFile) -> dict:
    data = await file.read()
    img = Image.open(BytesIO(data)).convert("RGB")
    text = pytesseract.image_to_string(img, lang='eng')
    conf = len(text) / 1000.0
    return {"filename": file.filename, "text": text.strip(), "confidence": round(conf, 2)}