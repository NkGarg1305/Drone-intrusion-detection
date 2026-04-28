# # inference.py

# from ultralytics import YOLO
# import cv2
# import time
# from utils import estimate_distance, point_in_polygon
# import config

# class DroneDetector:
#     def __init__(self):
#         self.model = YOLO(config.MODEL_PATH)

#     def run(self, frame):
#         results = self.model(frame)

#         detections = []

#         for r in results:
#             for box in r.boxes:
#                 conf = float(box.conf[0])
#                 if conf < config.CONF_THRESHOLD:
#                     continue

#                 x1, y1, x2, y2 = map(int, box.xyxy[0])
#                 width = x2 - x1

#                 distance = estimate_distance(
#                     config.REAL_DRONE_WIDTH,
#                     config.FOCAL_LENGTH,
#                     width
#                 )

#                 center = ((x1+x2)//2, (y1+y2)//2)

#                 intrusion = point_in_polygon(center, config.GEOFENCE)

#                 detections.append({
#                     "bbox": (x1,y1,x2,y2),
#                     "distance": distance,
#                     "intrusion": intrusion
#                 })

#         return detections

from ultralytics import YOLO
import config

model = YOLO(config.MODEL_PATH)

def detect(frame):
    results = model(frame)[0]

    detections = []

    for box in results.boxes:
        x1, y1, x2, y2 = box.xyxy[0]
        conf = float(box.conf[0])

        if conf > config.CONF_THRESHOLD:
            detections.append([
                int(x1), int(y1),
                int(x2 - x1), int(y2 - y1),
                conf
            ])

    return detections