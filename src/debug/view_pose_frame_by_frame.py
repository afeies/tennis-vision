import cv2
import mediapipe as mp
from pathlib import Path

VIDEO_PATH = Path("data/raw/feies.mov")

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(str(VIDEO_PATH))

paused = True
frame_idx = 0

with mp_pose.Pose(
    static_image_mode=False,
    model_complexity=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as pose:
    
    while cap.isOpened():
        if not paused:
            ret, frame = cap.read()
            if not ret:
                break
            frame_idx += 1
        else:
            # If paused, don't advance frame
            ret, frame = cap.read()
            if not ret:
                break
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        
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
        
        key = cv2.waitKey(0 if paused else 30)
        
        if key == ord('q'):
            break
        elif key == ord(' '):       # space = toggle pause
            paused = not paused
        elif key == ord('n'):       # n = next frame
            paused = True
            frame_idx += 1
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)

cap.release()
cv2.destroyAllWindows()