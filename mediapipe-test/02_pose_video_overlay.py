import os
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

VIDEO_PATH = "data/serve.mov"
MODEL_PATH = "models/pose_landmarker_lite.task"
OUT_PATH = "outputs/pose_overlay.mp4"

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

w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# video writer
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = cv2.VideoWriter(OUT_PATH, fourcc, fps, (w, h))
if not writer.isOpened():
    raise RuntimeError("Could not open VideoWriter. Try changing codec/fourcc.")

options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=RunningMode.VIDEO,
    num_poses=1,
)

frame_idx = 0

with PoseLandmarker.create_from_options(options) as landmarker:
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        
        # VIDEO mode requires increasing timestamps in milliseconds
        timestamp_ms = int((frame_idx / fps) * 1000)
        frame_idx += 1
        
        result = landmarker.detect_for_video(mp_image, timestamp_ms)
        
        # draw landmarks as dots
        if result.pose_landmarks:
            lms = result.pose_landmarks[0]
            for lm in lms:
                x, y = int(lm.x * w), int(lm.y * h)
                cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)
        
        # overlay debug text
        cv2.putText(
            frame,
            f"frame={frame_idx} fps={fps:.2f}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (255, 255, 255),
            2
        )
        
        writer.write(frame)
        
        cv2.imshow("Pose overlay (press q to quit)", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.waitKey(0)
cap.release()
writer.release()
cv2.destroyAllWindows()