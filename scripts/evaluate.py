import os
import cv2
import time
import numpy as np
from insightface.app import FaceAnalysis
from sklearn.metrics import roc_curve, auc, accuracy_score, f1_score
from itertools import combinations
from tqdm import tqdm

print("======================================")
print("  EVALUATE INSIGHTFACE FACE RECOGNITION")
print("======================================")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "..", "dataset")

print("[INFO] Dataset path:", DATASET_DIR)

if not os.path.exists(DATASET_DIR):
    raise FileNotFoundError(f"Dataset not found at {DATASET_DIR}")

# ================= LOAD MODEL =================
print("[1] Loading InsightFace model...")

app = FaceAnalysis(name="buffalo_l")
app.prepare(ctx_id=0, det_size=(640, 640))

# ================= LOAD IMAGES =================
print("[2] Loading images...")

images = []
labels = []

for file in os.listdir(DATASET_DIR):
    if file.lower().endswith((".jpg", ".png", ".jpeg")):
        label = file.split("_")[0]  # person name
        path = os.path.join(DATASET_DIR, file)
        images.append(path)
        labels.append(label)

print(f"[INFO] Total images: {len(images)}")

# ================= EXTRACT EMBEDDINGS + LATENCY =================
print("[3] Extracting face embeddings & measuring latency...")

embeddings = []
valid_labels = []

total_time = 0.0
count_time = 0

for img_path, label in tqdm(zip(images, labels), total=len(images)):
    img = cv2.imread(img_path)

    if img is None:
        continue

    start = time.time()
    faces = app.get(img)
    end = time.time()

    total_time += (end - start)
    count_time += 1

    if len(faces) == 0:
        continue

    face = max(
        faces,
        key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1])
    )

    embeddings.append(face.embedding)
    valid_labels.append(label)

embeddings = np.array(embeddings)
valid_labels = np.array(valid_labels)

avg_infer_time_ms = (total_time / count_time) * 1000

print(f"[INFO] Faces detected: {len(embeddings)}")
print(f"[INFO] Average inference time: {avg_infer_time_ms:.2f} ms/image")

# ================= CREATE PAIRS =================
print("[4] Creating positive / negative pairs...")

scores = []
pair_labels = []

for i, j in combinations(range(len(embeddings)), 2):
    emb1 = embeddings[i]
    emb2 = embeddings[j]

    sim = np.dot(emb1, emb2) / (
        np.linalg.norm(emb1) * np.linalg.norm(emb2)
    )

    scores.append(sim)

    if valid_labels[i] == valid_labels[j]:
        pair_labels.append(1)
    else:
        pair_labels.append(0)

scores = np.array(scores)
pair_labels = np.array(pair_labels)

print("[INFO] Total pairs:", len(scores))

# ================= ROC + AUC =================
print("[5] Computing ROC & AUC...")

fpr, tpr, thresholds = roc_curve(pair_labels, scores)
roc_auc = auc(fpr, tpr)

# ================= BEST THRESHOLD =================
print("[6] Finding best threshold...")

best_acc = 0
best_f1 = 0
best_thresh = 0

for thresh in thresholds:
    preds = (scores >= thresh).astype(int)

    acc = accuracy_score(pair_labels, preds)
    f1 = f1_score(pair_labels, preds)

    if acc > best_acc:
        best_acc = acc
        best_f1 = f1
        best_thresh = thresh

# ================= PRINT RESULTS =================
print("\n----------------------------------------------")
print("| mAP@0.50 | F1-score | Latency (ms) |")
print("----------------------------------------------")

# Với face recognition: dùng AUC ~ mAP@0.50
map50 = roc_auc
latency = avg_infer_time_ms

print(f"|  {map50:.3f}   |   {best_f1:.3f}  |     {latency:.1f}    |")
print("----------------------------------------------")

print("\n[INFO] Best threshold:", round(best_thresh, 4))
print("[INFO] Best accuracy:", round(best_acc, 4))
print("[INFO] AUC (Verification mAP):", round(roc_auc, 4))
