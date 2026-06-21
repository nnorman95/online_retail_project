import subprocess
import sys

steps = [
    "scripts/load_raw.py",
    "scripts/build_models.py",
]

for script in steps:
    print(f"Running {script}...")
    subprocess.run([sys.executable, script], check=True)

print("Pipeline finished successfully!")