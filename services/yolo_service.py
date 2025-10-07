from fastapi import UploadFile, HTTPException
from io import BytesIO
from pathlib import Path
from PIL import Image
from ultralytics import YOLO
import os

# 모델 파일 경로 설정 및 체크
def get_yolo_model_path() -> Path:
    # path = Path("models_storage\\yolov11n.pt")
    path = Path("models_storage")
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
            _model = YOLO("yolo11n.yaml")
            _model = YOLO("models_storage/yolo11n.pt")
            print("YOLO model loaded successfully.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to load YOLO model: {e}")
    return _model

# async def infer_yolo(file: UploadFile) -> dict:
#     # 모델 로드
#     model = get_model()
#     # 이미지 로드
#     content = await file.read()
#     img = Image.open(BytesIO(content)).convert("RGB")
#     try:
#         results = model.predict(img)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"YOLO inference error: {e}")
#     res = results[0]
#     predictions = []
#     for box, cls, conf in zip(res.boxes.xyxy, res.boxes.cls, res.boxes.conf):
#         predictions.append({
#             "bbox": box.tolist(),
#             "class_id": int(cls.item()),
#             "confidence": float(conf.item())
#         })
#     print(f"YOLO inference completed. Predictions: {predictions}")
#     return {"filename": file.filename, "predictions": predictions}
from typing import Optional
import uuid
import cv2
BASE_DIR = Path(__file__).resolve().parents[1] if (Path(__file__).name != "main.py") else Path.cwd()
MODELS_DIR = BASE_DIR / "models_storage"
STATIC_OUT_DIR = BASE_DIR / "static" / "yolo_out"
STATIC_OUT_DIR.mkdir(parents=True, exist_ok=True)
async def infer_yolo(
    file: UploadFile,
    conf: Optional[float] = None,
    iou: Optional[float] = None,
    imgsz: Optional[int] = None,
) -> dict:

    """
    업로드된 이미지에 대해 YOLO 탐지 수행.
    결과(바운딩박스 리스트)와 함께 박스/라벨이 그려진 시각화 이미지를 생성/저장하여 경로를 반환.
    """
    model = get_model()

    # 이미지 로드
    content = await file.read()
    try:
        img = Image.open(BytesIO(content)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {e}")

    # 파라미터 기본값
    conf = 0.25 if conf is None else conf
    iou = 0.45 if iou is None else iou
    imgsz = 640  if imgsz is None else imgsz

    # 추론
    try:
        results = model.predict(
            img,
            conf=conf,
            iou=iou,
            imgsz=imgsz,
            save=False,
            verbose=False
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"YOLO inference error: {e}")

    res = results[0]

    # 예측값 정리
    predictions = []
    if res.boxes is not None:
        for box, cls, confv in zip(res.boxes.xyxy, res.boxes.cls, res.boxes.conf):
            predictions.append({
                "bbox": [float(v) for v in box.tolist()],
                "class_id": int(cls.item()),
                "confidence": float(confv.item()),
                "name": res.names.get(int(cls.item()), str(int(cls.item()))) if hasattr(res, "names") else str(int(cls.item()))
            })

    # 박스/라벨 오버레이 이미지 생성 및 저장
    vis_img = res.plot()  # numpy ndarray (BGR)
    out_name = f"{uuid.uuid4().hex}.jpg"
    out_path = STATIC_OUT_DIR / out_name
    cv2.imwrite(str(out_path), vis_img)

    # 정적 경로로 접근할 수 있는 URL (main.py에서 /static 마운트되어 있어야 함)
    vis_relurl = f"/static/yolo_out/{out_name}"

    result_payload = {
        "filename": file.filename,
        "params": {"conf": conf, "iou": iou, "imgsz": imgsz},
        "predictions": predictions,
        "counts": {"detections": len(predictions)},
        "visualization": vis_relurl,
    }
    print(f"YOLO inference completed. Dets={len(predictions)} -> {vis_relurl}")
    return result_payload
