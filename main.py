# # # # main.py

# # # import cv2
# # # import time
# # # from inference import DroneDetector
# # # import config
# # # from utils import draw_geofence

# # # def main():
# # #     cap = cv2.VideoCapture(config.INPUT_SOURCE)
# # #     detector = DroneDetector()

# # #     prev_time = time.time()

# # #     while True:
# # #         ret, frame = cap.read()
# # #         if not ret:
# # #             break

# # #         detections = detector.run(frame)

# # #         # FPS
# # #         curr_time = time.time()
# # #         fps = 1 / (curr_time - prev_time)
# # #         prev_time = curr_time

# # #         for det in detections:
# # #             x1,y1,x2,y2 = det["bbox"]

# # #             color = (0,0,255) if det["intrusion"] else (0,255,0)

# # #             cv2.rectangle(frame, (x1,y1), (x2,y2), color, 2)

# # #             text = f"{det['distance']:.2f}m"
# # #             cv2.putText(frame, text, (x1,y1-10),
# # #                         cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

# # #         draw_geofence(frame, config.GEOFENCE)

# # #         cv2.putText(frame, f"FPS: {fps:.2f}", (10,30),
# # #                     cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)

# # #         cv2.imshow("Drone Detection", frame)

# # #         if cv2.waitKey(1) == 27:
# # #             break

# # #     cap.release()
# # #     cv2.destroyAllWindows()

# # # if __name__ == "__main__":
# # #     main()

# # import cv2
# # import time
# # import numpy as np

# # from inference import detect
# # from utils import draw_box, compute_distance, get_center
# # from geofence import draw_geofence, check_intrusion
# # import config
# # from logger import log_event
# # from preprocessing import enhance_frame
# # from tracker import update_tracks
# # from utils import filter_duplicates
# # from collections import defaultdict
# # import time

# # current_time = time.time()

# # trajectories = defaultdict(list)

# # cap = cv2.VideoCapture("demo.mp4")  # webcam

# # # intrusion_counter = 0
# # intrusion_counter = 0
# # miss_counter = 0
# # prev_boxes = {}
# # prev_centers = {}
# # track_age = {}
# # velocity_data = {}
# # saved_ids = set()
# # save_flag=False

# # while True:
# #     ret, frame = cap.read()
# #     if not ret:
# #         break

# #     start = time.time()
# #     frame=enhance_frame(frame)
# #     frame = cv2.resize(frame, (640, 480))

# # # Run detection
# # # detections = detect(frame)
# #     detections = detect(frame)

# #     filtered = []

# #     for det in detections:
# #         x, y, w, h, conf = det

# #         if conf < 0.7:
# #             continue

# #         if w < 20 or h < 20:
# #             continue

# #         filtered.append(det)

# #     detections = filtered

# #     detections = filter_duplicates(detections)
# #     intrusion_detected = False



# #     # for bbox in detections:
# #     #     x, y, w, h, conf = bbox

# #     #     draw_box(frame, (x,y,w,h))

# #     #     # Distance
# #     #     distance = compute_distance(
# #     #         config.REAL_DRONE_WIDTH,
# #     #         config.FOCAL_LENGTH,
# #     #         w
# #     #     )

# #     #     cv2.putText(frame, f"{distance:.2f}m",
# #     #                 (x, y-10),
# #     #                 cv2.FONT_HERSHEY_SIMPLEX,
# #     #                 0.6, (255,0,0), 2)

# #     #     # Center point
# #     #     center = get_center((x,y,w,h))

# #     #     # Check geofence
# #     #     if check_intrusion(center):
# #     #         intrusion_detected = True

# #     tracks = update_tracks(detections, frame)

# #     for obj in tracks:
# #         track_id = obj["id"]
# #         x, y, w, h = obj["bbox"]
        
# #         cx, cy = get_center((x, y, w, h))
# #         draw_box(frame, (x, y, w, h))

# #         cv2.putText(frame, f"ID: {track_id}",
# #                     (x, y-30),
# #                     cv2.FONT_HERSHEY_SIMPLEX,
# #                     0.6, (0,255,255), 2)

# #         # Distance
# #         distance = compute_distance(
# #             config.REAL_DRONE_WIDTH,
# #             config.FOCAL_LENGTH,
# #             w
# #         )

# #                 # Determine threat level
# #         if distance < 10:
# #             threat = "HIGH"
# #         elif distance < 20:
# #             threat = "MEDIUM"
# #         else:
# #             threat = "LOW" 

# #         cv2.putText(frame, f"{distance:.2f}m",
# #                     (x, y-10),
# #                     cv2.FONT_HERSHEY_SIMPLEX,
# #                     0.6, (255,0,0), 2)

# #         center = get_center((x,y,w,h))

# #         trajectories[track_id].append(center)

# #         if len(trajectories[track_id]) > 30:
# #             trajectories[track_id].pop(0)

# #         points = trajectories[track_id]

# #         for i in range(1, len(points)):
# #             cv2.line(frame, points[i-1], points[i], (0, 255, 255), 1) 
# #             color = (int(track_id) * 50 % 255, 100, 255)
# #             # if threat == "HIGH":
# #             #     color = (0,0,255)
# #             # elif threat == "MEDIUM":
# #             #     color = (0,165,255)
# #             # else:
# #             #     color = (0,255,0)
# #             cv2.line(frame, points[i-1], points[i], color, 2)
# #             cv2.circle(frame, center, 4, (0,255,255), -1) 

          
# #         # cv2.line(frame, points[i-1], points[i], (0, 255, 255), 1)

# #         # color = (track_id * 50 % 255, 100, 255)
# #         # cv2.line(frame, points[i-1], points[i], color, 2)  
# #         if check_intrusion(center):
# #             intrusion_detected = True

        

# #         if track_id in prev_boxes:
# #             prev_w, prev_h = prev_boxes[track_id]

# #             # Prevent sudden size jump
# #             if w > prev_w * 2 or h > prev_h * 2:
# #                 continue

# #         prev_boxes[track_id] = (w, h)

# #         # if track_id in velocity_data:
# #         #     prev_center, prev_time = velocity_data[track_id]

# #         #     dx = center[0] - prev_center[0]
# #         #     dy = center[1] - prev_center[1]

# #         #     distance_px = (dx**2 + dy**2) ** 0.5
# #         #     time_diff = current_time - prev_time

# #         #     if time_diff > 0:
# #         #         speed = distance_px / time_diff
# #         #     else:
# #         #         speed = 0
# #         # else:
# #         #     speed = 0

# #         # velocity_data[track_id] = (center, current_time)
# #         current_time = time.time()

# #         if track_id in velocity_data:
# #             prev_center, prev_time = velocity_data[track_id]

# #             dx = center[0] - prev_center[0]
# #             dy = center[1] - prev_center[1]

# #             distance_px = (dx**2 + dy**2) ** 0.5
# #             time_diff = current_time - prev_time

# #             if time_diff > 0.001:   # avoid near-zero division
# #                 speed = distance_px / time_diff
# #             else:
# #                 speed = 0.0
# #         else:
# #             speed = 0.0

# #         # UPDATE AFTER CALCULATION
# #         velocity_data[track_id] = (center, current_time)
# #         print(track_id, center)


        

# #             # Center stability check
# #         # if track_id in prev_centers:
# #         #     px, py = prev_centers[track_id]

# #         #     # If jump is too large → ignore this detection
# #         #     if abs(cx - px) > 80 or abs(cy - py) > 80:
# #         #         continue

# #         # # Update center
# #         # prev_centers[track_id] = (cx, cy)
# #         # Initialize tracking history
# #         # Track age
# #         if track_id not in track_age:
# #             track_age[track_id] = 0

# #         track_age[track_id] += 1
# #         # if track_id not in prev_centers:
# #         #     prev_centers[track_id] = (cx, cy)
# #         # else:
# #         #     px, py = prev_centers[track_id]

# #         #     # Allow larger movement at beginning
# #         #     if abs(cx - px) > 120 or abs(cy - py) > 120:
# #         #         continue

# #         #     prev_centers[track_id] = (cx, cy)
# #         if track_id not in prev_centers:
# #             prev_centers[track_id] = (cx, cy)

# #         else:
# #             px, py = prev_centers[track_id]

# #             # Apply strict check only after 5 frames
# #             if track_age[track_id] > 5:
# #                 if abs(cx - px) > 80 or abs(cy - py) > 80:
# #                     continue

# #             prev_centers[track_id] = (cx, cy)

# #             # 🚨 SAVE ONLY WHEN NEW DRONE ENTERS GEOFENCE
# #         # if intrusion_detected and track_id not in saved_ids:

# #         #     x1, y1 = x, y
# #         #     x2, y2 = x + w, y + h

# #         #     drone_crop = frame[y1:y2, x1:x2]

# #         #     import time
# #         #     timestamp = time.strftime("%Y%m%d_%H%M%S")

# #         #     filename = f"outputs/drone_ID{track_id}_{timestamp}.jpg"

# #         #     cv2.imwrite(filename, drone_crop)

# #         #     # Save details
# #         #     with open(f"outputs/drone_ID{track_id}_{timestamp}.txt", "w") as f:
# #         #         f.write(f"Drone ID: {track_id}\n")
# #         #         f.write(f"Distance: {distance:.2f} m\n")
# #         #         f.write(f"Speed: {speed:.2f} px/s\n")
# #         #         f.write(f"Time: {timestamp}\n")

# #         #     saved_ids.add(track_id)
# #         if intrusion_detected and track_id not in saved_ids:
# #             save_flag = True
# #             save_id = track_id
# #             save_bbox = (x, y, w, h)
# #             save_distance = distance
# #             save_speed = speed

# #     # Draw geofence
# #     draw_geofence(frame)

# #     if intrusion_detected:
# #         intrusion_counter += 1
# #         miss_counter = 0
# #     else:
# #         miss_counter += 1

# #     # allow small misses
# #     if miss_counter < 5:
# #         intrusion_counter += 1
# #     else:
# #         intrusion_counter = 0

# #     # if intrusion_counter > config.ALERT_FRAMES:
# #     #     cv2.putText(frame, " INTRUSION ALERT - Drone detected ",
# #     #                 (50,50),
# #     #                 cv2.FONT_HERSHEY_SIMPLEX,
# #     #                 1, (0,0,255), 3)
        
# #     #     cv2.putText(frame, f"Speed: {speed:.1f} px/s",
# #     #         (x, y-50),
# #     #         cv2.FONT_HERSHEY_SIMPLEX,
# #     #         0.6, (0,255,255), 2)

# #     #     log_event("Drone intrusion detected")

# #     if intrusion_counter > config.ALERT_FRAMES:

# #         cv2.rectangle(frame, (20,20), (500,120), (0,0,0), -1)

# #         cv2.putText(frame, "DRONE INTRUSION ALERT",
# #                     (30,50),
# #                     cv2.FONT_HERSHEY_SIMPLEX,
# #                     0.7, (0,0,255), 2)

# #         cv2.putText(frame, f"ID: {track_id} threat: {threat}",
# #                     (30,75),
# #                     cv2.FONT_HERSHEY_SIMPLEX,
# #                     0.6, (255,255,255), 2)

# #         cv2.putText(frame, f"Distance: {distance:.1f} m",
# #                     (30,95),
# #                     cv2.FONT_HERSHEY_SIMPLEX,
# #                     0.6, (255,255,255), 2)

# #         cv2.putText(frame, f"Speed: {speed:.1f} px/s",
# #                     (30,115),
# #                     cv2.FONT_HERSHEY_SIMPLEX,
# #                     0.6, (255,255,255), 2)
# #         log_event(f"Drone ID {track_id} intrusion | Dist: {distance:.2f} | Speed: {speed:.2f}")

# #     # FPS
# #     fps = 1 / (time.time() - start)
# #     cv2.putText(frame, f"FPS: {int(fps)}",
# #                 (10,30),
# #                 cv2.FONT_HERSHEY_SIMPLEX,
# #                 0.7, (0,255,0), 2)

# #     display_frame = cv2.resize(frame, (800, 600))

# #     cv2.imshow("Drone Detection", display_frame)

# #     if save_flag:
# #         import time
# #         timestamp = time.strftime("%Y%m%d_%H%M%S")

# #         x, y, w, h = save_bbox

# #         # ✅ Save FULL FRAME (with boxes + text)
# #         full_filename = f"outputs/full_ID{save_id}_{timestamp}.jpg"
# #         cv2.imwrite(full_filename, frame)

# #         # ✅ Save CROPPED DRONE
# #         crop = frame[y:y+h, x:x+w]
# #         crop_filename = f"outputs/crop_ID{save_id}_{timestamp}.jpg"
# #         cv2.imwrite(crop_filename, crop)

# #         # ✅ Save DETAILS
# #         with open(f"outputs/data_ID{save_id}_{timestamp}.txt", "w") as f:
# #             f.write(f"Drone ID: {save_id}\n")
# #             f.write(f"Distance: {save_distance:.2f} m\n")
# #             f.write(f"Speed: {save_speed:.2f} px/s\n")
# #             f.write(f"Time: {timestamp}\n")

# #         saved_ids.add(save_id)
# #         save_flag = False

# #     if cv2.waitKey(1) & 0xFF == ord('q'):
# #             break


# # cap.release()
# # cv2.destroyAllWindows()

# import cv2
# import time
# import numpy as np
# import os

# from inference import detect
# from utils import draw_box, compute_distance, get_center, filter_duplicates
# from geofence import draw_geofence, check_intrusion
# import config
# from logger import log_event
# from preprocessing import enhance_frame
# from tracker import update_tracks
# from collections import defaultdict


# def run_pipeline(source_type="video", source=0):

#     os.makedirs("outputs", exist_ok=True)

#     if source_type == "image":
#         frame = cv2.imread(source)
#         process_single_frame(frame)
#         return

#     elif source_type == "video":
#         cap = cv2.VideoCapture(source)

#     elif source_type == "webcam":
#         cap = cv2.VideoCapture(0)

#     # ✅ Video writer for Streamlit output
#     out = cv2.VideoWriter(
#         "output.mp4",
#         cv2.VideoWriter_fourcc(*'mp4v'),
#         20,
#         (640, 480)
#     )

#     trajectories = defaultdict(list)

#     intrusion_counter = 0
#     miss_counter = 0
#     prev_boxes = {}
#     prev_centers = {}
#     track_age = {}
#     velocity_data = {}
#     saved_ids = set()
#     save_flag = False

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         start = time.time()
#         frame = enhance_frame(frame)
#         frame = cv2.resize(frame, (640, 480))

#         detections = detect(frame)

#         # 🔹 Filter detections
#         filtered = []
#         for det in detections:
#             x, y, w, h, conf = det

#             if conf < 0.7:
#                 continue
#             if w < 20 or h < 20:
#                 continue

#             filtered.append(det)

#         detections = filter_duplicates(filtered)

#         intrusion_detected = False

#         # 🔹 Tracking
#         tracks = update_tracks(detections, frame)

#         for obj in tracks:
#             track_id = int(obj["id"])
#             x, y, w, h = obj["bbox"]

#             center = get_center((x, y, w, h))

#             # Track age
#             track_age[track_id] = track_age.get(track_id, 0) + 1

#             # Stability check
#             if track_id in prev_centers:
#                 px, py = prev_centers[track_id]
#                 if track_age[track_id] > 5:
#                     if abs(center[0] - px) > 80 or abs(center[1] - py) > 80:
#                         continue
#             prev_centers[track_id] = center

#             # Distance
#             distance = compute_distance(
#                 config.REAL_DRONE_WIDTH,
#                 config.FOCAL_LENGTH,
#                 w
#             )

#             # Threat
#             if distance < 10:
#                 threat = "HIGH"
#                 color = (0, 0, 255)
#             elif distance < 20:
#                 threat = "MEDIUM"
#                 color = (0, 165, 255)
#             else:
#                 threat = "LOW"
#                 color = (0, 255, 0)

#             # Velocity
#             current_time = time.time()
#             if track_id in velocity_data:
#                 prev_c, prev_t = velocity_data[track_id]
#                 dx = center[0] - prev_c[0]
#                 dy = center[1] - prev_c[1]
#                 dist_px = (dx**2 + dy**2) ** 0.5
#                 dt = current_time - prev_t
#                 speed = dist_px / dt if dt > 0.001 else 0
#             else:
#                 speed = 0

#             velocity_data[track_id] = (center, current_time)

#             # Trajectory
#             trajectories[track_id].append(center)
#             if len(trajectories[track_id]) > 30:
#                 trajectories[track_id].pop(0)

#             for i in range(1, len(trajectories[track_id])):
#                 cv2.line(frame,
#                          trajectories[track_id][i - 1],
#                          trajectories[track_id][i],
#                          color, 2)

#             # Draw box
#             draw_box(frame, (x, y, w, h))
#             cv2.putText(frame, f"ID:{track_id}", (x, y - 60),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
#             cv2.putText(frame, f"{distance:.1f}m", (x, y - 40),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
#             cv2.putText(frame, f"{speed:.1f}px/s", (x, y - 20),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

#             # Intrusion check
#             if check_intrusion(center):
#                 intrusion_detected = True

#             # Save trigger
#             if intrusion_detected and track_id not in saved_ids:
#                 save_flag = True
#                 save_id = track_id
#                 save_bbox = (x, y, w, h)
#                 save_distance = distance
#                 save_speed = speed

#         draw_geofence(frame)

#         # Alert logic
#         if intrusion_detected:
#             intrusion_counter += 1
#             miss_counter = 0
#         else:
#             miss_counter += 1
#             if miss_counter > 5:
#                 intrusion_counter = 0

#         if intrusion_counter > config.ALERT_FRAMES:
#             cv2.putText(frame, "🚨 INTRUSION ALERT 🚨",
#                         (50, 50),
#                         cv2.FONT_HERSHEY_SIMPLEX,
#                         1, (0, 0, 255), 3)

#             log_event(f"Drone ID {save_id} intrusion | Dist: {save_distance:.2f} | Speed: {save_speed:.2f}")

#         # FPS
#         fps = 1 / (time.time() - start)
#         cv2.putText(frame, f"FPS:{int(fps)}",
#                     (10, 30),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     0.7, (0, 255, 0), 2)

#         # ✅ Save output video
#         out.write(frame)

#         # Optional local display
#         cv2.imshow("Drone Detection", frame)

#         # ✅ SAVE FULL FRAME + DATA
#         if save_flag:
#             timestamp = time.strftime("%Y%m%d_%H%M%S")

#             full_filename = f"outputs/full_ID{save_id}_{timestamp}.jpg"
#             cv2.imwrite(full_filename, frame)

#             with open(f"outputs/data_ID{save_id}_{timestamp}.txt", "w") as f:
#                 f.write(f"Drone ID: {save_id}\n")
#                 f.write(f"Distance: {save_distance:.2f} m\n")
#                 f.write(f"Speed: {save_speed:.2f} px/s\n")
#                 f.write(f"Time: {timestamp}\n")

#             saved_ids.add(save_id)
#             save_flag = False

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     out.release()
#     cv2.destroyAllWindows()


import cv2
import time
import os
from collections import defaultdict

from inference import detect
from utils import draw_box, compute_distance, get_center, filter_duplicates
from geofence import draw_geofence, check_intrusion
import config
from logger import log_event
from preprocessing import enhance_frame
from tracker import update_tracks
from logger import log_event

def process_frame(frame, state):

    start = time.time()
    frame = enhance_frame(frame)
    frame = cv2.resize(frame, (640, 480))

    detections = detect(frame)

    # 🔹 Filter detections
    filtered = []
    for det in detections:
        x, y, w, h, conf = det
        if conf < 0.7:
            continue
        if w < 20 or h < 20:
            continue
        filtered.append(det)

    detections = filter_duplicates(filtered)

    intrusion_detected = False

    tracks = update_tracks(detections, frame)

    for obj in tracks:
        track_id = int(obj["id"])
        x, y, w, h = obj["bbox"]

        center = get_center((x, y, w, h))

        state["track_age"][track_id] = state["track_age"].get(track_id, 0) + 1

       

        # Stability
        if track_id in state["prev_centers"]:
            px, py = state["prev_centers"][track_id]
            if state["track_age"][track_id] > 5:
                if abs(center[0] - px) > 80 or abs(center[1] - py) > 80:
                    continue
        state["prev_centers"][track_id] = center

        # Distance
        distance = compute_distance(config.REAL_DRONE_WIDTH, config.FOCAL_LENGTH, w)

        # Threat
        if distance < 10:
            threat = "HIGH"
            color = (0, 0, 255)
        elif distance < 20:
            threat = "MEDIUM"
            color = (0, 165, 255)
        else:
            threat = "LOW"
            color = (0, 255, 0)

        
        # Velocity
        current_time = time.time()
        if track_id in state["velocity_data"]:
            prev_c, prev_t = state["velocity_data"][track_id]
            dx = center[0] - prev_c[0]
            dy = center[1] - prev_c[1]
            dist_px = (dx**2 + dy**2) ** 0.5
            dt = current_time - prev_t
            speed = dist_px / dt if dt > 0.001 else 0
        else:
            speed = 0

        state["velocity_data"][track_id] = (center, current_time)

        # Trajectory
        state["trajectories"][track_id].append(center)
        if len(state["trajectories"][track_id]) > 30:
            state["trajectories"][track_id].pop(0)

        for i in range(1, len(state["trajectories"][track_id])):
            cv2.line(frame,
                     state["trajectories"][track_id][i - 1],
                     state["trajectories"][track_id][i],
                     color, 2)

        # draw_box(frame, (x, y, w, h))
        # cv2.putText(frame, f"ID:{track_id}", (x, y - 60),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        # cv2.putText(frame, f"{distance:.1f}m", (x, y - 40),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        # cv2.putText(frame, f"{speed:.1f}px/s", (x, y - 20),
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        # Draw box
        draw_box(frame, (x, y, w, h))

        cv2.putText(frame, f"ID:{track_id}", (x, y - 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        cv2.putText(frame, f"Threat: {threat}", (x, y - 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        cv2.putText(frame, f"{distance:.1f}m", (x, y - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        cv2.putText(frame, f"{speed:.1f}px/s", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        state["last_alert"] = {
            "id": track_id,
            "distance": distance,
            "speed": speed,
            "threat": threat
        }
        if check_intrusion(center):
            intrusion_detected = True

            state["last_alert"] = {
                "id": track_id,
                "distance": distance,
                "speed": speed,
                "threat": threat
            }

        # Save full frame once
        # if intrusion_detected and track_id not in state["saved_ids"]:
        #     timestamp = time.strftime("%Y%m%d_%H%M%S")
        #     filename = f"outputs/full_ID{track_id}_{timestamp}.jpg"
        #     cv2.imwrite(filename, frame)
        #     state["saved_ids"].add(track_id)
        if intrusion_detected and track_id not in state["saved_ids"]:

            timestamp = time.strftime("%Y%m%d_%H%M%S")

            # ✅ SAVE ONLY FULL FRAME (with boxes + info)
            filename = f"outputs/full_ID{track_id}_{timestamp}.jpg"
            cv2.imwrite(filename, frame)

            # ✅ Save metadata (optional but recommended)
            # with open(f"outputs/data_ID{track_id}_{timestamp}.txt", "w") as f:
            #     f.write(f"Drone ID: {track_id}\n")
            #     f.write(f"Distance: {distance:.2f} m\n")
            #     f.write(f"Speed: {speed:.2f} px/s\n")
            #     f.write(f"Time: {timestamp}\n")++

            state["saved_ids"].add(track_id)

    draw_geofence(frame)

    # Alert logic
    if intrusion_detected:
        state["intrusion_counter"] += 1
        state["miss_counter"] = 0
    else:
        state["miss_counter"] += 1
        if state["miss_counter"] > 5:
            state["intrusion_counter"] = 0

    # if state["intrusion_counter"] > config.ALERT_FRAMES:
    #     cv2.putText(frame, " INTRUSION ALERT ",
    #                 (50, 50),
    #                 cv2.FONT_HERSHEY_SIMPLEX,
    #                 1, (0, 0, 255), 3)
    if state["intrusion_counter"] > config.ALERT_FRAMES and "last_alert" in state:

        alert = state["last_alert"]

        cv2.rectangle(frame, (20,20), (520,130), (0,0,0), -1)

        cv2.putText(frame, " DRONE INTRUSION ALERT ",
                    (30,50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (0,0,255), 2)

        cv2.putText(frame, f"ID: {alert['id']} | Threat: {alert['threat']}",
                    (30,75),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (255,255,255), 2)

        cv2.putText(frame, f"Distance: {alert['distance']:.1f} m",
                    (30,100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (255,255,255), 2)

        cv2.putText(frame, f"Speed: {alert['speed']:.1f} px/s",
                    (30,120),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (255,255,255), 2)
        
        if not state.get("logged", False):
            log_event(f"Drone ID {alert['id']} | Threat: {alert['threat']} | "
                    f"Dist: {alert['distance']:.2f} | Speed: {alert['speed']:.2f}")
            state["logged"] = True

    if state["intrusion_counter"] == 0:
        state["logged"] = False        
    fps = 1 / (time.time() - start)

    cv2.putText(frame, f"FPS: {int(fps)}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7, (0,255,0), 2)

    return frame, state


def run_pipeline(source_type="video", source=0):

    os.makedirs("outputs", exist_ok=True)

    state = {
        "trajectories": defaultdict(list),
        "velocity_data": {},
        "prev_centers": {},
        "track_age": {},
        "saved_ids": set(),
        "intrusion_counter": 0,
        "miss_counter": 0
    }

    # IMAGE
    if source_type == "image":
        frame = cv2.imread(source)
        frame, _ = process_frame(frame, state)
        cv2.imshow("Image Detection", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return

    # VIDEO / WEBCAM
    cap = cv2.VideoCapture(0 if source_type == "webcam" else source)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame, state = process_frame(frame, state)

        cv2.imshow("Drone Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()