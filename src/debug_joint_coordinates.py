import cv2
import mediapipe as mp
from pathlib import Path

VIDEO_PATH = Path("data/raw/feies.mov")

mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(str(VIDEO_PATH))

with mp_pose.Pose() as pose:
    ret, frame = cap.read()
    if not ret:
        raise RuntimeError("Failed to read video")

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    if not results.pose_landmarks:
        raise RuntimeError("No pose detected")

    lm = results.pose_landmarks.landmark

    # Right arm landmarks
    shoulder = lm[12]
    elbow = lm[14]
    wrist = lm[16]

    print("Right Shoulder:", shoulder.x, shoulder.y)
    print("Right Elbow:", elbow.x, elbow.y)
    print("Right Wrist:", wrist.x, wrist.y)

cap.release()