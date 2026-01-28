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
    csv_path = Path(f"data/processed/csv/{serve_name}_knee_angle.csv")
    frames = []
    angles = []
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            frames.append(int(row["frame"]))
            angles.append(float(row["knee_angle_deg"]))
    return frames, angles

def load_events(serve_name):
    """Load knee events if they exist (future implementation)"""
    csv_path = Path(f"data/processed/csv/{serve_name}_knee_events.csv")
    events = {}
    try:
        with open(csv_path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                events[row["event"]] = int(row["frame"])
    except FileNotFoundError:
        pass
    return events

fig, ax = plt.subplots(figsize=(10, 4))
lines = []
original_linewidths = []

if args.all:
    for serve in SERVES:
        try:
            frames, angles = load_serve_data(serve)
            events = load_events(serve)

            line, = ax.plot(frames, angles, label=serve, linewidth=1.5)
            lines.append(line)
            original_linewidths.append(1.5)

            # Plot event markers if they exist (future)
            if "max_knee_bend" in events:
                ax.axvline(events["max_knee_bend"], color='red', linestyle=':', alpha=0.3, linewidth=1)
            if "knee_extension" in events:
                ax.axvline(events["knee_extension"], color='green', linestyle=':', alpha=0.3, linewidth=1)

        except FileNotFoundError:
            print(f"Warning: {serve} data not found, skipping")
    ax.legend()
    ax.set_title("Knee Angle Over Time - All Serves")

    def on_hover(event):
        if event.inaxes != ax:
            return
        for i, line in enumerate(lines):
            if line.contains(event)[0]:
                # Highlight hovered line
                for j, other_line in enumerate(lines):
                    if j == i:
                        other_line.set_linewidth(3.5)
                        other_line.set_alpha(1.0)
                    else:
                        other_line.set_linewidth(1.0)
                        other_line.set_alpha(0.3)
                fig.canvas.draw_idle()
                return
        # Reset all lines if not hovering over any
        for j, line in enumerate(lines):
            line.set_linewidth(original_linewidths[j])
            line.set_alpha(1.0)
        fig.canvas.draw_idle()

    fig.canvas.mpl_connect('motion_notify_event', on_hover)

elif args.serve:
    serve_name = Path(args.serve).stem
    frames, angles = load_serve_data(serve_name)
    events = load_events(serve_name)

    ax.plot(frames, angles, label="Knee angle")

    # Plot event markers if they exist
    if "max_knee_bend" in events:
        ax.axvline(events["max_knee_bend"], color='red', linestyle='--', linewidth=2, label='Max knee bend')
    if "knee_extension" in events:
        ax.axvline(events["knee_extension"], color='green', linestyle='--', linewidth=2, label='Knee extension')

    ax.legend()
    ax.set_title(f"Knee Angle Over Time - {serve_name}")
else:
    print("Usage: python plot_knee_angle.py --serve feies.mov")
    print("       python plot_knee_angle.py --all")
    exit(1)

ax.set_xlabel("Frame")
ax.set_ylabel("Knee Angle (deg)")
ax.grid(True)
plt.show()
