#!/usr/bin/env python3
"""Static native-config checks; these do not replace Android or iOS builds."""

import hashlib
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
ANDROID = "{http://schemas.android.com/apk/res/android}"
DOMAINS = {
    "root", "file", "database", "sharedpref", "external", "device_root",
    "device_file", "device_database", "device_sharedpref",
}


def require(condition, message):
    if not condition:
        raise SystemExit(message)


def main():
    manifest = ET.parse(ROOT / "android/app/src/main/AndroidManifest.xml").getroot()
    app = manifest.find("application")
    require(app is not None, "Android application element missing")
    require(app.get(ANDROID + "allowBackup") == "false", "Android backup enabled")
    require(
        app.get(ANDROID + "fullBackupContent") == "@xml/backup_rules"
        and app.get(ANDROID + "dataExtractionRules") == "@xml/data_extraction_rules",
        "Android backup rule references changed",
    )
    require(
        not any(item.get(ANDROID + "name") == "android.permission.INTERNET"
                for item in manifest.findall("uses-permission")),
        "Main manifest must not require network access",
    )
    resources = ROOT / "android/app/src/main/res/xml"
    legacy = ET.parse(resources / "backup_rules.xml").getroot()
    modern = ET.parse(resources / "data_extraction_rules.xml").getroot()
    for rules in (legacy, modern.find("cloud-backup"), modern.find("device-transfer")):
        require(rules is not None, "Android backup/transfer rule set missing")
        excluded = {node.get("domain") for node in rules.findall("exclude")
                    if node.get("path") == "."}
        require(DOMAINS <= excluded, "Android backup/transfer exclusion missing")

    settings = (ROOT / "android/settings.gradle.kts").read_text()
    require('version "9.1.0"' in settings, "Unapproved Android Gradle Plugin")
    require('version "2.4.0"' in settings, "Unapproved Kotlin plugin")
    gradle = (ROOT / "android/app/build.gradle.kts").read_text()
    require("minSdk = 24" in gradle, "Android deployment floor changed")
    require('applicationId = "com.example.contractorcalc"' in gradle,
            "Development application identity changed")
    require('signingConfigs.getByName("debug")' not in gradle,
            "Release must not silently use debug signing")
    wrapper = (ROOT / "android/gradle/wrapper/gradle-wrapper.properties").read_text()
    require("gradle-9.3.1-all.zip" in wrapper, "Unapproved Gradle distribution")
    require(
        "distributionSha256Sum=17f277867f6914d61b1aa02efab1ba7bb439ad652ca485cd8ca6842fccec6e43" in wrapper,
        "Gradle distribution checksum missing or changed",
    )
    jar = ROOT / "android/gradle/wrapper/gradle-wrapper.jar"
    require(
        hashlib.sha256(jar.read_bytes()).hexdigest()
        == "b3a875ddc1f044746e1b1a55f645584505f4a10438c1afea9f15e92a7c42ec13",
        "Gradle wrapper JAR checksum mismatch",
    )
    project = (ROOT / "ios/Runner.xcodeproj/project.pbxproj").read_text()
    floors = re.findall(r"IPHONEOS_DEPLOYMENT_TARGET = ([^;]+);", project)
    require(floors and set(floors) == {"15.0"}, "iOS deployment floor changed")
    require("PRODUCT_BUNDLE_IDENTIFIER = com.example.contractorcalc;" in project,
            "iOS development identity changed")
    print("Static platform configuration checks passed; native builds not established.")


if __name__ == "__main__":
    main()
