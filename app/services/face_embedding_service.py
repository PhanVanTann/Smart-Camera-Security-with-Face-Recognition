import cv2
import numpy as np
from app.modelsAI.INSIGHTFACE.embeding import get_face_embedding

def crop_face_with_margin(img, bbox, margin=0.3):
    x1, y1, x2, y2 = map(int, bbox)
    h, w, _ = img.shape
    bw, bh = x2 - x1, y2 - y1
    size = int(max(bw, bh) * (1 + margin))
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
    x1 = max(0, cx - size // 2)
    y1 = max(0, cy - size // 2)
    x2 = min(w, cx + size // 2)
    y2 = min(h, cy + size // 2)
    return img[y1:y2, x1:x2].copy()

def get_face_embedding_facenet(img_bytes, model_app):
    # Decode ảnh
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Invalid image")

    # Detect face
    faces = model_app.get(img)
    if len(faces) == 0:
        raise ValueError("No face detected")

    # Chọn mặt lớn nhất
    face = max(faces, key=lambda f: (f.bbox[2]-f.bbox[0])*(f.bbox[3]-f.bbox[1]))

    # Crop với margin
    x1, y1, x2, y2 = map(int, face.bbox)
    face_img = crop_face_with_margin(img, (x1, y1, x2, y2), margin=0.3)

    # Lấy embedding trực tiếp từ numpy array
    embedding = get_face_embedding(face_img, model_app)

    if embedding is None:
        raise ValueError("Failed to generate embedding from cropped face")

    return embedding