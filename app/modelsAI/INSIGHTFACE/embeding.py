import cv2
import numpy as np
def get_face_embedding(img,model_app):
    if img is None:
        return None

    faces = model_app.get(img)
    if len(faces) == 0:
        return None

    # Chọn mặt lớn nhất
    face = max(faces, key=lambda f: (f.bbox[2]-f.bbox[0])*(f.bbox[3]-f.bbox[1]))
    emb = face.normed_embedding

    # L2 normalize
    emb = emb / np.linalg.norm(emb)

    return emb.tolist()  # ready để lưu MongoDB