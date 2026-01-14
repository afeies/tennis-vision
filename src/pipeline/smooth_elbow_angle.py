import csv
from pathlib import Path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--serve", required=True)
args = parser.parse_args()

SERVE_ID = args.serve

INPUT_CSV = Path("data/processed/csv/serve1_elbow_angle.csv")
OUTPUT_CSV = Path("data/processed/csv/serve1_elbow_angle_smoothed.csv")

# small window for minimal distortion
WINDOW_SIZE = 5

def moving_average(values, window):
    smoothed = []
    for i in range(len(values)):
        start = max(0, i - window // 2)
        end = min(len(values), i + window // 2 + 1)
        smoothed.append(sum(values[start:end]) / (end - start))
    return smoothed

frames = []
angles = []

with open(INPUT_CSV, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        frames.append(int(row["frame"]))
        angles.append(float(row["elbow_angle_deg"]))

smoothed_angles = moving_average(angles, WINDOW_SIZE)

with open(OUTPUT_CSV, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["frame", "elbow_angle_deg_smoothed"])
    for frame, angle in zip(frames, smoothed_angles):
        writer.writerow([frame, angle])

print(f"Saved smoothed elbow angle to: {OUTPUT_CSV}")