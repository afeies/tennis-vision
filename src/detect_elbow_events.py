import csv
from pathlib import Path

INPUT_CSV = Path("output/pose_videos/serve1_elbow_angle_smoothed.csv")
OUTPUT_CSV = Path("output/pose_videos/serve1_elbow_events.csv")

frames = []
angles = []

with open(INPUT_CSV, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        frames.append(int(row["frame"]))
        angles.append(float(row["elbow_angle_deg_smoothed"]))

# find key events
min_angle = min(angles)
max_angle = max(angles)

min_idx = angles.index(min_angle)
max_idx = angles.index(max_angle)

events = [
    ("max_flexion", frames[min_idx], min_angle),
    ("max_extension", frames[max_idx], max_angle)
]

with open(OUTPUT_CSV, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["event", "frame", "elbow_angle_deg"])
    for e in events:
        writer.writerow(e)

print(f"Saved elbow events to: {OUTPUT_CSV}")