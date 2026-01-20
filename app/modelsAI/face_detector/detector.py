from mtcnn import MTCNN
import cv2
import numpy as np

detector = MTCNN()

def detect_and_crop_faces(img, margin=0.25):
    results = detector.detect_faces(img)
    faces = []

    for res in results:
        x, y, w, h = res["box"]
        x, y = max(0, x), max(0, y)

        mx = int(w * margin)
        my = int(h * margin)

        x1 = max(0, x - mx)
        y1 = max(0, y - my)
        x2 = min(img.shape[1], x + w + mx)
        y2 = min(img.shape[0], y + h + my)

        face = img[y1:y2, x1:x2]
        faces.append(face)

    return faces