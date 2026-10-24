#!/usr/bin/env python3
"""Verify this checkout's installed Android toolchain, without starting devices."""

import json
from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent


def package_revision(path, expected_id):
    tree = ET.parse(path)
    package = next(node for node in tree.iter()
                   if node.tag.split("}")[-1] == "localPackage")
    if package.get("path") != expected_id:
        raise ValueError(f"Unexpected package identity at {path}")
    revision = next(node for node in package
                    if node.tag.split("}")[-1] == "revision")
    parts = {node.tag.split("}")[-1]: node.text for node in revision}
    values = [parts.get("major", "0"), parts.get("minor", "0"), parts.get("micro", "0")]
    while len(values) > 1 and values[-1] == "0":
        values.pop()
    if "preview" in parts:
        raise ValueError(f"Preview Android package at {path}")
    return ".".join(values)


def normalized_revision(value):
    parts = value.split(".")
    while len(parts) > 1 and parts[-1] == "0":
        parts.pop()
    return ".".join(parts)


def main():
    baseline = json.loads((ROOT / "tool/android-baseline.json").read_text())
    jdk = ROOT / ".toolchain" / baseline["java"]["directory"]
    sdk = ROOT / ".toolchain/android-sdk"
    try:
        result = subprocess.run(
            [str(jdk / "bin/java"), "-XshowSettings:properties", "-version"],
            capture_output=True, text=True, check=True,
        )
        match = re.search(r"^\s*java.runtime.version = (.+)$", result.stderr, re.MULTILINE)
        if not match or match.group(1).strip() != baseline["java"]["runtime_version"]:
            sys.exit("Installed Java runtime differs from the approved baseline.")
        cli = baseline["command_line_tools"]["version"]
        properties = (sdk / "cmdline-tools" / cli / "source.properties").read_text()
        match = re.search(r"^Pkg.Revision\s*=\s*(.+)$", properties, re.MULTILINE)
        if not match or match.group(1).strip() != cli:
            sys.exit("Installed Android command-line tools differ from the baseline.")
        installed = {}
        for identity, expected in baseline["packages"].items():
            path = sdk.joinpath(*identity.split(";"), "package.xml")
            revision = package_revision(path, identity)
            if revision != normalized_revision(expected):
                sys.exit(f"{identity}: installed {revision}; expected {expected}. No automatic upgrade allowed.")
            installed[identity] = revision
    except (OSError, ValueError, ET.ParseError, StopIteration,
            subprocess.CalledProcessError) as error:
        sys.exit(f"Android toolchain is missing or invalid: {error}")
    print(json.dumps({"java_runtime": baseline["java"]["runtime_version"],
                      "command_line_tools": cli, "packages": installed}, indent=2))


if __name__ == "__main__":
    main()
