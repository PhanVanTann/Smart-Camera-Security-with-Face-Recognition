import cv2
import numpy as np
from modelsAI.INSIGHTFACE.model import cosine_sim
from  core.mongodb import residents_collection 
from modelsAI.INSIGHTFACE.model import app 
from dotenv import load_dotenv
from services.usersService import usersService
import os
load_dotenv()
usersService = usersService()
cap = cv2.VideoCapture(0)  

THRESHOLD = float(os.getenv("THRESHOLD", 0.7))

face_db = {}
users = usersService.getListUsers()
for name, user_info in users.items():
    face_db[name] = user_info

while True:
    ret, frame = cap.read()
    if not ret:
        break

    faces = app.get(frame)

    for face in faces:
        emb = face.normed_embedding 

        name = "UNKNOWN"
        address = "N/A"
        best_score = 0
        x1, y1, x2, y2 = map(int, face.bbox)
        
        for k, db in face_db.items():
            score = cosine_sim(emb, db["embedding_vector"])
            if score > best_score:
                best_score = score
                name = k
                address = db["address"]
        if best_score < THRESHOLD:
            name = "UNKNOWN"
            address = "N/A"

       

        if name == "UNKNOWN":
            color = (0, 0, 255)
        else:
            color = (0, 255, 0)
        cv2.rectangle(frame, (x1,y1), (x2,y2), color, 2)
        cv2.putText(
            frame,
            f"Address: {address}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2
        )
        cv2.putText(
            frame,
            f"{name} ({best_score:.2f})",
            (x1, y1 - 40),
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