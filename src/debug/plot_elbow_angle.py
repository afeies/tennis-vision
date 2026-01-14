import csv
import matplotlib.pyplot as plt
from pathlib import Path

CSV_PATH = Path("data/processed/csv/serve1_elbow_angle_smoothed.csv")

frames = []
angles = []

with open(CSV_PATH, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        frames.append(int(row["frame"]))
        angles.append(float(row["elbow_angle_deg_smoothed"]))

plt.figure(figsize=(10, 4))
plt.plot(frames, angles)
plt.xlabel("Frame")
plt.ylabel("Elbow Angle (deg)")
plt.title("Elbow Angle Over Time")
plt.grid(True)
plt.show()