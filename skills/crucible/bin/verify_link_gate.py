#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crucible Verification Gate — LINK GATE
Probe every external URL in an HTML file (or a URL list) for liveness AND real content.
Catches: dead links (4xx/5xx), soft-404s, ".pdf" URLs that actually return an HTML shell,
parked/login/error pages, and datacenter bot-blocks (real-in-browser, flagged NEEDS_EYES).

USAGE
  python3 verify_link_gate.py page.html                 # extract + probe every http(s) link
  python3 verify_link_gate.py --urls urls.txt           # one URL per line
  python3 verify_link_gate.py --url https://a https://b # explicit URLs
  python3 verify_link_gate.py page.html --out links.json
Emits a JSON array of ledger entries to --out (default link_ledger.json) + a console summary.
Status values: PASS | BROKEN | NEEDS_EYES
No credentials required.
"""
import sys, json, re, argparse, subprocess

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
try:
    import requests
except Exception:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "requests"])
    import requests


def human(n):
    if not n:
        return ""
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return "%.1f %s" % (n, unit)
        n /= 1024.0
    return "%.1f TB" % n


def extract_urls_from_html(html):
    urls = re.findall(r'href=["\'](https?://[^"\']+)["\']', html)
    urls += re.findall(r'src=["\'](https?://[^"\']+)["\']', html)
    # drop google-fonts noise by default
    seen, out = set(), []
    for u in urls:
        if u in seen:
            continue
        seen.add(u)
        if "fonts.googleapis.com" in u or "fonts.gstatic.com" in u:
            continue
        out.append(u)
    return out


def probe(url, timeout=30):
    e = {"kind": "link", "target_url": url}
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=timeout,
                         stream=True, allow_redirects=True)
        code = r.status_code
        ct = (r.headers.get("content-type") or "").lower()
        clen = r.headers.get("content-length")
        try:
            first = next(r.iter_content(2048), b"") or b""
        except Exception:
            first = b""
        botblock = ("cf-ray" in r.headers) or ("akamai" in str(r.headers).lower()) \
            or (b"cloudflare" in first.lower())
        r.close()
        size = int(clen) if (clen and clen.isdigit()) else None
        e.update({"http": code, "content_type": ct, "size": size,
                  "final_url": r.url})
        is_pdf_url = url.lower().split("?")[0].rstrip("/").endswith(".pdf")
        looks_pdf = first[:5] == b"%PDF-"
        low = first.lower()
        errish = any(s in low for s in (b"sign in", b"signin", b"log in to",
                     b"accounts.google.com/v3/signin", b"<title>error",
                     b"page not found", b"404 not found", b"domain for sale",
                     b"this domain is parked"))
        if code >= 400:
            if code in (401, 403) and (botblock or ct.startswith("text/html")):
                e["status"] = "NEEDS_EYES"
                e["detail"] = "HTTP %d — likely a datacenter bot-block; verify in a real browser" % code
            else:
                e["status"] = "BROKEN"
                e["detail"] = "HTTP %d" % code
        elif is_pdf_url and not looks_pdf:
            e["status"] = "BROKEN"
            e["detail"] = "URL is .pdf but server returned %s, not a PDF (soft-404 / HTML shell)" % (ct or "?")
        elif errish:
            e["status"] = "NEEDS_EYES"
            e["detail"] = "HTTP 200 but body reads like an error/login/parked page"
        elif looks_pdf:
            e["status"] = "PASS"
            e["detail"] = "real PDF%s" % ((" · " + human(size)) if size else "")
        else:
            e["status"] = "PASS"
            e["detail"] = "%s%s" % (ct or "ok", (" · " + human(size)) if size else "")
    except Exception as ex:
        e["status"] = "BROKEN"
        e["detail"] = "fetch error: %s" % ex
    return e


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html", nargs="?", help="HTML file to extract links from")
    ap.add_argument("--urls", help="text file, one URL per line")
    ap.add_argument("--url", nargs="*", default=[], help="explicit URL(s)")
    ap.add_argument("--out", default="link_ledger.json")
    ap.add_argument("--timeout", type=int, default=30)
    a = ap.parse_args()

    urls = list(a.url)
    if a.html:
        with open(a.html, encoding="utf-8", errors="ignore") as f:
            urls += extract_urls_from_html(f.read())
    if a.urls:
        with open(a.urls, encoding="utf-8") as f:
            urls += [ln.strip() for ln in f if ln.strip() and ln.strip().startswith("http")]
    urls = sorted(set(urls))
    if not urls:
        print("No URLs found. Pass an HTML file, --urls file, or --url ...")
        sys.exit(1)

    entries = [probe(u, a.timeout) for u in urls]
    with open(a.out, "w") as f:
        json.dump(entries, f, indent=2)

    tally = {"PASS": 0, "BROKEN": 0, "NEEDS_EYES": 0}
    for e in entries:
        tally[e["status"]] = tally.get(e["status"], 0) + 1
        mark = {"PASS": "ok ", "BROKEN": "XX ", "NEEDS_EYES": ".. "}[e["status"]]
        print("[%s] %-11s %s\n        %s" % (mark, e["status"], e["target_url"], e["detail"]))
    print("\nLINK GATE: %d PASS · %d BROKEN · %d NEEDS_EYES  (%d total) -> %s"
          % (tally["PASS"], tally["BROKEN"], tally["NEEDS_EYES"], len(entries), a.out))
    sys.exit(2 if tally["BROKEN"] else 0)


if __name__ == "__main__":
    main()
