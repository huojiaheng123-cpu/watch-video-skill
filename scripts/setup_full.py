from __future__ import annotations

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def run(args: list[str]) -> int:
    print("\n$ " + " ".join(args))
    return subprocess.run(args, cwd=ROOT, check=False).returncode


def main() -> int:
    print("Setting up local dependencies for watch-video full mode.")
    print("This script installs repo-local Python and Node dependencies.")
    print("It does not silently install system apps or Codex plugins.")

    failures = 0
    failures += run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]) != 0
    failures += run(["npm", "install"]) != 0
    failures += run(["npx", "playwright", "install", "chromium"]) != 0
    run([sys.executable, "scripts/check_capabilities.py"])

    if failures:
        print("\nSome automatic setup steps failed. Read the missing items above and install them manually.")
        return 1
    print("\nLocal dependencies installed. If FFmpeg or Codex Browser plugin is missing, install those separately.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
