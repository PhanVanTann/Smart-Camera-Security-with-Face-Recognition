import cv2
import numpy as np
import torch

# Device configuration
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def preprocess_unet(face_img):
    face_img = np.array(face_img)
    face_img = cv2.cvtColor(face_img, cv2.COLOR_RGB2BGR)
    
    img = cv2.resize(face_img, (512, 512), interpolation=cv2.INTER_LINEAR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.astype(np.float32) / 255.0
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    img = (img - mean) / std
    img = img.transpose((2, 0, 1)) 
    img_tensor = torch.as_tensor(img, dtype=torch.float32).unsqueeze(0)
    return img_tensor.to(DEVICE)

def filter_occlusions(original_img, prediction_mask):
    original_img = np.array(original_img)
    original_img = cv2.cvtColor(original_img, cv2.COLOR_RGB2BGR)
    
    original_resized = cv2.resize(original_img, (512, 512))
    
    VALID_CLASSES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 16, 17] 
    binary_mask = np.isin(prediction_mask, VALID_CLASSES).astype(np.uint8)
    
    kernel = np.ones((3,3), np.uint8)
    binary_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_OPEN, kernel)
    binary_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_CLOSE, kernel)

    mask_3d = np.repeat(binary_mask[:, :, np.newaxis], 3, axis=2)
    clean_face = original_resized * mask_3d
    
    return clean_face, binary_mask, original_resized