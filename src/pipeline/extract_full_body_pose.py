import cv2
import csv
import mediapipe as mp
from pathlib import Path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--serve", required=True)
args = parser.parse_args()

SERVE_ID = args.serve
SERVE_NAME = Path(SERVE_ID).stem

# -------- Paths --------
VIDEO_PATH = Path(f"data/raw/{SERVE_ID}")
OUTPUT_CSV = Path(f"data/processed/csv/{SERVE_NAME}_full_body_pose.csv")
OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
# -----------------------

mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(str(VIDEO_PATH))

# Configure MediaPipe Pose with highest accuracy model (complexity=2)
# Tracking mode enabled (static_image_mode=False) for video processing
with mp_pose.Pose(
    static_image_mode=False,
    model_complexity=2,  # 0=lite, 1=full, 2=heavy (most accurate)
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as pose, open(OUTPUT_CSV, "w", newline="") as f:

    writer = csv.writer(f)
    writer.writerow([
        "frame",
        "right_shoulder_x", "right_shoulder_y",
        "right_elbow_x", "right_elbow_y",
        "right_wrist_x", "right_wrist_y",
        "left_shoulder_x", "left_shoulder_y",
        "left_elbow_x", "left_elbow_y",
        "left_wrist_x", "left_wrist_y",
        "left_hip_x", "left_hip_y",
        "right_hip_x", "right_hip_y",
        "left_knee_x", "left_knee_y",
        "right_knee_x", "right_knee_y",
        "left_ankle_x", "left_ankle_y",
        "right_ankle_x", "right_ankle_y"
    ])

    frame_idx = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # MediaPipe expects RGB input (OpenCV reads BGR by default)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark

            # Extract landmarks using MediaPipe's landmark index system
            # Full reference: https://google.github.io/mediapipe/solutions/pose.html
            writer.writerow([
                frame_idx,
                lm[12].x, lm[12].y,  # right shoulder
                lm[14].x, lm[14].y,  # right elbow
                lm[16].x, lm[16].y,  # right wrist
                lm[11].x, lm[11].y,  # left shoulder
                lm[13].x, lm[13].y,  # left elbow
                lm[15].x, lm[15].y,  # left wrist
                lm[23].x, lm[23].y,  # left hip
                lm[24].x, lm[24].y,  # right hip
                lm[25].x, lm[25].y,  # left knee
                lm[26].x, lm[26].y,  # right knee
                lm[27].x, lm[27].y,  # left ankle
                lm[28].x, lm[28].y   # right ankle
            ])

        frame_idx += 1

cap.release()
print(f"Saved full body pose to: {OUTPUT_CSV}")
