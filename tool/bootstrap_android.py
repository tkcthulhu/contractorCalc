#!/usr/bin/env python3
"""Install the pinned Linux JDK and Android CLI without global changes."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent


def download(selected, destination):
    if destination.exists():
        digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    else:
        partial = destination.with_suffix(destination.suffix + ".partial")
        digest = hashlib.sha256()
        print(f"Downloading {selected['url']}", flush=True)
        with urllib.request.urlopen(selected["url"], timeout=120) as response, \
                partial.open("wb") as output:
            while chunk := response.read(1024 * 1024):
                digest.update(chunk)
                output.write(chunk)
        digest = digest.hexdigest()
        if digest == selected["sha256"]:
            os.replace(partial, destination)
    if digest != selected["sha256"]:
        sys.exit(f"Archive checksum mismatch: {destination}; refusing extraction.")
    print(f"Verified {destination.name}: {digest}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--accept-sdk-license", action="store_true",
        help="Confirm you reviewed and accept the exact SDK agreement in the baseline.",
    )
    args = parser.parse_args()
    baseline = json.loads((ROOT / "tool/android-baseline.json").read_text())
    if platform.system() != "Linux" or platform.machine() != "x86_64":
        sys.exit("This Android tool archive selection is approved for Linux x64 only.")
    if not args.accept_sdk_license:
        sys.exit(
            "Review the Android SDK License Agreement first. Explicit acceptance "
            "requires --accept-sdk-license; no terms are accepted by default."
        )
    selected_license = baseline["sdk_license"]
    with urllib.request.urlopen(selected_license["source"], timeout=60) as response:
        repository = ET.fromstring(response.read())
    text = next(node.text for node in repository.findall("license")
                if node.get("id") == selected_license["id"])
    if hashlib.sha256(text.encode()).hexdigest() != selected_license["sha256"]:
        sys.exit("SDK license text changed; stop and review the new agreement.")

    home = ROOT / ".toolchain"
    if home.is_symlink():
        sys.exit("Refusing a symlinked toolchain directory.")
    downloads = home / "android-downloads"
    downloads.mkdir(parents=True, exist_ok=True)
    java = baseline["java"]
    jdk = home / java["directory"]
    if not jdk.exists():
        archive = downloads / "temurin-jdk-21.0.13+9.tar.gz"
        download(java, archive)
        subprocess.run(["tar", "-xf", str(archive), "-C", str(home)], check=True)
    cli = baseline["command_line_tools"]
    parent = home / "android-sdk/cmdline-tools"
    target = parent / cli["version"]
    if not target.exists():
        archive = downloads / "commandlinetools-linux-15859902.zip"
        download(cli, archive)
        extraction = parent / (".extract-" + cli["version"])
        extraction.mkdir(parents=True, exist_ok=False)
        subprocess.run(["unzip", "-q", str(archive), "-d", str(extraction)], check=True)
        (extraction / "cmdline-tools").rename(target)
        extraction.rmdir()
    print("JDK and Android CLI installed locally. Source tool/android_env.sh.")
    print("SDK packages/license receipt and native build verification remain separate.")


if __name__ == "__main__":
    main()
