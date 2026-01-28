import csv
import math
from pathlib import Path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--serve", required=True)
args = parser.parse_args()

SERVE_ID = args.serve
SERVE_NAME = Path(SERVE_ID).stem

INPUT_CSV = Path(f"data/processed/csv/{SERVE_NAME}_full_body_pose.csv")
OUTPUT_CSV = Path(f"data/processed/csv/{SERVE_NAME}_shoulder_angle.csv")

# compute angle at point b (in degrees) given points a-b-c
def angle_between(a, b, c):
    ba = (a[0] - b[0], a[1] - b[1])
    bc = (c[0] - b[0], c[1] - b[1])

    dot = ba[0] * bc[0] + ba[1] * bc[1]
    mag_ba = math.sqrt(ba[0]**2 + ba[1]**2)
    mag_bc = math.sqrt(bc[0]**2 + bc[1]**2)

    if mag_ba == 0 or mag_bc == 0:
        return None

    cos_angle = dot / (mag_ba * mag_bc)
    cos_angle = max(-1.0, min(1.0, cos_angle))  # numerical safety
    return math.degrees(math.acos(cos_angle))

with open(INPUT_CSV, "r") as f_in, open(OUTPUT_CSV, "w", newline="") as f_out:
    reader = csv.DictReader(f_in)
    writer = csv.writer(f_out)
    writer.writerow(["frame", "shoulder_angle_deg"])

    for row in reader:
        frame = int(row["frame"])

        # Calculate hip center as torso reference point
        left_hip = (float(row["left_hip_x"]), float(row["left_hip_y"]))
        right_hip = (float(row["right_hip_x"]), float(row["right_hip_y"]))
        hip_center = ((left_hip[0] + right_hip[0]) / 2, (left_hip[1] + right_hip[1]) / 2)

        # Right arm points for serving arm
        shoulder = (float(row["right_shoulder_x"]), float(row["right_shoulder_y"]))
        elbow = (float(row["right_elbow_x"]), float(row["right_elbow_y"]))

        # Shoulder angle: hip_center -> shoulder -> elbow
        # Measures upper arm abduction relative to torso
        angle = angle_between(hip_center, shoulder, elbow)

        if angle is not None:
            writer.writerow([frame, angle])

print(f"Saved shoulder angle time series to: {OUTPUT_CSV}")
