#!/bin/bash
# Build a macOS-only Firefox copy that doesn't appear in the Dock.
#
# Why: macOS shows every foreground GUI app in the Dock, even when -headless
# means the app has no visible windows. The copy below sets LSUIElement=true
# so the headless Firefox the radio app drives never claims a Dock spot.
# Your personal /Applications/Firefox.app is untouched.
#
# Run once after cloning, and re-run after Firefox updates.
# The output (FirefoxHeadless.app) is gitignored.

set -euo pipefail

if [[ "$(uname)" != "Darwin" ]]; then
  echo "This script is macOS-only." >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="/Applications/Firefox.app"
DST="$SCRIPT_DIR/FirefoxHeadless.app"

if [[ ! -d "$SRC" ]]; then
  echo "Firefox.app not found at $SRC — install Firefox first (brew install --cask firefox)." >&2
  exit 1
fi

echo "Removing any previous copy at $DST"
rm -rf "$DST"

echo "Copying $SRC → $DST (this takes a few seconds)"
cp -R "$SRC" "$DST"

echo "Stripping extended attributes and quarantine flags"
xattr -cr "$DST"

echo "Patching Info.plist: LSUIElement=true (no Dock icon)"
PLIST="$DST/Contents/Info.plist"
if /usr/libexec/PlistBuddy -c "Print :LSUIElement" "$PLIST" >/dev/null 2>&1; then
  /usr/libexec/PlistBuddy -c "Set :LSUIElement true" "$PLIST"
else
  /usr/libexec/PlistBuddy -c "Add :LSUIElement bool true" "$PLIST"
fi

echo "Re-signing bundle with ad-hoc signature"
codesign --force --deep --sign - "$DST" 2>&1 | grep -v "^$" || true

echo
echo "Done. RadioSelenium.py will use this copy automatically on macOS."
echo "Bundle: $DST"
