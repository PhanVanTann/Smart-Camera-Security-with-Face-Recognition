import os
from app.services.faceEmbeddingService import get_face_embedding

RESIDENT_DIR = "dataset/residents"

resident_embeddings = {}

for person in os.listdir(RESIDENT_DIR):
    person_dir = os.path.join(RESIDENT_DIR, person)
    resident_embeddings[person] = []

    for img_name in os.listdir(person_dir):
        img_path = os.path.join(person_dir, img_name)
        try:
            emb = get_face_embedding(img_path)
            resident_embeddings[person].append(emb)
        except Exception as e:
            print(f"Skip {img_path}: {e}")

print(resident_embeddings)