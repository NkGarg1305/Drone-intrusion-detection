# # utils.py
# import cv2
# import numpy as np

# def estimate_distance(real_width, focal_length, pixel_width):
#     if pixel_width == 0:
#         return 0
#     return (real_width * focal_length) / pixel_width


# def point_in_polygon(point, polygon):
#     return cv2.pointPolygonTest(
#         np.array(polygon, np.int32), point, False
#     ) >= 0


# def draw_geofence(frame, polygon):
#     pts = np.array(polygon, np.int32)
#     cv2.polylines(frame, [pts], isClosed=True, color=(0,0,255), thickness=2)

import cv2

def draw_box(frame, bbox):
    x, y, w, h = bbox
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

def compute_distance(real_width, focal_length, pixel_width):
    return (real_width * focal_length) / pixel_width

def get_center(bbox):
    x, y, w, h = bbox
    return (int(x + w/2), int(y + h/2))

import numpy as np

def iou(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2

    xi1 = max(x1, x2)
    yi1 = max(y1, y2)
    xi2 = min(x1 + w1, x2 + w2)
    yi2 = min(y1 + h1, y2 + h2)

    inter_area = max(0, xi2 - xi1) * max(0, yi2 - yi1)

    box1_area = w1 * h1
    box2_area = w2 * h2

    union = box1_area + box2_area - inter_area

    return inter_area / union if union > 0 else 0

def filter_duplicates(detections, iou_thresh=0.5):
    detections = sorted(detections, key=lambda x: x[4], reverse=True)

    filtered = []

    for det in detections:
        keep = True
        for f in filtered:
            if iou(det[:4], f[:4]) > iou_thresh:
                keep = False
                break
        if keep:
            filtered.append(det)

    return filtered