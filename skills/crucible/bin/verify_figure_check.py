#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crucible Verification Gate — MECHANICAL FIGURE CHECK
Verifies the figures a machine CAN settle against the cited file:
  - file size claims ("~86 MB", "118 KB")  vs the server's Content-Length
  - PDF page-count claims ("636 pages")     vs pdfinfo / pypdf on the file
Everything it cannot settle mechanically (dollar amounts, dates, attributions)
is emitted as NEEDS_SOURCE_CHECK for verify_figure_exa.py or the agent's judgment.

INPUT MODES
  python3 verify_figure_check.py --claims claims.json
      claims.json = [{"id":"ca-full","type":"filesize","url":"https://...pdf","expected":"86 MB"},
                     {"id":"fulton","type":"pagecount","url":"https://...pdf","expected":"636"},
                     {"id":"citi","type":"figure","claim":"$16T lost GDP","source":"Citi GPS 2020"}]
  python3 verify_figure_check.py --from-html page.html
      auto-extracts size/page claims paired to the nearest link in each card/block.
Emits a JSON array of ledger entries to --out (default figure_ledger.json) + a console summary.
Status: MATCH | MISMATCH | UNVERIFIABLE | NEEDS_SOURCE_CHECK
No credentials required. (PDF page counts use poppler `pdfinfo`, falling back to pypdf.)
"""
import sys, json, re, argparse, subprocess, os, tempfile

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
try:
    import requests
except Exception:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "requests"])
    import requests

UNIT = {"B": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3}


def parse_size(s):
    m = re.search(r"([\d.]+)\s*(GB|MB|KB|B)", s, re.I)
    if not m:
        return None
    return float(m.group(1)) * UNIT[m.group(2).upper()]


def content_length(url, timeout=40, measure_cap=60 * 1024**2):
    for method in ("head", "get"):
        try:
            r = requests.request(method, url, headers={"User-Agent": UA},
                                 timeout=timeout, allow_redirects=True, stream=True)
            cl = r.headers.get("content-length")
            r.close()
            if cl and cl.isdigit():
                return int(cl)
        except Exception:
            continue
    # fallback: server omitted Content-Length (e.g. chunked) — measure by streaming, capped
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=timeout, stream=True, allow_redirects=True)
        total = 0
        for chunk in r.iter_content(1 << 16):
            total += len(chunk)
            if total > measure_cap:
                r.close(); return None  # too big to measure cheaply
        r.close()
        return total
    except Exception:
        return None


def pdf_pagecount(url, timeout=180, cap=170 * 1024**2):
    size = content_length(url) or 0
    if size and size > cap:
        return None, "file %d bytes exceeds cap; skip auto page-count" % size
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=timeout, stream=True, allow_redirects=True)
        fd, path = tempfile.mkstemp(suffix=".pdf")
        with os.fdopen(fd, "wb") as f:
            for chunk in r.iter_content(1 << 16):
                f.write(chunk)
        r.close()
    except Exception as ex:
        return None, "download failed: %s" % ex
    try:
        out = subprocess.run(["pdfinfo", path], capture_output=True, text=True, timeout=60).stdout
        m = re.search(r"^Pages:\s*(\d+)", out, re.M)
        if m:
            os.remove(path)
            return int(m.group(1)), "pdfinfo"
    except Exception:
        pass
    try:
        from pypdf import PdfReader
        n = len(PdfReader(path).pages)
        os.remove(path)
        return n, "pypdf"
    except Exception as ex:
        try: os.remove(path)
        except Exception: pass
        return None, "no page-count tool succeeded: %s" % ex


def check_filesize(url, expected, tol=0.18):
    actual = content_length(url)
    exp = parse_size(expected)
    if actual is None:
        return "UNVERIFIABLE", "no Content-Length from server", None
    am = actual / float(UNIT["MB"])
    if exp is None:
        return "UNVERIFIABLE", "could not parse expected size %r; server reports %.1f MB" % (expected, am), am
    em = exp / float(UNIT["MB"])
    ok = abs(actual - exp) <= tol * max(actual, exp)
    return ("MATCH" if ok else "MISMATCH"), "claimed %.1f MB · actual %.1f MB" % (em, am), am


def check_pagecount(url, expected):
    try:
        exp = int(re.sub(r"[^\d]", "", str(expected)))
    except Exception:
        exp = None
    n, how = pdf_pagecount(url)
    if n is None:
        return "UNVERIFIABLE", how, None
    if exp is None:
        return "UNVERIFIABLE", "could not parse expected pages %r; actual %d (%s)" % (expected, n, how), n
    return ("MATCH" if n == exp else "MISMATCH"), "claimed %d pages · actual %d (%s)" % (exp, n, how), n


def from_html(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        html = f.read()
    # split into blocks at each anchor; pair a nearby size/page claim with the link
    claims = []
    for m in re.finditer(r'href=["\'](https?://[^"\']+\.pdf[^"\']*)["\']', html, re.I):
        url = m.group(1)
        window = html[max(0, m.start() - 700):m.end() + 200]
        sz = re.search(r"([\d.]+\s*(?:GB|MB|KB))", window, re.I)
        pg = re.search(r"(\d[\d,]*)\s*pages", window, re.I)
        if sz:
            claims.append({"id": url.split("/")[-1][:40], "type": "filesize", "url": url, "expected": sz.group(1)})
        if pg:
            claims.append({"id": url.split("/")[-1][:40] + "#pg", "type": "pagecount", "url": url, "expected": pg.group(1)})
    return claims


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--claims", help="claims.json")
    ap.add_argument("--from-html", help="auto-extract size/page claims from an HTML file")
    ap.add_argument("--out", default="figure_ledger.json")
    ap.add_argument("--tol", type=float, default=0.18, help="filesize tolerance (default 18%)")
    a = ap.parse_args()

    if a.claims:
        claims = json.load(open(a.claims))
    elif getattr(a, "from_html"):
        claims = from_html(a.from_html)
    else:
        print("Pass --claims claims.json or --from-html page.html"); sys.exit(1)

    entries = []
    for c in claims:
        t = c.get("type", "figure")
        e = {"kind": "figure", "id": c.get("id"), "target_url": c.get("url"),
             "claim": c.get("claim") or "%s=%s" % (t, c.get("expected")),
             "source": c.get("source", "")}
        if t == "filesize":
            st, det, _ = check_filesize(c["url"], c["expected"], a.tol)
        elif t == "pagecount":
            st, det, _ = check_pagecount(c["url"], c["expected"])
        else:
            st, det = "NEEDS_SOURCE_CHECK", "not mechanically checkable — verify against source (use verify_figure_exa.py)"
        e["status"], e["detail"] = st, det
        entries.append(e)

    with open(a.out, "w") as f:
        json.dump(entries, f, indent=2)
    tally = {}
    for e in entries:
        tally[e["status"]] = tally.get(e["status"], 0) + 1
        mark = {"MATCH": "ok ", "MISMATCH": "XX ", "UNVERIFIABLE": "?? ",
                "NEEDS_SOURCE_CHECK": ".. "}.get(e["status"], "   ")
        print("[%s] %-18s %s\n        %s" % (mark, e["status"], e.get("claim"), e["detail"]))
    print("\nFIGURE GATE: " + " · ".join("%d %s" % (v, k) for k, v in tally.items()) + "  -> " + a.out)
    sys.exit(2 if tally.get("MISMATCH") else 0)


if __name__ == "__main__":
    main()
