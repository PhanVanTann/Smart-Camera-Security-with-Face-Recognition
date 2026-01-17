import cv2
import numpy as np
from insightface.app import FaceAnalysis
from modelsAI.INSIGHTFACE.model import cosine_sim, get_face_embedding
from  core.mongodb import residents_collection 
from modelsAI.INSIGHTFACE.model import app 

cap = cv2.VideoCapture(0)  

THRESHOLD = 0.6


face_db = {}
for user in residents_collection.find({}):
    name = user.get("last_name", "N/A") + " " + user.get("first_name", "N/A")
    print("Checking user:", name)
    for emb in user.get("embeddings", []):
        vec = emb.get("vector")
        if vec is None:
            continue
        emb_A = np.array(vec, dtype=np.float32)
        face_db[name] = emb_A

while True:
    ret, frame = cap.read()
    if not ret:
        break

    faces = app.get(frame)

    for face in faces:
        emb = face.normed_embedding 

        name = "UNKNOWN"
        best_score = 0

        for k, db_emb in face_db.items():
            score = cosine_sim(emb, db_emb)
            if score > best_score:
                best_score = score
                name = k

        if best_score < THRESHOLD:
            name = "UNKNOWN"

        x1, y1, x2, y2 = map(int, face.bbox)

        if name == "UNKNOWN":
            color = (0, 0, 255)
        else:
            color = (0, 255, 0)
        cv2.rectangle(frame, (x1,y1), (x2,y2), color, 2)
        cv2.putText(
            frame,
            f"{name} ({best_score:.2f})",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2
        )

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()