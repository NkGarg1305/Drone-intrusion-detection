#Drone Intrusion Detection and Tracking System

---

## 1. Project Title

**Drone Intrusion Detection and Tracking using CNN-based Object Detection**

---

## 2. Problem Statement

With the rapid increase in drone usage, unauthorized drone activity has become a major security concern in sensitive areas such as airports, military zones, and private properties.

Traditional surveillance systems rely on manual monitoring or radar-based systems, which are either inefficient or expensive. Therefore, there is a need for an automated, intelligent system that can:

* Detect drones in real-time
* Track their movement
* Identify intrusion into restricted zones
* Generate alerts and analytics

This project solves the above problem using deep learning and computer vision techniques.

---

## 3. Role of Edge Computing

*(Note: Current implementation is on local system, but architecture supports edge deployment)*

* The system is designed to run inference locally without requiring cloud processing
* Enables real-time detection with low latency
* Can be deployed on edge devices like NVIDIA Jetson Nano (future work)

**Benefits:**

* Faster response time
* No internet dependency
* Improved privacy

---

## 4. Methodology / Approach

### System Pipeline

```text
Input → Preprocessing → YOLOv8 Detection → DeepSORT Tracking → 
Distance & Velocity → Geofence Check → Alert → Output
```

---

### Explanation of Each Stage

**1. Input**

* Supports Image, Video, and Webcam feed

**2. Preprocessing**

* Frame resizing
* Enhancement for better detection

**3. Detection (YOLOv8)**

* Detects drones using bounding boxes
* Outputs: (x, y, w, h, confidence)

**4. Tracking (DeepSORT)**

* Assigns unique ID to each drone
* Maintains identity across frames

**5. Analytics**

* Distance estimation using pinhole camera model
* Speed (velocity) calculation

**6. Geofence**

* Defined polygon region
* Detects intrusion based on drone position

**7. Alert System**

* Triggered when drone stays inside region for multiple frames

---

## 5. Model Details

* Model Used: **YOLOv8 (CNN-based object detection)**
* Framework: **PyTorch (Ultralytics)**
* Input Size: **640 × 640**
* Output:

  * Bounding boxes
  * Confidence score

---

### Architecture

* Backbone → Feature extraction
* Neck → Feature aggregation
* Head → Bounding box prediction

---

## 6. Training Details

### Dataset

* **Anti-UAV Dataset** (KaggleHub)

---

### Data Preparation (from your training code)

* Extracted frames from videos
* Skipped frames without drones using `exist` flag
* Used bounding box from `gt_rect`
* Converted to YOLO format:

```text
x_center = (x + w/2) / width
y_center = (y + h/2) / height
w = w / width
h = h / height
```

* Generated ~800–1000 images

---

###  Dataset Split

* 80% Training
* 20% Validation

---

###  Training Configuration

* Model: YOLOv8n
* Epochs: 30
* Image Size: 640
* Batch Size: 16

---

###  Training Output

* Model saved as: `best.pt`
* Used for inference pipeline

---

## 7. Results / Output

###  Sample Outputs
<img width="261" height="210" alt="output" src="https://github.com/user-attachments/assets/a15dc4f5-652b-4b7d-aab7-82a198ac2881" />

<img width="261" height="210" alt="lossVs Epoch" src="https://github.com/user-attachments/assets/fa7393a0-944f-4726-84f6-a8471a7a5141" />

<img width="261" height="210" alt="maPVsEpoch" src="https://github.com/user-attachments/assets/69fb13e9-4e8f-4580-be76-547f75a25a98" />

<img width="261" height="210" alt="precVsRecall" src="https://github.com/user-attachments/assets/22d782d0-3ebb-4ba1-8a40-8783d81193e7" />

####  Detection + Intrusion Alert

* Drone detected with bounding box
* Threat level displayed (HIGH)
* Distance and speed shown

#### Dashboard Logs

* Intrusion logs stored and displayed in table format
* Columns:

  * Time
  * Drone ID
  * Distance
  * Speed

    <img width="261" height="210" alt="logs" src="https://github.com/user-attachments/assets/595a606a-a7db-4b62-943c-9b34706dc51a" />


---

### Performance Metrics

* FPS: **10–30** (depends on hardware)
* Real-time processing supported
* Stable tracking using DeepSORT

---

### Observations

* Works well for visible drones
* Struggles with:

  * Very small drones
  * Low-light conditions
  * unseen environments

---

## 8. Setup Instructions

### Installation

```bash
git clone https://github.com/NKGarg1305/drone-intrusion-detection.git
cd drone-intrusion-detection

pip install -r requirements.txt
```

---

### ▶ Run Streamlit Dashboard

```bash
streamlit run app.py
```

---

### ▶ Run Core System

```python
from main import run_pipeline
run_pipeline("video", "video.mp4")
```

---

### ▶ Webcam

```python
run_pipeline("webcam", 0)
```

---

## Project Structure

```text
drone_intrusion/
│
├── main.py
├── preprocessing.py
├── training.py
├── inference.py
├── utils.py
├── config.py
├── logger.py
├── app.py
│
├── models/
├── outputs/
├── logs/
└── README.md
```

---

##  Author

**Naitik Garg**
AIML, Thapar Institute of Engineering & Technology

---

## ⭐ If you like this project

Give it a ⭐ on GitHub!
