# # preprocessing.py

# import cv2

# def preprocess_frame(frame):
#     frame = cv2.resize(frame, (640, 480))
#     return frame

import cv2
import numpy as np

def preprocess_frame(frame, size=640):
    """
    Resize and normalize frame before inference
    (Optional because YOLO does this internally)
    """
    frame_resized = cv2.resize(frame, (size, size))
    frame_normalized = frame_resized / 255.0
    return frame_normalized


def enhance_frame(frame):
    """
    Improve visibility (useful for drone detection)
    """
    # Convert to LAB color space
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    # Apply CLAHE (contrast enhancement)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    cl = clahe.apply(l)

    merged = cv2.merge((cl, a, b))
    enhanced = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)

    return enhanced


def blur_frame(frame):
    """
    Optional smoothing
    """
    return cv2.GaussianBlur(frame, (5,5), 0)