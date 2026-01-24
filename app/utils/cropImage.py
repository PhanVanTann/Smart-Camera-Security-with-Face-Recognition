def cropImage(image, bbox):
    if image is None:
        return None

    h, w = image.shape[:2]
    x1, y1, x2, y2 = map(int, bbox)

    # clamp bbox
    x1 = max(0, x1)
    y1 = max(0, y1)
    x2 = min(w, x2)
    y2 = min(h, y2)

    if x2 <= x1 or y2 <= y1:
        return None

    cropped = image[y1:y2, x1:x2]

    if cropped.size == 0:
        return None

    return cropped