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

def has_mask( prediction_mask):

    # class id
    NOSE = 2
    MOUTH = [10, 11, 12]

    h, w = prediction_mask.shape
    total_pixels = h * w

    nose_pixels = np.sum(prediction_mask == NOSE)
    mouth_pixels = np.sum(np.isin(prediction_mask, MOUTH))

    nose_ratio = nose_pixels / total_pixels
    mouth_ratio = mouth_pixels / total_pixels

    # THRESHOLD – bạn có thể tinh chỉnh
    NOSE_THRESHOLD = 0.010236
    MOUTH_THRESHOLD = 0.004886

    has_mask = (nose_ratio < NOSE_THRESHOLD) and (mouth_ratio < MOUTH_THRESHOLD)
    return has_mask