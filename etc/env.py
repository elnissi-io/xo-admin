import os
from pathlib import Path

# Determine paths
script_path = Path(__file__).resolve()
working_dir = script_path.parent.parent
src = working_dir / "src"
debug = True
# Environment variables to set in .env file
env_vars = {
    "WORKINGDIR": str(working_dir),
    "PYTHONPATH": str(src),
    "DEBUG": debug,
}
# Write to .env file
env_path = working_dir / ".env"
with env_path.open("w") as f:
    for key, value in env_vars.items():
        f.write(f"{key}={value}\n")

print(f"Dev Environment variables set in {env_path}")
