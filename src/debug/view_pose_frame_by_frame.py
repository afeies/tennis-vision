import cv2
import mediapipe as mp
from pathlib import Path

VIDEO_PATH = Path("data/raw/feies.mov")

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(str(VIDEO_PATH))

paused = True
frame_idx = 0
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Callback for timeline trackbar
def on_trackbar(val):
    global frame_idx, paused
    frame_idx = val
    paused = True

with mp_pose.Pose(
    static_image_mode=False,
    model_complexity=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as pose:

    # Create window and timeline trackbar
    cv2.namedWindow("Pose Debug Viewer")
    cv2.createTrackbar("Frame", "Pose Debug Viewer", 0, total_frames - 1, on_trackbar)

    while cap.isOpened():
        # Set frame position and read
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
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

            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS
            )
            
            # Overlay stats
            cv2.putText(
                frame,
                f"Frame: {frame_idx}",
                (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Elbow: ({elbow.x:.2f}, {elbow.y:.2f})",
                (20, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )
        
        cv2.imshow("Pose Debug Viewer", frame)

        # Update trackbar position
        cv2.setTrackbarPos("Frame", "Pose Debug Viewer", frame_idx)

        # Use short wait even when paused to respond to trackbar changes
        key = cv2.waitKey(1 if paused else 30)

        if key == ord('q'):
            break
        elif key == ord(' '):       # space = toggle pause
            paused = not paused
        elif key in [83, 3, 2555904]:  # right arrow = next frame
            paused = True
            frame_idx = min(total_frames - 1, frame_idx + 1)
        elif key in [81, 2, 2424832]:  # left arrow = previous frame
            paused = True
            frame_idx = max(0, frame_idx - 1)

        # Auto-advance if playing
        if not paused:
            frame_idx = min(total_frames - 1, frame_idx + 1)

cap.release()
cv2.destroyAllWindows()