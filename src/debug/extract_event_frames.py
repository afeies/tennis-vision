import cv2
import csv
from pathlib import Path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--serve", required=True, help="Serve file (e.g., feies.mov)")
args = parser.parse_args()

SERVE_ID = args.serve
SERVE_NAME = Path(SERVE_ID).stem

# Paths
VIDEO_PATH = Path(f"data/raw/{SERVE_ID}")
EVENTS_CSV = Path(f"data/processed/csv/{SERVE_NAME}_elbow_events.csv")
OUTPUT_DIR = Path(f"data/debug/event_frames/{SERVE_NAME}")

# Create output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load events
events = {}
with open(EVENTS_CSV, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        events[row["event"]] = int(row["frame"])

print(f"Extracting frames from {SERVE_ID}:")
print(f"  - Racquet drop @ frame {events.get('racquet_drop', 'N/A')}")
print(f"  - Contact @ frame {events.get('contact', 'N/A')}")

# Open video
cap = cv2.VideoCapture(str(VIDEO_PATH))

for event_name, frame_num in events.items():
    # Seek to frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
    ret, frame = cap.read()

    if ret:
        output_path = OUTPUT_DIR / f"{frame_num:04d}_{event_name}.jpg"
        cv2.imwrite(str(output_path), frame)
        print(f"Saved: {output_path}")
    else:
        print(f"Failed to extract frame {frame_num} for {event_name}")

cap.release()
print(f"\nAll frames saved to: {OUTPUT_DIR}")
