#!/usr/bin/env python3
"""ts.py — minimal Tailscale API client for tailnet admin (devices, ACLs, SSH rule).

Credentials come from env (injected by RunWithCredentials), NEVER from argv, NEVER printed:
  TAILSCALE_API_KEY    (required)  API access token (tskey-api-...) — sent as Bearer
  TAILSCALE_TAILNET    (optional)  tailnet name; default "-" = the token owner's default tailnet
  TAILSCALE_AUTH_KEY   (optional)  device auth key (tskey-auth-...) for enrolling nodes

urllib honors HTTPS_PROXY, so this works from the sandbox. api.tailscale.com is HTTPS only.

Subcommands:
  verify                       confirm the API token works; print tailnet + device count
  devices                      list devices (name, host, 100.x addrs, os, online, lastSeen)
  acl-get                      print current ACL policy (JSON) + ETag (policy, no secrets)
  acl-validate <file.json>     validate a candidate policy WITHOUT applying
  acl-set <file.json> [etag]   replace the policy (optional If-Match ETag for safe concurrency)
"""
import json, os, sys, urllib.request, urllib.error

BASE = "https://api.tailscale.com/api/v2"
KEY = os.environ.get("TAILSCALE_API_KEY", "")
TAILNET = os.environ.get("TAILSCALE_TAILNET", "") or "-"


def req(method, path, body=None, accept="application/json", extra=None):
    if not KEY:
        print("ERROR: TAILSCALE_API_KEY not set (use RunWithCredentials)"); sys.exit(2)
    data = json.dumps(body).encode() if body is not None else None
    headers = {"Authorization": "Bearer " + KEY, "Accept": accept,
               "User-Agent": "e5-tailscale-admin/1.0"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    if extra:
        headers.update(extra)
    r = urllib.request.Request(BASE + path, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(r, timeout=60) as resp:
            return resp.status, dict(resp.headers), resp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), (e.read().decode() if e.fp else "")


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    c = sys.argv[1]

    if c in ("verify", "tailnet"):
        st, h, b = req("GET", "/tailnet/%s/devices" % TAILNET)
        if st == 200:
            print("OK auth | tailnet:", TAILNET, "| devices:", len(json.loads(b).get("devices", [])))
        else:
            print("FAIL", st, b[:400])
        return

    if c == "devices":
        st, h, b = req("GET", "/tailnet/%s/devices" % TAILNET)
        if st != 200:
            print("FAIL", st, b[:400]); return
        for d in json.loads(b).get("devices", []):
            print("-", d.get("name"),
                  "| host:", d.get("hostname"),
                  "| addrs:", ",".join(d.get("addresses", [])),
                  "| os:", d.get("os"),
                  "| lastSeen:", d.get("lastSeen"),
                  "| ver:", d.get("clientVersion", "")[:20])
        return

    if c == "acl-get":
        st, h, b = req("GET", "/tailnet/%s/acl" % TAILNET)
        print("HTTP", st, "| ETag:", h.get("ETag"))
        print(b)
        return

    if c == "acl-validate":
        pol = json.loads(open(sys.argv[2]).read())
        st, h, b = req("POST", "/tailnet/%s/acl/validate" % TAILNET, body=pol)
        print("HTTP", st, "|", (b[:1000] or "(empty = valid)"))
        return

    if c == "acl-set":
        pol = json.loads(open(sys.argv[2]).read())
        etag = sys.argv[3] if len(sys.argv) > 3 else None
        extra = {"If-Match": etag} if etag else None
        st, h, b = req("POST", "/tailnet/%s/acl" % TAILNET, body=pol, extra=extra)
        print("HTTP", st, "|", b[:1000])
        return

    print("unknown command:", c); sys.exit(1)


if __name__ == "__main__":
    main()
