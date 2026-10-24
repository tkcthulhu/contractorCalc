#!/usr/bin/env bash
# Source this file from a Bash shell before running Flutter commands.
CONTRACTORCALC_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
export PATH="$CONTRACTORCALC_ROOT/.toolchain/flutter/bin:$PATH"
export PUB_CACHE="$CONTRACTORCALC_ROOT/.local/pub-cache"
export GRADLE_USER_HOME="$CONTRACTORCALC_ROOT/.local/gradle"
export XDG_CACHE_HOME="$CONTRACTORCALC_ROOT/.local/cache"
export XDG_CONFIG_HOME="$CONTRACTORCALC_ROOT/.local/config"
export FLUTTER_SUPPRESS_ANALYTICS=true
export DART_SUPPRESS_ANALYTICS=true
