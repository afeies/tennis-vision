import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

VIDEO_PATH = "data/serve.mov"  # or serve.mp4
MODEL_PATH = "models/pose_landmarker_lite.task"

BaseOptions = python.BaseOptions
PoseLandmarker = vision.PoseLandmarker
PoseLandmarkerOptions = vision.PoseLandmarkerOptions
RunningMode = vision.RunningMode

# read first frame
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    raise RuntimeError(f"Could not open video: {VIDEO_PATH}")

ret, frame = cap.read()
cap.release()
if not ret:
    raise RuntimeError("Could not read first frame. If this is .mov, try converting to .mp4.")

h, w = frame.shape[:2]
rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=RunningMode.IMAGE,
    num_poses=1,
)

with PoseLandmarker.create_from_options(options) as landmarker:
    result = landmarker.detect(mp_image)

if not result.pose_landmarks:
    print("No pose detected in this frame. Try a clearer frame or better lighting.")
else:
    lms = result.pose_landmarks[0]
    print("Landmarks:", len(lms))  # should be 33
    # draw green dots for landmarks
    for lm in lms:
        x, y = int(lm.x * w), int(lm.y * h)
        cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

cv2.imshow("Pose Landmarker (Tasks) - first frame", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()