from fastapi import UploadFile, HTTPException
from io import BytesIO
from pathlib import Path
from PIL import Image
from ultralytics import YOLO

# 모델 파일 경로 설정 및 체크
def get_yolo_model_path() -> Path:
    path = Path("models_storage\\yolov11n.pt")
    if not path.exists():
        without_model = Path("models_storage\\")
        model = YOLO(without_model+"yolo11n.yaml")
        model = YOLO(without_model+"yolo11n.pt")
        # raise HTTPException(status_code=500, detail=f"YOLO model file not found: {path}")
    return model

# 지연 로드 방식으로 모델 로드
_model = None

def get_model() -> YOLO:
    global _model
    if _model is None:
        model = get_yolo_model_path()
        try:
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to load YOLO model: {e}")
    return _model

async def infer_yolo(file: UploadFile) -> dict:
    # 모델 로드
    model = get_model()
    # 이미지 로드
    content = await file.read()
    img = Image.open(BytesIO(content)).convert("RGB")
    try:
        results = model.predict(img)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"YOLO inference error: {e}")
    res = results[0]
    predictions = []
    for box, cls, conf in zip(res.boxes.xyxy, res.boxes.cls, res.boxes.conf):
        predictions.append({
            "bbox": box.tolist(),
            "class_id": int(cls.item()),
            "confidence": float(conf.item())
        })
    return {"filename": file.filename, "predictions": predictions}