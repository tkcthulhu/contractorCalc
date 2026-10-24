#!/usr/bin/env bash
set -euo pipefail
source "$(dirname -- "${BASH_SOURCE[0]}")/env.sh"
cd "$CONTRACTORCALC_ROOT"

python3 tool/check_toolchain.py
python3 -m unittest discover -s tool -p '*_test.py' -v
python3 tool/check_platforms.py
flutter pub get --enforce-lockfile
dart run build_runner build
dart format --output=none --set-exit-if-changed lib test
flutter analyze --no-pub
flutter test --no-pub --reporter expanded

git diff --exit-code -- pubspec.lock '*.g.dart'
if [[ -n "$(git ls-files --others --exclude-standard -- '*.g.dart')" ]]; then
  printf '%s\n' 'Generated Dart outputs are untracked; inspect and retain them.' >&2
  exit 1
fi
