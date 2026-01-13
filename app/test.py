import cv2
from modelsAI.face_detector.detector import FaceDetector
from modelsAI.facenet.model import get_embedding
import numpy as np
from core.mongodb import residents_collection as users_col
face_detector = FaceDetector()
cap = cv2.VideoCapture(0)

FRAME_SKIP = 3
frame_id = 0
faces_cache = []
next_id = 1
SIM_THRESHOLD = 0.7
embeddings_list = []
user_ids = []

for user in users_col.find({}):
    print("Loading user:", user["_id"])
    for emb in user.get("embeddings", []):
        vec = emb.get("vector")
        if vec is None:
            continue
        print("Embedding type:", type(vec), len(vec) if hasattr(vec, "__len__") else "N/A")
        if isinstance(vec, (list, np.ndarray)) and len(vec) == 512:
            embeddings_list.append(vec)
            user_ids.append(user["_id"])

if len(embeddings_list) > 0:
    db_embeddings = np.stack([np.array(e, dtype=np.float32) for e in embeddings_list], axis=0)
else:
    db_embeddings = np.zeros((0, 512), dtype=np.float32)

def crop_face_square(frame, bbox, margin=0.2):
    x1, y1, x2, y2 = map(int, bbox)
    h, w, _ = frame.shape

    bw = x2 - x1
    bh = y2 - y1
    size = int(max(bw, bh) * (1 + margin))

    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2

    x1 = max(0, cx - size // 2)
    y1 = max(0, cy - size // 2)
    x2 = min(w, cx + size // 2)
    y2 = min(h, cy + size // 2)

    face = frame[y1:y2, x1:x2]
    if face.size == 0:
        return None

    return face
def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def identify_user_vectorized(embedding, db_embeddings, user_ids, threshold=0.7):
    if len(db_embeddings) == 0:
        return None, 0.0

    embedding = np.array(embedding, dtype=np.float32)
    db_embeddings = np.array(db_embeddings, dtype=np.float32)

    # cosine similarity vì đã normalize
    sims = np.dot(db_embeddings, embedding)

    best_idx = np.argmax(sims)
    best_sim = sims[best_idx]

    if best_sim >= threshold:
        return user_ids[best_idx], float(best_sim)
    else:
        return None, float(best_sim)
img1 = cv2.imread("./app/test1.jpg")  # người A
img2 = cv2.imread("./app/anhchinhdien.jpg")  # người B (hoặc A ảnh khác)

assert img1 is not None and img2 is not None

faces1 = face_detector.detect(img1)
faces2 = face_detector.detect(img2)

assert len(faces1) > 0 and len(faces2) > 0

face1 = crop_face_square(img1, faces1[0]["bbox"])
face2 = crop_face_square(img2, faces2[0]["bbox"])

cv2.imwrite("debug_face1.jpg", face1)
cv2.imwrite("debug_face2.jpg", face2)

emb1 = get_embedding(face1)
emb2 = get_embedding(face2)

print("emb1 shape:", emb1.shape, "std:", emb1.std())
print("emb2 shape:", emb2.shape, "std:", emb2.std())

print("L2 distance:", np.linalg.norm(emb1 - emb2))
print("Cosine similarity:", cosine_sim(emb1, emb2))