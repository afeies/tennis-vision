import csv
import matplotlib.pyplot as plt
from pathlib import Path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--serve", help="Single serve file (e.g., feies.mov)")
parser.add_argument("--all", action="store_true", help="Plot all serves on one graph")
args = parser.parse_args()

SERVES = ["feies", "federer", "alcaraz", "murray", "sinner"]

def load_serve_data(serve_name):
    csv_path = Path(f"data/processed/csv/{serve_name}_elbow_angle_smoothed.csv")
    frames = []
    angles = []
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            frames.append(int(row["frame"]))
            angles.append(float(row["elbow_angle_deg_smoothed"]))
    return frames, angles

plt.figure(figsize=(10, 4))

if args.all:
    for serve in SERVES:
        try:
            frames, angles = load_serve_data(serve)
            plt.plot(frames, angles, label=serve)
        except FileNotFoundError:
            print(f"Warning: {serve} data not found, skipping")
    plt.legend()
    plt.title("Elbow Angle Over Time - All Serves")
elif args.serve:
    serve_name = Path(args.serve).stem
    frames, angles = load_serve_data(serve_name)
    plt.plot(frames, angles)
    plt.title(f"Elbow Angle Over Time - {serve_name}")
else:
    print("Usage: python plot_elbow_angle.py --serve feies.mov")
    print("       python plot_elbow_angle.py --all")
    exit(1)

plt.xlabel("Frame")
plt.ylabel("Elbow Angle (deg)")
plt.grid(True)
plt.show()
