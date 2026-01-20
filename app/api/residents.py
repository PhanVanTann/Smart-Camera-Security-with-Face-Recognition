from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.core.mongodb import residents_collection
from bson import ObjectId
from app.schemas.residentsSchema import ResidentCreate
from app.modelsAI.INSIGHTFACE.model import app as insightface_model_app
import cv2
import numpy as np


router = APIRouter(prefix="/residents", tags=["Residents"])


@router.post("/")
async def create_resident(
    resident: ResidentCreate
):
    print( resident)
    result = residents_collection.insert_one(resident.dict())
    return {
        "id": str(result.inserted_id),
        "msg": "Resident created & embedding added"
    }

@router.post("/{resident_id}/face")
async def upload_face(
    resident_id: str,
    image: UploadFile = File(...),
    angle: str = Form(...),      # frontal / left / right
    mask: bool = Form(...),      # true / false
    distance: str = Form(...)    # near / medium / far
):
    img_bytes = await image.read()
    nparr = np.frombuffer(img_bytes, np.uint8)
     
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise HTTPException(status_code=400, detail="Invalid image")

    faces = insightface_model_app.get(img)
    if len(faces) == 0:
        raise HTTPException(status_code=400, detail="No face detected")

    # Chọn mặt lớn nhất
    face = max(faces, key=lambda f: (f.bbox[2]-f.bbox[0])*(f.bbox[3]-f.bbox[1]))

    # Lấy embedding trực tiếp, không cần crop lại
    embedding = face.normed_embedding.tolist()

    result = residents_collection.update_one(
        {"_id": ObjectId(resident_id)},
        { "$push": {
                "embeddings": {
                    "vector": embedding,
                    "angle": angle,        # frontal / left / right
                    "mask": mask,          # true / false
                    "distance": distance   # near / medium / far
                }
            }}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Resident not found")

    return {"message": "Face added successfully"}

@router.get("/get_all")
async def get_residents():
    residents = residents_collection.find()
    return residents
