# Debug Utilities

This folder contains interactive tools used to visually inspect pose estimation and biomechanical signals frame-by-frame during development

## `view_pose_frame_by_frame`

Interactive video viewer for pose debugging

### Features
- pause / resume playback
- step through video frame-by-frame
- overlay pose landmarks
- display joint statistics on screen

### Controls
- space: play / pause
- n: advance one frame
- q: quit

## `plot_elbow_angle.py`
Plots the smoothed elbow angle over time for a single serve

### Run
`python src/debug/view_pose_frame_by_frame.py`