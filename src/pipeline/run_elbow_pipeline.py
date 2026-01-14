import subprocess

SERVES = [
    "feies.mov",
    "federer.mov",
    "alcaraz.mov",
    "murray.mov",
    "sinner.mov",
]

SCRIPTS = [
    "extract_arm_timeseries.py",
    "compute_elbow_angle.py",
    "smooth_elbow_angle.py",
]

for serve in SERVES:
    print(f"Processing {serve}")
    
    for script in SCRIPTS:
        subprocess.run(
            [
                "python3",
                f"src/pipeline/{script}",
                "--serve",
                serve
            ],
            check=True
        )

print("\nAll serves processed successfully")