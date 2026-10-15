#!/usr/bin/env python3
"""Read-only Lambda Cloud connectivity check (stdlib only, no pip).

Verifies the Secure-Vault-injected LAMBDA_API_KEY authenticates, then
prints a read-only account snapshot: instance count, SSH key count,
filesystem count.

NOTE: the public API (v1.10.0) exposes NO credit-balance endpoint --
service-credit balance is console-only (https://cloud.lambda.ai/billing).
This check proves auth works; it cannot report the $7,500 balance.

Usage: LAMBDA_API_KEY=<from vault> python3 bin/lambda_check.py
"""
import json
import os
import sys
import time
import urllib.request
import urllib.error

BASE = "https://cloud.lambdalabs.com/api/v1"


def get(path, key):
    time.sleep(1.2)
    req = urllib.request.Request(
        BASE + path,
        headers={"Authorization": "Bearer " + key,
                 "Accept": "application/json",
                 # Cloudflare bot management 403s urllib's default UA
                 # (Error 1010); a browser UA clears it (2026-09-15).
                 "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                               "AppleWebKit/537.36 (KHTML, like Gecko) "
                               "Chrome/126.0.0.0 Safari/537.36"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode()).get("data", [])
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:300]
        print("HTTP %d on %s\n%s" % (e.code, path, body))
        sys.exit(3)


def main():
    key = os.environ.get("LAMBDA_API_KEY", "").strip()
    if not key:
        try:
            with open(os.path.expanduser("~/.lambda/api_key")) as f:
                key = f.read().strip()
        except OSError:
            pass
    if not key:
        print("No Lambda API key: LAMBDA_API_KEY unset and "
              "~/.lambda/api_key missing.")
        print("You mint it at "
              "https://cloud.lambda.ai/api-keys/cloud-api")
        sys.exit(2)
    print("Lambda Cloud API: AUTH OK (Bearer)")
    insts = get("/instances", key)
    keys = get("/ssh-keys", key)
    fss = get("/file-systems", key)
    print("instances:  %d" % len(insts))
    for i in insts:
        it = i.get("instance_type", {}) or {}
        print("  - %s  %s  %s  %s" %
              (i.get("id"), (i.get("name") or "")[:30],
               it.get("name", "?"), i.get("status", "?")))
    print("ssh keys:   %d" % len(keys))
    for k in keys:
        print("  - %s" % k.get("name"))
    print("filesystems:%d" % len(fss))
    for f in fss:
        print("  - %s (%s, %s GB)" %
              (f.get("name"), f.get("region", {}).get("name", "?"),
               f.get("size_gb", "?")))
    print("\nNote: credit balance is console-only; check "
          "https://cloud.lambda.ai/billing")


if __name__ == "__main__":
    main()
