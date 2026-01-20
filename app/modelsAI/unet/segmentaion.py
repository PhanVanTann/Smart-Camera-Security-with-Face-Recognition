import cv2
import numpy as np
import torch
import segmentation_models_pytorch as smp
import os
from .unet import preprocess_unet,has_mask, DEVICE

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
    mask = has_mask( prediction)

    
    return mask

