# Pipeline Scripts
This folder contains scripts that run multiple processing steps in sequence for one or more serve videos

### `run_elbow_pipeline.py`
- Runs the full elbow-angle processing pipeline for all serve videos found in `data/raw`
- For each serve video, this script executes the following
1. extract right arm joint coordinates
2. compute elbow angle over time
3. smooth the elbow angle signal

### `extract_full_body_pose.py`
- Extracts full body joint coordinates from serve video using MediaPipe
- Captures arms, torso, and legs for comprehensive biomechanics analysis
- Output: CSV with shoulders, elbows, wrists, hips, knees, ankles (24 columns)

### `compute_shoulder_angle.py`
- Calculates shoulder angle from hip_center → shoulder → elbow
- Measures upper arm abduction relative to torso
- Output: CSV with frame and shoulder_angle_deg

### `compute_knee_angle.py`
- Calculates knee angle from hip → knee → ankle
- Measures knee flexion/extension (important for leg drive)
- Output: CSV with frame and knee_angle_deg

### `compute_hip_angle.py`
- Calculates hip angle from shoulder → hip → knee
- Measures hip flexion/extension and torso positioning
- Output: CSV with frame and hip_angle_deg

### subprocess
use Python's `subprocess` module to execute existing scripts as standalone programs.

### argparse
processing scripts in `src` accept command-line argument (like serve ID) using `argparse` so they can be reused by the pipeline

