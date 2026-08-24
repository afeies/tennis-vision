# Debug Utilities

This folder contains interactive tools used to visually inspect pose estimation and biomechanical signals frame-by-frame during development

## `view_pose_frame_by_frame`

Interactive video viewer for pose debugging

### Features
- pause / resume playback
- step through video frame-by-frame
- timeline scrubber for jumping to any frame
- overlay pose landmarks
- display joint statistics on screen

### Controls
- space: play / pause
- ← / →: previous / next frame
- timeline slider: drag to jump to any frame
- q: quit and close window

**Note**: Press 'q' to exit the viewer and close the video window.

## `plot_elbow_angle.py`
Plots the smoothed elbow angle over time for a single serve

### Run
`python src/debug/view_pose_frame_by_frame.py`