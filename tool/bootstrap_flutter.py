#!/usr/bin/env python3
"""Install only the approved Flutter archive into this checkout's .toolchain."""

import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import urllib.request

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://storage.googleapis.com/flutter_infra_release/releases"


def main():
    baseline = json.loads((ROOT / "tool/flutter-baseline.json").read_text())
    system = {"Linux": "linux", "Darwin": "macos"}.get(platform.system())
    arch = {"x86_64": "x64", "arm64": "arm64", "aarch64": "arm64"}.get(
        platform.machine()
    )
    selected = baseline["archives"].get(f"{system}-{arch}")
    if selected is None:
        sys.exit("No approved SDK archive for this host. Do not substitute latest.")

    home = ROOT / ".toolchain"
    sdk = home / "flutter"
    if sdk.exists():
        print(f"SDK already exists at {sdk}; run tool/check_toolchain.py to verify it.")
        return
    if home.is_symlink():
        sys.exit("Refusing a symlinked .toolchain directory.")
    home.mkdir(exist_ok=True)
    with urllib.request.urlopen(
        f"{BASE_URL}/{selected['manifest']}", timeout=60
    ) as response:
        manifest = json.load(response)
    matches = [
        entry for entry in manifest["releases"]
        if entry["hash"] == baseline["revision"]
        and entry["version"] == baseline["version"]
        and entry["channel"] == baseline["channel"]
        and entry["archive"] == selected["path"]
        and entry["sha256"] == selected["sha256"]
        and entry["dart_sdk_version"] == baseline["dart_version"]
    ]
    if len(matches) != 1:
        sys.exit("Official release metadata does not match the approved baseline.")

    archive = home / Path(selected["path"]).name
    partial = archive.with_suffix(archive.suffix + ".partial")
    print(f"Downloading {selected['path']}", flush=True)
    digest = hashlib.sha256()
    with urllib.request.urlopen(
        f"{BASE_URL}/{selected['path']}", timeout=120
    ) as response, partial.open("wb") as output:
        while chunk := response.read(1024 * 1024):
            digest.update(chunk)
            output.write(chunk)
    if digest.hexdigest() != selected["sha256"]:
        sys.exit(f"SDK checksum mismatch; retained untrusted download at {partial}.")
    os.replace(partial, archive)
    print(f"Verified SHA-256: {digest.hexdigest()}", flush=True)
    if archive.suffix == ".zip":
        subprocess.run(["unzip", "-q", str(archive), "-d", str(home)], check=True)
    else:
        subprocess.run(["tar", "-xf", str(archive), "-C", str(home)], check=True)
    print(f"SDK extracted to {sdk}; no global PATH or configuration changed.")


if __name__ == "__main__":
    main()
