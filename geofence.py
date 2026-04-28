import cv2
import numpy as np

# Define polygon (change for your demo)
GEOFENCE = [(100,100), (500,100), (500,400), (100,400)]

def draw_geofence(frame):
    pts = np.array(GEOFENCE, np.int32)
    cv2.polylines(frame, [pts], True, (255,255,0), 2)

def check_intrusion(point):
    pts = np.array(GEOFENCE, np.int32)
    return cv2.pointPolygonTest(pts, point, False) >= 0