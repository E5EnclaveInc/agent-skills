#!/usr/bin/env python3
"""iOS Ship — the IPA verification GATE.

Open a built .ipa and PROVE it is installable before anyone taps INSTALL.
This is the gate that caught the boot-stall and manifest-version defects on a
real delivery — never ship an Ad Hoc IPA to a human without it.

Usage:
  python3 verify_ipa.py <ipa_path> \
      --bundle com.example.app \
      --devices 00008030-...,00008140-... \
      [--manifest-url https://.../manifest.plist] \
      [--web]                # also assert web-bundle hygiene (Capacitor apps)

Exit 0 = PASS (every check green). Exit 1 = FAIL (prints the failing checks).
Pure stdlib. Needs `unzip` on PATH.
"""
import sys, os, re, plistlib, subprocess, tempfile, glob, json, argparse, urllib.request

def load_provision(app):
    raw = open(os.path.join(app, "embedded.mobileprovision"), "rb").read()
    s = raw[raw.find(b"<?xml"):raw.find(b"</plist>") + 8]
    return plistlib.loads(s)

def main():
    P = argparse.ArgumentParser()
    P.add_argument("ipa")
    P.add_argument("--bundle", required=True)
    P.add_argument("--devices", default="", help="comma-separated UDIDs at least one must be provisioned")
    P.add_argument("--team", default=os.environ.get("ASC_TEAM_ID", ""), help="Apple Team ID (default: $ASC_TEAM_ID)")
    P.add_argument("--manifest-url", default="")
    P.add_argument("--web", action="store_true", help="assert Capacitor web-bundle hygiene")
    a = P.parse_args()

    tmp = tempfile.mkdtemp(prefix="ipa_")
    subprocess.run(["unzip", "-q", a.ipa, "-d", tmp], check=True)
    apps = glob.glob(os.path.join(tmp, "Payload", "*.app"))
    if not apps:
        print("FAIL: no Payload/*.app in IPA"); sys.exit(1)
    app = apps[0]

    info = plistlib.load(open(os.path.join(app, "Info.plist"), "rb"))
    prov = load_provision(app)
    devs = set(prov.get("ProvisionedDevices") or [])
    ent = prov.get("Entitlements", {})
    want_devs = [d.strip() for d in a.devices.split(",") if d.strip()]

    checks = {}
    checks["bundle id matches"] = info.get("CFBundleIdentifier") == a.bundle
    if a.team:
        checks["team matches"] = a.team in (prov.get("TeamIdentifier") or [])
    checks["ad hoc (get-task-allow false)"] = ent.get("get-task-allow") is False
    checks["has provisioned devices"] = len(devs) > 0
    if want_devs:
        checks["target device provisioned"] = any(d in devs for d in want_devs)

    ver = info.get("CFBundleShortVersionString")
    if a.manifest_url:
        try:
            # NB: send a real UA — Cloudflare r2.dev 403s the default Python-urllib agent
            req = urllib.request.Request(a.manifest_url, headers={"User-Agent": "Mozilla/5.0 (ship-gate)"})
            mtxt = urllib.request.urlopen(req, timeout=20).read().decode()
            m = re.search(r"bundle-version</key>\s*<string>([^<]+)</string>", mtxt)
            checks["manifest version == IPA version"] = bool(m) and m.group(1) == ver
            mb = re.search(r"bundle-identifier</key>\s*<string>([^<]+)</string>", mtxt)
            checks["manifest bundle == IPA bundle"] = bool(mb) and mb.group(1) == a.bundle
        except Exception as e:
            checks["manifest reachable"] = False
            print("  (manifest fetch error:", str(e)[:80], ")")

    if a.web:
        idx_p = os.path.join(app, "public", "index.html")
        if not os.path.exists(idx_p):
            checks["web index present"] = False
        else:
            html = open(idx_p, encoding="utf-8", errors="ignore").read()
            # the boot-stall class: absolute vendor refs cannot resolve on capacitor://
            checks["no absolute vendor refs"] = ("/assets/" not in html and "cdn.jsdelivr.net" not in html)  # extend with your app's absolute asset prefixes
            # importmap must point at the bundled copy
            im = re.search(r'"imports"\s*:\s*\{[^}]*\}', html)
            checks["importmap vendored"] = bool(im) and "./vendor/three.module.js" in (im.group(0) if im else "")
            checks["three vendored present"] = os.path.exists(os.path.join(app, "public", "vendor", "three.module.js"))

    ok = all(checks.values())
    print(json.dumps({"build": info.get("CFBundleVersion"), "version": ver,
                      "bundle": info.get("CFBundleIdentifier"), "devices": sorted(devs)}, indent=2))
    for k, v in checks.items():
        print(("  PASS " if v else "  FAIL ") + k)
    print("GATE:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
