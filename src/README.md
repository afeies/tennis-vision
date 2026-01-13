# Common libraries

### pathlib: Object-oriented filesystem paths
https://docs.python.org/3/library/pathlib.html#basic-use

# Source Code Overview
This folder contains scripts for extracting and analyzing biomechanical signals from tennis serve videos using pose estimation

### `run_pose_on_video.py`
Runs pose estimation on a single input video and saves a skeleton-overlay video.
Used to visually validate pose tracking quality.
- input: raw serve video
- output: pose overlay video

### `extract_arm_timeseries.py`
Extracts right arm joint coordinates (shoulder, elbow, wrist) across all frames and saves them as a time series CSV
- input: raw serve video
- output: joint coordinate CSV

### `compute_elbow_angle.py`
Computes right elbow flexion angle over time from joint coordinate data
- input: right arm time series CSV
- output: elbow angle CSV

### `smooth_elbow_angle.py`
Applies a moving average filter to the raw elbow angle signal to reduce frame-to-frame noise and produce a smoother biomechanical curve
- input: raw elbow angle CSV
- output: smoothed elbow angle CSV

### `detect_elbow_events.py`
Detects key serve events from the smoothed elbow angle signal, including maximum elbow flexion (racquet drop) and maximum elbow extension (near contact)
- input: smoothed elbow angle CSV
- output: elbow event CSV

### `normalize_elbow_angle.py`
Aligns and normalizes the elbow angle time series between key serve events (max elbow flexion and max elbow extension). Converts a variable-length serve into a normalized 0-100% serve
- input: smoothed elbow angle CSV and elbow event CSV
- output: normalized elbow angle CSV