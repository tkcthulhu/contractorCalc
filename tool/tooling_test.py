import contextlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import bootstrap_android
import bootstrap_flutter
import check_platforms
import check_toolchain


class ToolchainCheckTest(unittest.TestCase):
    def setUp(self):
        baseline = json.loads(
            (check_toolchain.ROOT / "tool/flutter-baseline.json").read_text()
        )
        self.identity = {
            "frameworkVersion": baseline["version"],
            "frameworkRevision": baseline["revision"],
            "channel": baseline["channel"],
            "dartSdkVersion": baseline["dart_version"],
        }

    def run_check(self, identity):
        result = subprocess.CompletedProcess([], 0, json.dumps(identity), "")
        with patch("check_toolchain.subprocess.run", return_value=result), \
                contextlib.redirect_stdout(io.StringIO()):
            check_toolchain.main()

    def test_accepts_exact_identity(self):
        self.run_check(self.identity)

    def test_refuses_each_mismatched_identity_field(self):
        for field in self.identity:
            with self.subTest(field=field), self.assertRaisesRegex(
                SystemExit, "Toolchain mismatch"
            ):
                self.run_check({**self.identity, field: "unapproved"})

    def test_missing_flutter_is_not_a_pass(self):
        with patch("check_toolchain.subprocess.run", side_effect=FileNotFoundError), \
                self.assertRaisesRegex(SystemExit, "Cannot inspect Flutter"):
            check_toolchain.main()

    def test_invalid_version_output_is_not_a_pass(self):
        result = subprocess.CompletedProcess([], 0, "not JSON", "")
        with patch("check_toolchain.subprocess.run", return_value=result), \
                self.assertRaisesRegex(SystemExit, "Cannot inspect Flutter"):
            check_toolchain.main()


class BootstrapTest(unittest.TestCase):
    def test_unsupported_host_refuses_before_network_access(self):
        with patch("bootstrap_flutter.platform.system", return_value="Unsupported"), \
                patch("bootstrap_flutter.urllib.request.urlopen") as network, \
                self.assertRaisesRegex(SystemExit, "No approved SDK archive"):
            bootstrap_flutter.main()
        network.assert_not_called()

    def test_checksum_mismatch_never_extracts_sdk(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "tool").mkdir()
            baseline = {
                "version": "selected", "revision": "commit", "channel": "stable",
                "dart_version": "dart",
                "archives": {"linux-x64": {
                    "manifest": "manifest.json", "path": "archive.tar.xz",
                    "sha256": "0" * 64,
                }},
            }
            (root / "tool/flutter-baseline.json").write_text(json.dumps(baseline))
            manifest = {"releases": [{
                "version": "selected", "hash": "commit", "channel": "stable",
                "dart_sdk_version": "dart", "archive": "archive.tar.xz",
                "sha256": "0" * 64,
            }]}
            responses = [io.BytesIO(json.dumps(manifest).encode()), io.BytesIO(b"bad")]
            with patch("bootstrap_flutter.ROOT", root), \
                    patch("bootstrap_flutter.platform.system", return_value="Linux"), \
                    patch("bootstrap_flutter.platform.machine", return_value="x86_64"), \
                    patch("bootstrap_flutter.urllib.request.urlopen", side_effect=responses), \
                    patch("bootstrap_flutter.subprocess.run") as extract, \
                    contextlib.redirect_stdout(io.StringIO()), \
                    self.assertRaisesRegex(SystemExit, "SDK checksum mismatch"):
                bootstrap_flutter.main()
            extract.assert_not_called()
            self.assertFalse((root / ".toolchain/flutter").exists())


class AndroidBootstrapTest(unittest.TestCase):
    def test_sdk_license_acceptance_is_never_implicit(self):
        with patch("sys.argv", ["bootstrap_android.py"]), \
                patch("bootstrap_android.platform.system", return_value="Linux"), \
                patch("bootstrap_android.platform.machine", return_value="x86_64"), \
                patch("bootstrap_android.urllib.request.urlopen") as network, \
                self.assertRaisesRegex(SystemExit, "Review the Android SDK License"):
            bootstrap_android.main()
        network.assert_not_called()

    def test_changed_license_requires_new_review(self):
        repository = b'<root><license id="android-sdk-license">changed</license></root>'
        with patch("sys.argv", ["bootstrap_android.py", "--accept-sdk-license"]), \
                patch("bootstrap_android.platform.system", return_value="Linux"), \
                patch("bootstrap_android.platform.machine", return_value="x86_64"), \
                patch("bootstrap_android.urllib.request.urlopen", return_value=io.BytesIO(repository)), \
                self.assertRaisesRegex(SystemExit, "SDK license text changed"):
            bootstrap_android.main()

    def test_cached_corrupt_archive_is_refused_without_download(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "archive.zip"
            archive.write_bytes(b"corrupt")
            with patch("bootstrap_android.urllib.request.urlopen") as network, \
                    self.assertRaisesRegex(SystemExit, "Archive checksum mismatch"):
                bootstrap_android.download({"sha256": "0" * 64}, archive)
            network.assert_not_called()


class PlatformCheckTest(unittest.TestCase):
    def test_enabled_android_backup_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = root / "android/app/src/main/AndroidManifest.xml"
            manifest.parent.mkdir(parents=True)
            manifest.write_text(
                '<manifest xmlns:android="http://schemas.android.com/apk/res/android">'
                '<application android:allowBackup="true" /></manifest>'
            )
            with patch("check_platforms.ROOT", root), self.assertRaisesRegex(
                SystemExit, "Android backup enabled"
            ):
                check_platforms.main()


if __name__ == "__main__":
    unittest.main()
