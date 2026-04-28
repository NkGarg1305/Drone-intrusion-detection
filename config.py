# # config.py

# MODEL_PATH = "models/yolov8n.pt"

# # Input source (0 = webcam, or video path)
# INPUT_SOURCE = 0

# # Detection settings
# CONF_THRESHOLD = 0.4

# # Drone real width (meters)
# REAL_DRONE_WIDTH = 0.3

# # Camera calibration
# FOCAL_LENGTH = 800  # you will update after calibration

# # Geofence polygon (clockwise points)
# GEOFENCE = [(100,100), (500,100), (500,400), (100,400)]

# # Logging
# LOG_FILE = "logs/output.log"

MODEL_PATH = "models/best.pt"

CONF_THRESHOLD = 0.7

REAL_DRONE_WIDTH = 0.3   # meters
FOCAL_LENGTH = 800       # adjust if needed

ALERT_FRAMES = 5