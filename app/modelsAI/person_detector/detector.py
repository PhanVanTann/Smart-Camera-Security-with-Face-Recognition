from ultralytics import YOLO
import cv2

class PersonDetector:
    def __init__(self):
        self.model = YOLO("yolov8l.pt")

    def detect(self, frame):
        results = self.model(frame, conf=0.5, classes=[0])
        detections = []
        for result in results:
            for box in result.boxes:
                cls_id = int(box.cls[0])
                if cls_id == 0:  
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = float(box.conf[0])
                    detections.append({
                        "bbox": (x1, y1, x2, y2),
                        "confidence": conf
                    })
        return detections
        