import cv2
import numpy as np
from insightface.app import FaceAnalysis

app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
app.prepare(ctx_id=0, det_size=(640, 640))

def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def get_face_embedding(img_path):
    img = cv2.imread(img_path)
    faces = app.get(img)
    if len(faces) == 0:
        return None
    return faces[0].normed_embedding 