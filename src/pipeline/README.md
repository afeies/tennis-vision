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

### subprocess
use Python's `subprocess` module to execute existing scripts as standalone programs.

### argparse
processing scripts in `src` accept command-line argument (like serve ID) using `argparse` so they can be reused by the pipeline

