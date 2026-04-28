# import streamlit as st
# import tempfile
# import os
# from main import run_pipeline

# st.title("🚁 Drone Intrusion Detection System")

# uploaded_file = st.file_uploader("Upload Video", type=["mp4","avi"])

# if uploaded_file is not None:

#     # Save uploaded video
#     tfile = tempfile.NamedTemporaryFile(delete=False)
#     tfile.write(uploaded_file.read())

#     st.info("Processing video...")

#     # Run your existing pipeline
#     run_pipeline(tfile.name)

#     st.success("Processing complete!")

#     # Show output video
#     if os.path.exists("output.mp4"):
#         st.video("output.mp4")

#     # Show saved images
#     st.subheader("Captured Intrusions")

#     if os.path.exists("outputs"):
#         images = os.listdir("outputs")

#         for img in images:
#             st.image(f"outputs/{img}", caption=img)

import streamlit as st
import tempfile
import os
import pandas as pd
from main import run_pipeline

st.title("🚁 Drone Intrusion Detection System")

mode = st.selectbox("Select Mode", ["Video", "Image", "Webcam"])

if mode == "Video":
    uploaded_file = st.file_uploader("Upload Video", type=["mp4","avi"])

    if uploaded_file:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())

        st.info("Processing video...")
        run_pipeline("video", tfile.name)
        st.success("Done!")

elif mode == "Image":
    uploaded_file = st.file_uploader("Upload Image", type=["jpg","png"])

    if uploaded_file:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())

        run_pipeline("image", tfile.name)

elif mode == "Webcam":
    if st.button("Start Webcam"):
        run_pipeline("webcam", 0)




# log_file = "logs/logs.txt"

# if os.path.exists(log_file):
#     with open(log_file, "r") as f:
#         logs = f.read()
#     st.text(logs)
# else:
#     st.info("No logs yet.")

import pandas as pd
import re

st.subheader("📊 Intrusion Logs Table")

log_file = "logs/logs.txt"

if os.path.exists(log_file):

    data = []

    with open(log_file, "r") as f:
        for line in f:

            try:
                # Example line:
                # 2026-04-24 14:15:06 - Drone ID 5 intrusion | Dist: 3.93 | Speed: 3.43

                # Split time and rest
                time_part, rest = line.split(" - ")

                # Extract ID
                id_match = re.search(r"ID (\d+)", rest)
                drone_id = id_match.group(1) if id_match else "?"

                # Extract distance
                dist_match = re.search(r"Dist:\s*([\d.]+)", rest)
                distance = dist_match.group(1) if dist_match else "?"

                # Extract speed
                speed_match = re.search(r"Speed:\s*([\d.]+)", rest)
                speed = speed_match.group(1) if speed_match else "?"

                data.append({
                    "Time": time_part.strip(),
                    "Drone ID": drone_id,
                    "Distance (m)": distance,
                    "Speed (px/s)": speed
                })

            except:
                continue

    if data:
        df = pd.DataFrame(data)
        df = df.drop_duplicates(subset=["Drone ID", "Time"])
        df = df.sort_values(by="Time", ascending=False)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No valid log entries found.")
else:
    st.info("No logs available.")





# def highlight_threat(row):
#     if "HIGH" in row["Threat"]:
#         return ["background-color: red"] * len(row)
#     elif "MEDIUM" in row["Threat"]:
#         return ["background-color: orange"] * len(row)
#     else:
#         return ["background-color: lightgreen"] * len(row)

# st.dataframe(df.style.apply(highlight_threat, axis=1))


# Show saved outputs
st.subheader("📸 Captured Intrusions")

if os.path.exists("outputs"):
    for img in os.listdir("outputs"):
        st.image(f"outputs/{img}", caption=img)

# st.text_area("Logs", logs, height=100)