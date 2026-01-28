# Visualization Tools for Tennis Serve Biomechanics

Simple tools to make angle measurements and timing patterns easy to understand.

---

## Current Visualizations

### `plot_elbow_angle.py`
**Purpose**: Visualize elbow angle changes throughout serve motion

**Usage**:
```bash
python src/visualization/plot_elbow_angle.py --serve feies.mov  # Single serve
python src/visualization/plot_elbow_angle.py --all              # Compare all serves
```

**Features**:
- Single serve view with event markers (racquet drop, contact)
- Multi-serve overlay with hover interaction
- Frame-by-frame timeline

### `plot_shoulder_angle.py`
**Purpose**: Visualize shoulder angle changes (upper arm abduction relative to torso)

**Usage**:
```bash
python src/visualization/plot_shoulder_angle.py --serve feies.mov  # Single serve
python src/visualization/plot_shoulder_angle.py --all              # Compare all serves
```

### `plot_knee_angle.py`
**Purpose**: Visualize knee flexion/extension for leg drive analysis

**Usage**:
```bash
python src/visualization/plot_knee_angle.py --serve feies.mov  # Single serve
python src/visualization/plot_knee_angle.py --all              # Compare all serves
```

---

## Planned Visualizations

### 1. Multi-Metric Overlay
**Purpose**: Show elbow AND shoulder angles on same timeline

**Why it matters**: Understand timing and coordination (does shoulder rotate before elbow extends?)

**Implementation**: Dual y-axis plot, same as current elbow plot but with both metrics

---

### 2. Stick Figure Animation
**Purpose**: See body position changes frame-by-frame

**Why it matters**: Makes biomechanics visual - easier to understand than numbers

**Implementation**: Draw skeleton using MediaPipe landmarks with matplotlib or OpenCV

---

### 3. Normalized Comparison
**Purpose**: Compare serves of different lengths by aligning them to 0-100% timeline

**Why it matters**: Identify exactly where your serve differs from pros (e.g., "shoulder rotation is late at 60% mark")

**Implementation**: Use existing normalized CSVs, plot multiple serves on same 0-100% x-axis

---

## Design Principles

- **Keep it simple**: Clean layouts, clear labels
- **Add context**: Always show reference lines (pro averages, event markers)
- **Make it useful**: Focus on answering "what should I change?"

---

## Example Workflow

```bash
# Extract pose data
python src/pipeline/extract_full_body_pose.py --serve feies.mov

# Compute angles
python src/pipeline/compute_shoulder_angle.py --serve feies.mov

# Visualize
python src/visualization/plot_elbow_angle.py --serve feies.mov
```
