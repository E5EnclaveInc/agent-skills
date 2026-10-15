#!/usr/bin/env python3
"""Compose a Sovereign Couture atelier character sheet.

Usage: python3 compose_sheet.py spec.json sheet.html

Emits one self-contained 4:5 (1200x1500) HTML file: fonts embedded as data
URIs (plus your own crest from assets/crest.webp when present), hero +
reference images embedded, zero network requests.
All annotation type is real HTML text — never rendered by an image model.
"""
import base64
import html
import json
import os
import sys

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(SKILL_DIR, "assets")

BG = "#0a0a0a"
INK = "#e8dcc0"
MUTED = "#a89a78"
GOLD = "#d6a84b"
GOLD_LIGHT = "#ecd9a4"
HAIR = "rgba(214,168,75,.35)"


def data_uri(path, mime):
    with open(path, "rb") as f:
        return "data:%s;base64,%s" % (mime, base64.b64encode(f.read()).decode())


def font_face(family, weight, style, filename):
    uri = data_uri(os.path.join(ASSETS, "fonts", filename), "font/woff2")
    return ("@font-face{font-family:'%s';font-weight:%s;font-style:%s;"
            "src:url(%s) format('woff2');font-display:swap;}"
            % (family, weight, style, uri))


def esc(s):
    return html.escape(str(s), quote=True)


def crop_style(ref_uri, x, y, w, h):
    # background-size/position so the fractional rect fills the crop box
    bw, bh = 100.0 / w, 100.0 / h
    px = (x / (1 - w) * 100) if w < 1 else 50
    py = (y / (1 - h) * 100) if h < 1 else 50
    return ("background-image:url(%s);background-size:%.2f%% %.2f%%;"
            "background-position:%.2f%% %.2f%%;" % (ref_uri, bw, bh, px, py))


def main():
    spec_path, out_path = sys.argv[1], sys.argv[2]
    with open(spec_path) as f:
        spec = json.load(f)

    crest_path = os.path.join(ASSETS, "crest.webp")
    crest = data_uri(crest_path, "image/webp") if os.path.exists(crest_path) else ""
    crest_mast = ('<img class="crest" src="%s" alt="atelier crest">' % crest) if crest else ""
    crest_foot = ('<img src="%s" alt="atelier crest">' % crest) if crest else ""
    hero = data_uri(spec["hero"], "image/webp"
                   if spec["hero"].lower().endswith(".webp") else "image/jpeg")
    ref = data_uri(spec["reference"], "image/webp"
                   if spec["reference"].lower().endswith(".webp") else "image/jpeg")

    css = "\n".join([
        font_face("Cormorant Garamond", 400, "normal",
                  "cormorant-garamond-latin-400-normal.woff2"),
        font_face("Cormorant Garamond", 500, "normal",
                  "cormorant-garamond-latin-500-normal.woff2"),
        font_face("Cormorant Garamond", 400, "italic",
                  "cormorant-garamond-latin-400-italic.woff2"),
        font_face("IBM Plex Sans", 400, "normal",
                  "ibm-plex-sans-latin-400-normal.woff2"),
        font_face("IBM Plex Sans", 500, "normal",
                  "ibm-plex-sans-latin-500-normal.woff2"),
        font_face("IBM Plex Sans", 600, "normal",
                  "ibm-plex-sans-latin-600-normal.woff2"),
        font_face("IBM Plex Mono", 400, "normal",
                  "ibm-plex-mono-latin-400-normal.woff2"),
        font_face("IBM Plex Mono", 500, "normal",
                  "ibm-plex-mono-latin-500-normal.woff2"),
    ])

    markers = "\n".join(
        '<div class="marker" style="left:%s%%;top:%s%%">%s</div>'
        % (esc(c["x"]), esc(c["y"]), esc(c["n"])) for c in spec["callouts"])

    callouts = "\n".join(
        '<div class="callout"><div class="cnum">%s</div>'
        '<div><div class="ctitle">%s</div><div class="cbody">%s</div></div></div>'
        % (esc(c["n"]), esc(c["title"]), esc(c["body"]))
        for c in spec["callouts"])

    details = "\n".join(
        '<div class="detail"><div class="crop" style="%s"></div>'
        '<div class="dlabel">%s</div><div class="dcap">%s</div></div>'
        % (crop_style(ref, d["x"], d["y"], d["w"], d["h"]),
           esc(d["label"]), esc(d["caption"]))
        for d in spec["details"])

    swatches = "\n".join(
        '<div class="sw"><div class="dot" style="background:%s"></div>'
        '<div class="sname">%s</div></div>'
        % (esc(p["hex"]), esc(p["name"])) for p in spec["palette"])

    appeal = "\n".join("<li>%s</li>" % esc(a) for a in spec["appeal_points"])

    page = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>%(title)s — Atelier Sovereign Character Sheet</title>
<style>
%(css)s
*{margin:0;padding:0;box-sizing:border-box}
html{background:#000}
body{width:1200px;margin:0 auto;background:%(bg)s;color:%(ink)s;
 font-family:'IBM Plex Sans',Helvetica,Arial,sans-serif;
 -webkit-font-smoothing:antialiased}
.sheet{width:1200px;padding:44px 64px 44px;position:relative}
.masthead{display:flex;align-items:center;gap:28px}
.masthead img.crest{width:92px;height:138px;object-fit:contain;
 filter:drop-shadow(0 0 18px rgba(214,168,75,.35))}
.eyebrow{font-family:'IBM Plex Mono',monospace;font-size:15px;letter-spacing:.42em;
 color:%(gold)s;text-transform:uppercase}
h1{font-family:'Cormorant Garamond',Georgia,serif;font-weight:500;font-size:58px;
 line-height:1.02;color:%(goldlight)s;margin:10px 0 8px}
.house{font-family:'Cormorant Garamond',Georgia,serif;font-style:italic;
 font-size:24px;color:%(muted)s}
.folio{margin-left:auto;text-align:right;font-family:'IBM Plex Mono',monospace;
 font-size:14px;letter-spacing:.28em;color:%(muted)s}
.rule{border:0;border-top:1px solid %(hair)s;margin:24px 0}
.stage{display:flex;gap:40px;margin-top:6px}
.hero{position:relative;flex:0 0 560px;height:700px;background:#000;
 border:1px solid %(hair)s;overflow:hidden}
.hero img{width:100%%;height:100%%;object-fit:cover;display:block}
.marker{position:absolute;width:44px;height:44px;margin:-22px 0 0 -22px;
 border:1px solid %(gold)s;border-radius:50%%;color:%(goldlight)s;
 font-family:'IBM Plex Mono',monospace;font-size:16px;font-weight:500;
 display:flex;align-items:center;justify-content:center;
 background:rgba(10,10,10,.72);box-shadow:0 0 14px rgba(214,168,75,.45)}
.callouts{flex:1;display:flex;flex-direction:column;gap:0}
.callout{display:flex;gap:16px;padding:10px 0;border-bottom:1px solid rgba(214,168,75,.16)}
.callout:first-child{padding-top:0}
.cnum{font-family:'IBM Plex Mono',monospace;color:%(gold)s;font-size:20px;
 font-weight:500;min-width:38px}
.ctitle{font-size:15px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;
 color:%(goldlight)s;margin-bottom:5px}
.cbody{font-size:16px;line-height:1.5;color:%(ink)s}
.sect{margin-top:32px}
.secthead{font-family:'IBM Plex Mono',monospace;font-size:14px;letter-spacing:.42em;
 color:%(gold)s;text-transform:uppercase;margin-bottom:18px}
.detailrow{display:flex;gap:22px}
.detail{flex:1}
.crop{width:100%%;height:140px;border:1px solid %(hair)s;background-color:#000;
 background-repeat:no-repeat}
.dlabel{font-family:'IBM Plex Mono',monospace;font-size:13px;letter-spacing:.24em;
 color:%(gold)s;text-transform:uppercase;margin:12px 0 4px}
.dcap{font-size:14.5px;line-height:1.5;color:%(muted)s}
.palrow{display:flex;gap:34px;align-items:flex-start}
.sw{text-align:center}
.dot{width:74px;height:74px;border-radius:50%%;border:1px solid %(hair)s;
 box-shadow:0 0 12px rgba(0,0,0,.6)}
.sname{font-family:'IBM Plex Mono',monospace;font-size:13px;letter-spacing:.18em;
 color:%(ink)s;text-transform:uppercase;margin-top:10px}
.edrow{display:flex;gap:44px}
.edcol{flex:1}
.edcol h3{font-family:'Cormorant Garamond',Georgia,serif;font-size:27px;
 font-weight:500;color:%(goldlight)s;margin-bottom:10px}
.edcol p,.edcol li{font-size:16px;line-height:1.65;color:%(ink)s}
.edcol ul{list-style:none}
.edcol li{padding:7px 0 7px 20px;position:relative}
.edcol li:before{content:"";position:absolute;left:0;top:15px;width:8px;height:1px;
 background:%(gold)s}
footer{margin-top:36px;border-top:1px solid %(hair)s;padding-top:26px;
 display:flex;align-items:center;gap:22px}
footer img{width:44px;height:66px;object-fit:contain;
 filter:drop-shadow(0 0 10px rgba(214,168,75,.4))}
.motto{font-family:'IBM Plex Mono',monospace;font-size:15px;letter-spacing:.34em;
 color:%(gold)s}
.prov{margin-left:auto;font-family:'IBM Plex Mono',monospace;font-size:12.5px;
 letter-spacing:.12em;color:%(muted)s;text-align:right;line-height:1.8}
</style></head>
<body><div class="sheet">
<header class="masthead">
 %(crest_mast)s
 <div><div class="eyebrow">Atelier Sovereign &middot; Character Sheet</div>
 <h1>%(title)s</h1><div class="house">%(house_line)s</div></div>
 <div class="folio">FOLIO<br>N&ordm; 001</div>
</header>
<hr class="rule">
<section class="stage">
 <div class="hero"><img src="%(hero)s" alt="%(title)s — reconstructed garment visualization">%(markers)s</div>
 <div class="callouts">%(callouts)s</div>
</section>
<section class="sect"><div class="secthead">Material &amp; Detail</div>
 <div class="detailrow">%(details)s</div></section>
<section class="sect"><div class="secthead">Color Palette</div>
 <div class="palrow">%(swatches)s</div></section>
<section class="sect"><div class="secthead">Atelier Notes</div>
 <div class="edrow">
  <div class="edcol"><h3>Coordinate Note</h3><p>%(coordinate_note)s</p></div>
  <div class="edcol"><h3>Appeal Point</h3><ul>%(appeal)s</ul></div>
  <div class="edcol"><h3>Styling Logic</h3><p>%(styling_logic)s</p></div>
 </div></section>
<footer>
 %(crest_foot)s
 <div class="motto">NIL SATIS NISI OPTIMUM</div>
 <div class="prov">REFERENCE IMAGE &gt; CREATIVE INTERPRETATION<br>
 RECONSTRUCTED WITH FIDELITY &middot; ATELIER SOVEREIGN</div>
</footer>
</div></body></html>""" % {
        "css": css, "bg": BG, "ink": INK, "muted": MUTED, "gold": GOLD,
        "goldlight": GOLD_LIGHT, "hair": HAIR,
        "title": esc(spec["title"]), "house_line": esc(spec["house_line"]),
        "crest_mast": crest_mast, "crest_foot": crest_foot, "hero": hero, "markers": markers,
        "callouts": callouts, "details": details, "swatches": swatches,
        "coordinate_note": esc(spec["coordinate_note"]), "appeal": appeal,
        "styling_logic": esc(spec["styling_logic"]),
    }

    with open(out_path, "w") as f:
        f.write(page)
    print("wrote %s (%d KB)" % (out_path, os.path.getsize(out_path) // 1024))


if __name__ == "__main__":
    main()
