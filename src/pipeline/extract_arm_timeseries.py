import cv2
import csv
import mediapipe as mp
from pathlib import Path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--serve", required=True)
args = parser.parse_args()

SERVE_ID = args.serve

# -------- Paths --------
VIDEO_PATH = Path("data/raw/feies.mov")
OUTPUT_CSV = Path("data/processed/csv/feies_right_arm.csv")
OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
# -----------------------

mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(str(VIDEO_PATH))

with mp_pose.Pose(
    static_image_mode=False,
    model_complexity=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as pose, open(OUTPUT_CSV, "w", newline="") as f:

    writer = csv.writer(f)
    writer.writerow([
        "frame",
        "shoulder_x", "shoulder_y",
        "elbow_x", "elbow_y",
        "wrist_x", "wrist_y"
    ])

    frame_idx = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark

            shoulder = lm[12]
            elbow = lm[14]
            wrist = lm[16]

            writer.writerow([
                frame_idx,
                shoulder.x, shoulder.y,
                elbow.x, elbow.y,
                wrist.x, wrist.y
            ])

        frame_idx += 1

cap.release()
print(f"Saved right arm time series to: {OUTPUT_CSV}")