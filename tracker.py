# from deep_sort_realtime.deepsort_tracker import DeepSort

# tracker = DeepSort(max_age=30)

# def update_tracks(detections, frame):
#     """
#     detections: list of [x, y, w, h, conf]
#     """
#     tracks = tracker.update_tracks(detections, frame=frame)

#     results = []

#     for track in tracks:
#         if not track.is_confirmed():
#             continue

#         track_id = track.track_id
#         l, t, w, h = track.to_ltrb()

#         results.append({
#             "id": track_id,
#             "bbox": (int(l), int(t), int(w-l), int(h-t))
#         })

#     return results

from deep_sort_realtime.deepsort_tracker import DeepSort

# tracker = DeepSort(max_age=30)
tracker = DeepSort(
    max_age=10,
    n_init=3,
    max_iou_distance=0.5,
    max_cosine_distance=0.4
)

def update_tracks(detections, frame):
    """
    detections: [x, y, w, h, conf]
    Convert to DeepSORT format
    """

    ds_detections = []

    for det in detections:
        x, y, w, h, conf = det

        ds_detections.append([[x, y, w, h], conf])

    tracks = tracker.update_tracks(ds_detections, frame=frame)

    results = []

    for track in tracks:
        if not track.is_confirmed():
            continue

        track_id = track.track_id
        l, t, r, b = track.to_ltrb()

        results.append({
            "id": track_id,
            "bbox": (int(l), int(t), int(r - l), int(b - t))
        })

    return results