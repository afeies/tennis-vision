import os
import csv
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

VIDEO_PATH = "data/serve.mov"
MODEL_PATH = "models/pose_landmarker_lite.task"
OUT_CSV = "outputs/landmarks.csv"

os.makedirs("outputs", exist_ok=True)

BaseOptions = python.BaseOptions
PoseLandmarker = vision.PoseLandmarker
PoseLandmarkerOptions = vision.PoseLandmarkerOptions
RunningMode = vision.RunningMode

cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    raise RuntimeError(f"Could not open video: {VIDEO_PATH}")

fps = cap.get(cv2.CAP_PROP_FPS)
if fps <= 0:
    fps = 30.0

# landmark names (33)
LM_NAMES = [lm.name for lm in mp.solutions.pose.PoseLandmark] if hasattr(mp, "solutions") else [
    "NOSE","LEFT_EYE_INNER","LEFT_EYE","LEFT_EYE_OUTER","RIGHT_EYE_INNER","RIGHT_EYE","RIGHT_EYE_OUTER",
    "LEFT_EAR","RIGHT_EAR","MOUTH_LEFT","MOUTH_RIGHT",
    "LEFT_SHOULDER","RIGHT_SHOULDER","LEFT_ELBOW","RIGHT_ELBOW","LEFT_WRIST","RIGHT_WRIST",
    "LEFT_PINKY","RIGHT_PINKY","LEFT_INDEX","RIGHT_INDEX","LEFT_THUMB","RIGHT_THUMB",
    "LEFT_HIP","RIGHT_HIP","LEFT_KNEE","RIGHT_KNEE","LEFT_ANKLE","RIGHT_ANKLE",
    "LEFT_HEEL","RIGHT_HEEL","LEFT_FOOT_INDEX","RIGHT_FOOT_INDEX"
]

# build header: time + each landmark's fields
header = ["frame", "time_s"]
for name in LM_NAMES:
    header += [f"{name}_x", f"{name}_y", f"{name}_z", f"{name}_vis"]

options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=RunningMode.VIDEO,
    num_poses=1
)

frame_idx = 0

with open(OUT_CSV, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    
    with PoseLandmarker.create_from_options(options) as landmarker:
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

            timestamp_ms = int((frame_idx / fps) * 1000)
            t = frame_idx / fps

            result = landmarker.detect_for_video(mp_image, timestamp_ms)

            row = [frame_idx, f"{t:.6f}"]

            if result.pose_landmarks:
                lms = result.pose_landmarks[0]  # 33 landmarks
                # each lm has x,y,z plus visibility (0..1-ish)
                for lm in lms:
                    row += [f"{lm.x:.6f}", f"{lm.y:.6f}", f"{lm.z:.6f}", f"{lm.visibility:.6f}"]
            else:
                # no detection this frame: write blanks
                row += [""] * (33 * 4)

            writer.writerow(row)
            frame_idx += 1

cap.release()
print(f"Saved: {OUT_CSV}")   