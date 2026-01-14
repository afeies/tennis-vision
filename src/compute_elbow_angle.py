import csv
import math
from pathlib import Path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--serve", required=True)
args = parser.parse_args()

SERVE_ID = args.serve

INPUT_CSV = Path("data/processed/csv/feies_right_arm.csv")
OUTPUT_CSV = Path("data/processed/csv/serve1_elbow_angle.csv")

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
    writer.writerow(["frame", "elbow_angle_deg"])
    
    for row in reader:
        frame = int(row["frame"])
        
        shoulder = (float(row["shoulder_x"]), float(row["shoulder_y"]))
        elbow = (float(row["elbow_x"]), float(row["elbow_y"]))
        wrist = (float(row["wrist_x"]), float(row["wrist_y"]))

        angle = angle_between(shoulder, elbow, wrist)

        if angle is not None:
            writer.writerow([frame, angle])

print(f"Saved elbow angle time series to: {OUTPUT_CSV}")