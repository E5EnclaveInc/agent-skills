#!/usr/bin/env python3
"""Shared helper: fetch a Lambda instance's JupyterLab base URL + token.

Reads the API key the same way bin/lambda.py does (LAMBDA_API_KEY env,
falling back to ~/.lambda/api_key). Never prints the key or token.
"""
import json
import os
import time
import urllib.request
from pathlib import Path
from urllib.parse import urlparse, parse_qs

API = "https://cloud.lambdalabs.com/api/v1"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"


def api_key() -> str:
    key = os.environ.get("LAMBDA_API_KEY")
    if key:
        return key
    return Path("~/.lambda/api_key").expanduser().read_text().strip()


def _req(method: str, path: str):
    # Transport note (2026-09-17): this sandbox's egress proxy mangles
    # chunked responses for urllib (IncompleteRead on /instances), while
    # requests handles them fine -- same rule as bin/lambda.py.
    headers = {"Authorization": "Bearer " + api_key(), "User-Agent": UA}
    try:
        import requests  # noqa: E402

        r = requests.request(method, API + path, headers=headers, timeout=30)
        r.raise_for_status()
        return r.json()["data"]
    except ImportError:
        req = urllib.request.Request(API + path, method=method, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)["data"]


def instance(instance_id: str) -> dict:
    return _req("GET", f"/instances/{instance_id}")


def jupyter(instance_id: str, wait_sec: int = 300) -> tuple[str, str]:
    """Return (base_url, token) for the instance's JupyterLab.

    Uses a PER-INSTANCE /tmp cache (written by an earlier probe); the
    lambdaspaces/API endpoints are intermittently flaky, so avoid
    re-fetching when the cache is fresh. The cache key MUST include the
    instance id — a shared cache once routed shakedown-03's tools at
    shakedown-02's box (2026-09-15).

    A freshly-active instance often has no jupyter_url for the first
    minute(s); wait up to wait_sec for it instead of failing on a
    1-second race (killed air-followup 2026-09-18).
    """
    base_f = Path(f"/tmp/jup_{instance_id}_base.txt")
    token_f = Path(f"/tmp/jup_{instance_id}_token.txt")
    try:
        base = base_f.read_text().strip()
        token = token_f.read_text().strip()
        if base and token:
            return base, token
    except OSError:
        pass
    deadline = time.time() + wait_sec
    last_status = None
    url = ""
    while True:
        info = instance(instance_id)
        url = info.get("jupyter_url") or ""
        last_status = info.get("status")
        if url:
            break
        if time.time() >= deadline:
            raise RuntimeError(
                f"no jupyter_url yet for {instance_id} (status={last_status}) after {wait_sec}s")
        time.sleep(10)
    parts = urlparse(url)
    token = parse_qs(parts.query).get("token", [""])[0]
    base = f"{parts.scheme}://{parts.netloc}"
    if not token:
        raise RuntimeError("jupyter_url has no token param")
    base_f.write_text(base)
    token_f.write_text(token)
    return base, token
