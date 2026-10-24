#!/usr/bin/env bash
# Source this only for this checkout's local Android toolchain.
source "$(dirname -- "${BASH_SOURCE[0]}")/env.sh"
export JAVA_HOME="$CONTRACTORCALC_ROOT/.toolchain/jdk-21.0.13+9"
export ANDROID_HOME="$CONTRACTORCALC_ROOT/.toolchain/android-sdk"
export ANDROID_USER_HOME="$CONTRACTORCALC_ROOT/.local/android-user"
export ANDROID_AVD_HOME="$CONTRACTORCALC_ROOT/.local/android-avd"
export ANDROID_EMULATOR_HOME="$CONTRACTORCALC_ROOT/.local/android-emulator"
export ANDROID_ADB_SERVER_PORT="${CONTRACTORCALC_ADB_PORT:-5038}"
export ADB_SERVER_SOCKET="tcp:127.0.0.1:$ANDROID_ADB_SERVER_PORT"
export PATH="$JAVA_HOME/bin:$ANDROID_HOME/cmdline-tools/22.0/bin:$ANDROID_HOME/platform-tools:$ANDROID_HOME/emulator:$PATH"
