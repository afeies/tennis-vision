# Tennis Vision: Pre-ML Development Plan

## Current State (Completed)
- MediaPipe pose estimation extracting joint coordinates from videos
- Elbow angle computation, smoothing, and normalization pipeline
- Event detection for racquet drop and contact points
- Basic visualization tools for elbow angle curves
- Processing pipeline for 5 serves (feies, federer, alcaraz, murray, sinner)

## Goal
Build out biomechanics analysis, comparison tools, and feature engineering to prepare for machine learning model training (Week 4 in roadmap).

---

## Phase 1: Expand Biomechanics Analysis (2-3 weeks)

### 1.1 Add Shoulder Angle Analysis
**Purpose**: Shoulder internal/external rotation is critical for serve power and injury prevention.

**Tasks**:
- Create `compute_shoulder_angle.py` - Calculate shoulder rotation using shoulder, elbow, and torso reference points
- Add to pipeline and generate `*_shoulder_angle.csv` for all serves
- Detect shoulder events (max external rotation, max internal rotation)
- Update visualization to show both elbow and shoulder angles

**Output**: `data/processed/csv/*_shoulder_angle.csv`, `*_shoulder_events.csv`

### 1.2 Add Lower Body Analysis
**Purpose**: Leg drive and kinetic chain timing differentiates recreational from pro serves.

**Tasks**:
- Create `compute_knee_angle.py` - Analyze knee flexion/extension (hip-knee-ankle)
- Create `compute_hip_angle.py` - Measure hip rotation
- Detect lower body events (max knee bend, knee extension at contact)
- Extract full-body pose data (currently only extracting right arm)

**Output**: `data/processed/csv/*_knee_angle.csv`, `*_hip_angle.csv`

### 1.3 Kinetic Chain Timing Analysis
**Purpose**: Understand sequencing of body segments (legs → hips → trunk → shoulder → elbow → wrist).

**Tasks**:
- Create `compute_kinetic_chain.py` - Calculate time delays between segment peak velocities
- Measure energy transfer efficiency
- Compare sequencing patterns between user and pro serves

**Output**: `data/processed/csv/*_kinetic_chain.csv`

---

## Phase 2: Data Quality & Validation (1 week)

### 2.1 Pose Tracking Confidence Scoring
**Tasks**:
- Add MediaPipe confidence scores to all extracted coordinates
- Flag frames with low confidence (< 0.5) for manual review
- Create `validate_pose_data.py` - Report tracking quality metrics per serve

**Output**: Quality reports showing % of frames with reliable tracking

### 2.2 Handle Edge Cases
**Tasks**:
- Detect and handle occlusions (player turns away from camera)
- Interpolate missing frames (if confidence drops temporarily)
- Create data cleaning pipeline to filter unreliable serves

**Output**: Cleaned dataset with quality thresholds enforced

### 2.3 Expand Dataset
**Tasks**:
- Record/collect 10-15 more serve videos (mix of skill levels)
- Categorize serves by player type (pro, junior, recreational)
- Document camera setup, angles, and recording guidelines

**Output**: `data/raw/` with 20+ serve videos, `data/metadata.csv` with labels

---

## Phase 3: Serve Comparison & Baseline Metrics (1-2 weeks)

### 3.1 Multi-Serve Overlay Visualization
**Tasks**:
- Update plotting tools to overlay multiple normalized serves on one chart
- Create comparison views (user vs. specific pro, user vs. all pros)
- Add interactive features (toggle serves on/off, zoom to specific phases)

**Output**: Enhanced `plot_elbow_angle.py` and new `plot_serve_comparison.py`

### 3.2 Define Baseline Metrics
**Tasks**:
- Calculate average pro serve metrics (mean angles, ranges, timing)
- Define "good serve" criteria based on pro patterns:
  - Elbow angle at racquet drop (target: 30-50°)
  - Shoulder external rotation at racquet drop (target: 160-180°)
  - Knee extension timing (should lead shoulder rotation)
  - Contact angle consistency
- Create reference ranges for each metric

**Output**: `data/baselines/pro_serve_metrics.json` with statistical ranges

### 3.3 Deviation Analysis
**Tasks**:
- Create `compare_to_baseline.py` - Compute user serve deviations from pro averages
- Generate per-metric scores (e.g., elbow angle similarity: 85/100)
- Identify outlier metrics (angles > 2 standard deviations from mean)

**Output**: `data/processed/analysis/*_deviation_report.csv`

---

## Phase 4: Feature Engineering for ML (1-2 weeks)

### 4.1 Extract Biomechanical Features
**Purpose**: Convert raw angle timeseries into ML-ready feature vectors.

**Tasks**:
- Create `extract_features.py` with feature extraction logic:
  - **Angle features**: min/max/mean/std for each joint angle
  - **Timing features**: frame deltas between key events
  - **Velocity features**: peak angular velocities for each segment
  - **Symmetry features**: left-right body balance metrics
  - **Coordination features**: kinetic chain timing deltas
- Generate feature matrix: rows = serves, columns = features (~30-50 features)
- Save as `data/ml/features.csv`

**Output**: Feature matrix ready for ML training

### 4.2 Define Target Labels
**Tasks**:
- Create labeling scheme for serve quality:
  - **Option A**: Binary (good/bad serve based on deviation threshold)
  - **Option B**: Multi-class (pro/advanced/intermediate/beginner)
  - **Option C**: Regression (overall serve score 0-100)
- Manually label all serves in dataset
- Save labels as `data/ml/labels.csv`

**Output**: Ground truth labels for supervised learning

### 4.3 Feature Analysis & Selection
**Tasks**:
- Compute feature correlations with target labels
- Identify most predictive features (e.g., shoulder rotation, kinetic chain timing)
- Remove redundant/low-variance features
- Create visualization of feature importance

**Output**: Reduced feature set (~15-20 features) with documented rationale

---

## Phase 5: ML Preparation & Data Pipeline (1 week)

### 5.1 Train/Test Split
**Tasks**:
- Split dataset (70% train, 15% validation, 15% test)
- Ensure balanced distribution across serve quality levels
- Document split in `data/ml/splits.json`

**Output**: Stratified dataset splits

### 5.2 Feature Normalization
**Tasks**:
- Standardize features (z-score normalization)
- Save normalization parameters (mean, std) for inference
- Create `preprocess.py` for consistent feature scaling

**Output**: Normalized feature matrices, scaler parameters

### 5.3 Baseline Model Prep
**Tasks**:
- Set up ML training environment (scikit-learn, pandas, matplotlib)
- Create `train_baseline.py` skeleton (ready for Week 4)
- Define evaluation metrics (accuracy, F1, confusion matrix)
- Create model versioning and experiment tracking structure

**Output**: ML training infrastructure ready to go

---

## Deliverables Summary

### Data Pipeline
```
Video → Pose Coordinates → Multi-Joint Angles → Events → Normalization → Features → ML Model
```

### File Structure
```
data/
├── raw/                    # 20+ serve videos with metadata
├── processed/
│   ├── csv/               # Joint coordinates, angles, events, normalized timeseries
│   └── analysis/          # Deviation reports, quality scores
├── baselines/             # Pro serve reference metrics
└── ml/
    ├── features.csv       # Feature matrix (n_serves × n_features)
    ├── labels.csv         # Target labels
    ├── splits.json        # Train/val/test indices
    └── scaler.pkl         # Feature normalization parameters
```

### Scripts Added
```
src/pipeline/
├── compute_shoulder_angle.py
├── compute_knee_angle.py
├── compute_hip_angle.py
├── compute_kinetic_chain.py
├── validate_pose_data.py
├── compare_to_baseline.py
└── extract_features.py

src/visualization/
├── plot_serve_comparison.py
└── plot_feature_importance.py

src/ml/
├── preprocess.py
└── train_baseline.py (skeleton)
```

---

## Success Criteria (Pre-ML Checklist)

- [ ] All 5+ body metrics computed for 20+ serves
- [ ] Data quality validation passed (>80% tracking confidence)
- [ ] Baseline pro metrics documented with statistical ranges
- [ ] Feature matrix generated (20 serves × 20 features minimum)
- [ ] Labels assigned to all serves
- [ ] Train/val/test splits created
- [ ] Visualization tools show clear differences between skill levels
- [ ] Feature analysis shows 3+ highly predictive features
- [ ] ML training pipeline ready to execute

**After completion**: Ready to train baseline classifier (SVM/RandomForest) in Week 4.
