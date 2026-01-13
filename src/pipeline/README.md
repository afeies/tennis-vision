# Pipeline Scripts
This folder contains scripts that run multiple processing steps in sequence for one or more serve videos

### `run_elbow_pipeline.py`
- Runs the full elbow-angle processing pipeline for all serve videos found in `raw_videos`
- For each serve video, this script executes the following
1. extract right arm joint coordinates
2. compute elbow angle over time
3. smooth the elbow angle signal

### subprocess
use Python's `subprocess` module to execute existing scripts as standalone programs.

### argparse
processing scripts in `src` accept command-line argument (like serve ID) using `argparse` so they can be reused by the pipeline

