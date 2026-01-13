import cv2
from detector import FaceDetector

img = cv2.imread("./app/models/face_detector/test.jpg")
print("Image shape:", img.shape)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

detector = FaceDetector()
faces = detector.detect(img)
for face in faces:
    x1, y1, x2, y2 = face["bbox"]
    confidence = face["confidence"]
    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
    cv2.putText(img, f'Face: {confidence:.2f}', (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)
cv2.imshow("Face Detection", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(faces)