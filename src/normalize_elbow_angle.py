import csv
from pathlib import Path

# Paths
ANGLE_CSV = Path("data/processed/csv/serve1_elbow_angle_smoothed.csv")
EVENT_CSV = Path("data/processed/csv/serve1_elbow_events.csv")
OUTPUT_CSV = Path("data/processed/csv/serve1_elbow_angle_normalized.csv")

# Read smoothed elbow angles
frames = []
angles = []

with open(ANGLE_CSV, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        frames.append(int(row["frame"]))
        angles.append(float(row["elbow_angle_deg_smoothed"]))

# Read detected events
event_frames = {}

with open(EVENT_CSV, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        event_frames[row["event"]] = int(row["frame"])

# racquet drop
start_frame = event_frames["max_flexion"]
# contact
end_frame = event_frames["max_extension"]
print(start_frame, end_frame)

if start_frame >= end_frame:
    raise ValueError("Invalid event ordering for normalization")

# Extract segment between key events
segment_frames = []
segment_angles = []

for frame, angle in zip(frames, angles):
    if start_frame <= frame <= end_frame:
        segment_frames.append(frame)
        segment_angles.append(angle)

num_points = len(segment_angles)

# Normalize time to 0-100%
normalized_data = []

for i, angle in enumerate(segment_angles):
    percent = (i / (num_points - 1)) * 100
    normalized_data.append((percent, angle))

# Save normalized signal
with open(OUTPUT_CSV, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["serve_phase_percent", "elbow_angle_deg"])
    for row in normalized_data:
        writer.writerow(row)

print(f"Saved normalized elbow angle to: {OUTPUT_CSV}")