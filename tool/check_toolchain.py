#!/usr/bin/env python3
"""Refuse unapproved Flutter/Dart versions before resolution or verification."""

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent


def main():
    baseline = json.loads((ROOT / "tool/flutter-baseline.json").read_text())
    try:
        result = subprocess.run(
            ["flutter", "--version", "--machine"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        actual = json.loads(result.stdout)
    except (OSError, subprocess.CalledProcessError, json.JSONDecodeError) as error:
        sys.exit(f"Cannot inspect Flutter: {error}. Source tool/env.sh first.")
    expected = {
        "frameworkVersion": baseline["version"],
        "frameworkRevision": baseline["revision"],
        "channel": baseline["channel"],
        "dartSdkVersion": baseline["dart_version"],
    }
    mismatches = {
        key: {"expected": value, "actual": actual.get(key)}
        for key, value in expected.items() if actual.get(key) != value
    }
    if mismatches:
        sys.exit("Toolchain mismatch:\n" + json.dumps(mismatches, indent=2))
    print(json.dumps(actual, indent=2))


if __name__ == "__main__":
    main()
