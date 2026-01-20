import cv2
import numpy as np
import torch
import segmentation_models_pytorch as smp
import os
from .unet import preprocess_unet, filter_occlusions, DEVICE

# Model configuration
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pth")
_unet_model = None

def load_unet_model():
    """Load UNet model - called once"""
    global _unet_model
    if _unet_model is not None:
        return _unet_model
    
    model = smp.Unet(
        encoder_name="resnet34", 
        encoder_weights=None, 
        in_channels=3, 
        classes=19
    )
    try: 
        state_dict = torch.load(MODEL_PATH, map_location=DEVICE)
        model.load_state_dict(state_dict)
        model.to(DEVICE)
        model.eval()
        print(f"[UNet] Model loaded successfully from {MODEL_PATH}")
        _unet_model = model
        return model
    except Exception as e:
        print(f"[UNet] Error loading model: {e}")
        return None

def segment_face(img):
    model = load_unet_model()
    if model is None:
        print("Model not loaded")
        return 
    
    # Preprocess
    img_tensor = preprocess_unet(img)
    
    # Segment
    with torch.no_grad():
        output = model(img_tensor)
        prediction = torch.argmax(output, dim=1).squeeze(0).cpu().numpy()
    
    # Filter occlusions
    clean_face_output, binary_mask, original_resized = filter_occlusions(img, prediction)
    
    # Resize back to original size
    clean_face_final = cv2.resize(clean_face_output, (img.shape[1], img.shape[0]))
    
    return clean_face_final

# Optional: Tô màu cho mask (for visualization)
def decode_segmap(image, nc=19):
    label_colors = np.array([
        (0, 0, 0),       # 0=Back (Đen)
        (204, 0, 0),     # 1=Skin (Đỏ)
        (76, 153, 0),    # 2=Nose
        (204, 204, 0),   # 3=Eye_G
        (51, 51, 255),   # 4=L_Eye
        (204, 0, 204),   # 5=R_Eye
        (0, 255, 255),   # 6=L_Brow
        (255, 204, 204), # 7=R_Brow
        (102, 51, 0),    # 8=L_Ear
        (255, 0, 0),     # 9=R_Ear
        (102, 204, 0),   # 10=Mouth
        (255, 255, 0),   # 11=U_Lip
        (0, 0, 153),     # 12=L_Lip
        (0, 0, 204),     # 13=Hair (Xanh đậm)
        (255, 51, 153),  # 14=Hat
        (0, 204, 204),   # 15=Ear_R
        (0, 51, 0),      # 16=Neck_L
        (255, 153, 51),  # 17=Neck
        (0, 204, 0),     # 18=Cloth
    ])
    
    r = np.zeros_like(image).astype(np.uint8)
    g = np.zeros_like(image).astype(np.uint8)
    b = np.zeros_like(image).astype(np.uint8)
    
    for l in range(0, nc):
        idx = image == l
        r[idx] = label_colors[l, 0]
        g[idx] = label_colors[l, 1]
        b[idx] = label_colors[l, 2]
        
    return np.stack([r, g, b], axis=2)
