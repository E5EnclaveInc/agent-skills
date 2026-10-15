#!/usr/bin/env python3
"""iOS Ship — OTA kit generator.
Composes the itms-services manifest.plist + branded install.html for an Ad Hoc app
and prints the two files to ./out/. Publish them (and later the IPA) to any HTTPS
host — any static HTTPS host works (e.g. an R2 public bucket). Usage:
  python3 ota_kit.py --bundle com.example.myapp --title "My App" --version 1.0.0 \
      --base https://pub-XXXX.r2.dev/myapp/app [--icon ../appicons/icon-only.png]
"""
import argparse, os, html
P = argparse.ArgumentParser()
P.add_argument('--bundle', required=True); P.add_argument('--title', required=True)
P.add_argument('--version', default='1.0.0'); P.add_argument('--base', required=True)
P.add_argument('--icon', default='')
a = P.parse_args()
os.makedirs('out', exist_ok=True)
ipa = f"{a.base}/{a.title.replace(' ','')}.ipa"
man = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict><key>items</key><array><dict>
<key>assets</key><array><dict><key>kind</key><string>software-package</string>
<key>url</key><string>{ipa}</string></dict></array>
<key>metadata</key><dict>
<key>bundle-identifier</key><string>{a.bundle}</string>
<key>bundle-version</key><string>{a.version}</string>
<key>kind</key><string>software</string>
<key>platform-identifier</key><string>com.apple.platform.iphoneos</string>
<key>title</key><string>{html.escape(a.title)}</string>
</dict></dict></array></dict></plist>'''
open('out/manifest.plist','w').write(man)
icon = f'<img src="{a.icon}" style="width:132px;height:132px;border-radius:30px">' if a.icon else ''
page = f'''<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(a.title)} — Install</title><style>body{{margin:0;background:#0a0c10;color:#e8ecf3;font-family:-apple-system,system-ui;display:grid;place-items:center;min-height:100vh;text-align:center}}.c{{padding:40px 28px;max-width:420px}}a.b{{display:inline-block;margin-top:22px;padding:16px 44px;background:#c9a84c;color:#141414;font-weight:800;letter-spacing:.1em;border-radius:12px;text-decoration:none}}.f{{margin-top:26px;font-size:11.5px;opacity:.5}}</style></head>
<body><div class="c">{icon}<h1>{html.escape(a.title).upper()}</h1>
<a class="b" href="itms-services://?action=download-manifest&amp;url={a.base}/manifest.plist">INSTALL</a>
<p class="f">Ad Hoc build for registered devices. Open in Safari on iPhone.<br>Settings → General → VPN &amp; Device Management → trust your developer profile if asked.</p>
</div></body></html>'''
open('out/install.html','w').write(page)
print('out/manifest.plist + out/install.html ready | ipa expected at', ipa)
