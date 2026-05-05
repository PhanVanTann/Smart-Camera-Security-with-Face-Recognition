from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap
import cv2
import os
from collections import deque

from modelsAI.unet.segmentaion import segment_face
from modelsAI.insightFace.model import cosine_sim, app
from services.usersService import usersService
from utils.cropImage import cropImage
from dotenv import load_dotenv
load_dotenv()
THRESHOLD = float(os.getenv("THRESHOLD", 0.7))
from PyQt6.QtCore import QThread, pyqtSignal
import time
usersService = usersService()

def iou(boxA, boxB):
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])

        inter = max(0, xB-xA) * max(0, yB-yA)
        areaA = (boxA[2]-boxA[0])*(boxA[3]-boxA[1])
        areaB = (boxB[2]-boxB[0])*(boxB[3]-boxB[1])
        union = areaA + areaB - inter

        return inter / union if union > 0 else 0
class FaceWorker(QThread):
    update_frame_signal = pyqtSignal(object)

    def __init__(self, cap, face_db, threshold):
        super().__init__()
        self.cap = cap
        self.face_db = face_db
        self.threshold = threshold
        self.running = True
        self.face_id_counter = 0
        self.tracked_faces = {}

    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue
                
            # xử lý mặt 
            faces = app.get(frame) 
            results = []
            for face in faces:
                x1, y1, x2, y2 = map(int, face.bbox)   
                cropped_face = cropImage(frame, (x1, y1, x2, y2))      
                matched_id = None
                for fid, data in self.tracked_faces.items():
                    if iou(data["bbox"], (x1,y1,x2,y2)) > 0.5:
                        matched_id = fid
                        break

                if matched_id is None:
                    matched_id = self.face_id_counter
                    self.face_id_counter += 1
                    self.tracked_faces[matched_id] = {
                        "bbox": (x1,y1,x2,y2),
                        "mask_history": deque(maxlen=10)
                    }

                self.tracked_faces[matched_id]["bbox"] = (x1,y1,x2,y2)

                has_mask = segment_face(cropped_face)
                print("has_mák",has_mask)

                self.tracked_faces[matched_id]["mask_history"].append(1 if has_mask else 0)
                final_mask = sum(self.tracked_faces[matched_id]["mask_history"]) >= 7

                emb = face.normed_embedding
                name = "UNKNOWN"
                address = "N/A"
                age = "N/A"
                best_score = 0
                for k, db in self.face_db.items():
                    for db_emb in db["embeddings"]:
                        score = cosine_sim(emb, db_emb)
                        if score > best_score:
                            best_score = score
                            name = k
                            address = db["address"]
                            age = db["age"]
                if best_score < self.threshold:
                    name = "UNKNOWN"
                    address = "N/A"
                    age = "N/A"
                results.append({
                    "bbox": (x1, y1, x2, y2),
                    "mask": final_mask,
                    "name": name,
                    "address": address,
                    "age":age,
                    "score": best_score
                })
            self.update_frame_signal.emit((frame, results))
            time.sleep(0.05)  

class CameraWidget(QFrame):
    def __init__(self, width=640, height=480):
        super().__init__()
        self.width = width
        self.height = height

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.video_label = QLabel()
        self.video_label.setFixedSize(width, height)
        self.video_label.setStyleSheet("background-color: black;")
        layout.addWidget(self.video_label)

        self.btn_stop = QPushButton("Stop Camera")
        self.btn_stop.clicked.connect(self.stop_camera)
        layout.addWidget(self.btn_stop)

        self.cap = cv2.VideoCapture(0)
        face_db = {}
        users = usersService.getListUsers()
        for name, user_info in users.items():
            face_db[name] = user_info
        print("facedb",face_db)
        self.worker = FaceWorker(self.cap, face_db, THRESHOLD)  
        self.worker.update_frame_signal.connect(self.display_frame)
        self.worker.start()

    def display_frame(self, data):
        frame, faces = data
        # vẽ bounding box + text
        for f in faces:
            x1, y1, x2, y2 = f["bbox"]
            if f["mask"]:
                color = (0, 0, 255)
                label = "Deo khau trang"
            else:
                color = (0, 255, 0) if f["name"] != "UNKNOWN" else (0, 0, 255)
                label = f'{f["name"]} - {f["age"]}T'
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (self.width, self.height))
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        qimg = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qimg))

    def stop_camera(self):
        self.worker.running = False
        self.worker.quit()
        self.worker.wait()
        self.cap.release()
        self.video_label.clear()