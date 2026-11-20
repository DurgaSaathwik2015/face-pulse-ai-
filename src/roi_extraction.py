import numpy as np
import cv2

# Face Mesh landmark groups: forehead and bilateral upper cheeks.
FOREHEAD = [10, 109, 67, 103, 54, 21, 71, 68, 104, 69, 108, 151, 337, 299, 333, 298, 301]
LEFT_CHEEK = [50, 101, 118, 117, 123, 147, 187, 205, 36, 206, 203]
RIGHT_CHEEK = [280, 330, 347, 346, 352, 376, 411, 425, 266, 426, 423]

def _points(landmarks, ids, width, height):
    return np.array([(int(landmarks[i].x * width), int(landmarks[i].y * height)) for i in ids], dtype=np.int32)

def extract_roi_means(rgb, landmarks):
    h, w = rgb.shape[:2]
    masks = []
    for ids in (FOREHEAD, LEFT_CHEEK, RIGHT_CHEEK):
        pts = _points(landmarks, ids, w, h)
        mask = np.zeros((h, w), dtype=np.uint8)
        hull = cv2.convexHull(pts)
        cv2.fillConvexPoly(mask, hull, 255)
        masks.append(mask)
    pixels = [rgb[m > 0] for m in masks]
    pixels = [p for p in pixels if len(p) >= 20]
    if not pixels:
        return None
    # Average ROI means; each region contributes equally.
    return np.mean([p.mean(axis=0) for p in pixels], axis=0)

def draw_rois(rgb, landmarks):
    out = rgb.copy()
    h, w = out.shape[:2]
    for ids in (FOREHEAD, LEFT_CHEEK, RIGHT_CHEEK):
        pts = _points(landmarks, ids, w, h)
        cv2.polylines(out, [cv2.convexHull(pts)], True, (30, 220, 90), 2)
    return out
