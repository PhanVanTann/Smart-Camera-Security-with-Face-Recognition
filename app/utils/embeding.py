import cv2
import numpy as np
from modelsAI.insightFace.model import app as insightface_model_app

def get_embedding_from_image(img_path):
    # Đọc ảnh
    nparr = np.fromfile(img_path, dtype=np.uint8) 
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        print(f"Invalid image: {img_path}")
        return None

    faces = insightface_model_app.get(img)  
    if len(faces) == 0:
        print(f"No face detected: {img_path}")
        return None

    # Chọn face lớn nhất
    face = max(faces, key=lambda f: (f.bbox[2]-f.bbox[0])*(f.bbox[3]-f.bbox[1]))
    embedding = face.normed_embedding.tolist()  
    return embedding