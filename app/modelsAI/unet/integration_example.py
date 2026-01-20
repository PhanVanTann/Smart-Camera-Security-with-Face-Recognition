
import cv2
import numpy as np
from app.modelsAI.face_detector.detector import detect_and_crop_faces
from app.modelsAI.unet.segmentaion import segment_face
from app.modelsAI.insightFace.model import app as insightface_model_app
from app.modelsAI.insightFace.embeding import get_face_embedding

def process_face_with_unet(image_path):

    # 1. Load image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Cannot load image")
    
    print("Step 1: MTCNN Face Detection...")
    # 2. MTCNN: Detect face
    faces = detect_and_crop_faces(img, margin=0.25)
    
    if len(faces) == 0:
        raise ValueError("No face detected by MTCNN")
    
    face_img = faces[0]  # Get first detected face
    print(f"  ✓ Face detected: {face_img.shape}")
    
    print("Step 2: UNet Cleaning (remove background/hair/hat)...")
    # 3. UNet: Clean face (remove background, hair, hat)
    cleaned_face = segment_face(face_img)
    print(f"  ✓ Face cleaned: {cleaned_face.shape}")
    
    print("Step 3: InsightFace Embedding Extraction...")
    # 4. InsightFace: Extract embedding from cleaned face
    embedding = get_face_embedding(cleaned_face, insightface_model_app)
    
    if embedding is None:
        raise ValueError("Failed to extract embedding")
    
    print(f"  ✓ Embedding extracted: {len(embedding)}-dim vector")
    
    return embedding, cleaned_face

def process_face_with_unet(img_bytes):
    # Decode image
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        raise ValueError("Invalid image")
    
    # MTCNN: Detect face
    faces = detect_and_crop_faces(img, margin=0.25)
    
    if len(faces) == 0:
        raise ValueError("No face detected")
    
    face_img = faces[0]
    
    # UNet: Clean face
    cleaned_face = segment_face(face_img)
    
    # InsightFace: Extract embedding
    embedding = get_face_embedding(cleaned_face, insightface_model_app)
    
    if embedding is None:
        raise ValueError("Failed to extract embedding")
    
    return embedding

# ===== TEST EXAMPLE =====
if __name__ == "__main__":
    # Test với file ảnh
    try:
        embedding, cleaned = process_face_with_unet("app/test1.jpg")
        
        print("\n" + "="*50)
        print("SUCCESS!")
        print(f"Embedding shape: {len(embedding)}")
        print(f"Embedding sample: {embedding[:5]}")
        
        # Save cleaned face for inspection
        cv2.imwrite("cleaned_face_output.jpg", cleaned)
        print("Cleaned face saved to: cleaned_face_output.jpg")
        
    except Exception as e:
        print(f"Error: {e}")
