from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap
import cv2
import os

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
class FaceWorker(QThread):
    update_frame_signal = pyqtSignal(object)

    def __init__(self, cap, face_db, threshold):
        super().__init__()
        self.cap = cap
        self.face_db = face_db
        self.threshold = threshold
        self.running = True

    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue

            # --- xử lý mặt ---
            faces = app.get(frame) 
            results = []
            for face in faces:
                x1, y1, x2, y2 = map(int, face.bbox)
                cropped_face = cropImage(frame, (x1, y1, x2, y2))
                has_mask = segment_face(cropped_face)

                emb = face.normed_embedding
                name = "UNKNOWN"
                address = "N/A"
                age = "N/A"
                best_score = 0
                for k, db in self.face_db.items():
                    score = cosine_sim(emb, db["embedding_vector"])
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
                    "mask": has_mask,
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
        self.worker = FaceWorker(self.cap, face_db, THRESHOLD)  # truyền face_db
        self.worker.update_frame_signal.connect(self.display_frame)
        self.worker.start()

    def display_frame(self, data):
        frame, faces = data
        # vẽ bounding box + text
        for f in faces:
            print("ffff",f)
            x1, y1, x2, y2 = f["bbox"]
            color = (0, 255, 0) if f["name"] != "UNKNOWN" else (0, 0, 255)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            if f["mask"]:
                cv2.putText(frame, "Deo khau trang", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                continue
            cv2.putText(frame, f'{f["name"]} - {f["age"]}T ({f["score"]:.2f})', (x1, y1-40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            cv2.putText(frame, f'Address: {f["address"]}', (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

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