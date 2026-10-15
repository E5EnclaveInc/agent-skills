#!/usr/bin/env bash
# Example iOS project patch (runs after `cap add ios`, before archive).
# The native project is generated fresh each build; every platform decision lives here.
set -euo pipefail
PL="ios/App/App/Info.plist"
PB="/usr/libexec/PlistBuddy"

echo "== Info.plist: landscape-only, hidden status bar, deep links =="

# Landscape only (iPhone + iPad)
$PB -c "Delete :UISupportedInterfaceOrientations" "$PL" 2>/dev/null || true
$PB -c "Add :UISupportedInterfaceOrientations array" "$PL"
$PB -c "Add :UISupportedInterfaceOrientations:0 string UIInterfaceOrientationLandscapeLeft" "$PL"
$PB -c "Add :UISupportedInterfaceOrientations:1 string UIInterfaceOrientationLandscapeRight" "$PL"
$PB -c "Delete :UISupportedInterfaceOrientations~ipad" "$PL" 2>/dev/null || true
$PB -c "Add :UISupportedInterfaceOrientations~ipad array" "$PL"
$PB -c "Add :UISupportedInterfaceOrientations~ipad:0 string UIInterfaceOrientationLandscapeLeft" "$PL"
$PB -c "Add :UISupportedInterfaceOrientations~ipad:1 string UIInterfaceOrientationLandscapeRight" "$PL"

# Full-screen game chrome
$PB -c "Delete :UIStatusBarHidden" "$PL" 2>/dev/null || true
$PB -c "Add :UIStatusBarHidden bool true" "$PL"
$PB -c "Delete :UIViewControllerBasedStatusBarAppearance" "$PL" 2>/dev/null || true
$PB -c "Add :UIViewControllerBasedStatusBarAppearance bool false" "$PL"
$PB -c "Delete :UIRequiresFullScreen" "$PL" 2>/dev/null || true
$PB -c "Add :UIRequiresFullScreen bool true" "$PL"

# Unlock ProMotion (120 Hz) for the render loop
$PB -c "Delete :CADisableMinimumFrameDurationOnPhone" "$PL" 2>/dev/null || true
$PB -c "Add :CADisableMinimumFrameDurationOnPhone bool true" "$PL"

# App deep links: exampleapp://open?<params>
$PB -c "Delete :CFBundleURLTypes" "$PL" 2>/dev/null || true
$PB -c "Add :CFBundleURLTypes array" "$PL"
$PB -c "Add :CFBundleURLTypes:0 dict" "$PL"
$PB -c "Add :CFBundleURLTypes:0:CFBundleURLName string com.example.app" "$PL"
$PB -c "Add :CFBundleURLTypes:0:CFBundleURLSchemes array" "$PL"
$PB -c "Add :CFBundleURLTypes:0:CFBundleURLSchemes:0 string exampleapp" "$PL"

# Monotonic build number so every OTA reinstall is a clean upgrade
BUILD_NUM=$(date -u +%y%m%d%H%M)
$PB -c "Delete :CFBundleVersion" "$PL" 2>/dev/null || true
$PB -c "Add :CFBundleVersion string $BUILD_NUM" "$PL"
echo "CFBundleVersion -> $BUILD_NUM"

# Export compliance: no non-exempt encryption -> no per-build questionnaire
$PB -c "Delete :ITSAppUsesNonExemptEncryption" "$PL" 2>/dev/null || true
$PB -c "Add :ITSAppUsesNonExemptEncryption bool false" "$PL"

echo "Info.plist patched:"
$PB -c "Print :UISupportedInterfaceOrientations" "$PL"

# Optional universal links: export UL_DOMAIN=circuit.example.com before running
if [ -n "${UL_DOMAIN:-}" ]; then
  ENT="ios/App/App/App.entitlements"
  if [ ! -f "$ENT" ]; then
    cat > "$ENT" <<'XML'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict/></plist>
XML
  fi
  $PB -c "Delete :com.apple.developer.associated-domains" "$ENT" 2>/dev/null || true
  $PB -c "Add :com.apple.developer.associated-domains array" "$ENT"
  $PB -c "Add :com.apple.developer.associated-domains:0 string applinks:${UL_DOMAIN}" "$ENT"
  echo "universal links entitlement added for ${UL_DOMAIN}"
fi
