import csv
from pathlib import Path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--serve", required=True)
args = parser.parse_args()

SERVE_ID = args.serve
SERVE_NAME = Path(SERVE_ID).stem

INPUT_CSV = Path(f"data/processed/csv/{SERVE_NAME}_elbow_angle_smoothed.csv")
OUTPUT_CSV = Path(f"data/processed/csv/{SERVE_NAME}_elbow_events.csv")

frames = []
angles = []

with open(INPUT_CSV, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        frames.append(int(row["frame"]))
        angles.append(float(row["elbow_angle_deg_smoothed"]))

# find key events using angle extrema
# racquet drop: minimum elbow angle (maximum flexion)
min_idx = angles.index(min(angles))

# contact: maximum elbow angle (maximum extension) after racquet drop
max_idx = min_idx + angles[min_idx:].index(max(angles[min_idx:]))

events = [
    ("racquet_drop", frames[min_idx], angles[min_idx]),
    ("contact", frames[max_idx], angles[max_idx])
]

with open(OUTPUT_CSV, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["event", "frame", "elbow_angle_deg"])
    for e in events:
        writer.writerow(e)

print(f"Saved elbow events to: {OUTPUT_CSV}")
