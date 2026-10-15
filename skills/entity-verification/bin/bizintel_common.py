"""Shared transport for the BizIntel lanes: retries with backoff, timeouts,
rate-limit respect, and response caching. No secrets, no spend."""
from __future__ import annotations

import hashlib
import json
import os
import random
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cache")
DEFAULT_TIMEOUT = 25
DEFAULT_TTL = 24 * 3600  # 24h

AGENT_CONTACT = os.environ.get("BIZINTEL_CONTACT", "you@example.com")  # declared contact for APIs that require one (e.g. SEC EDGAR)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _cache_path(key: str) -> str:
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
    return os.path.join(CACHE_DIR, digest + ".json")


def cache_get(key: str, ttl: int = DEFAULT_TTL):
    path = _cache_path(key)
    try:
        with open(path, "r", encoding="utf-8") as fh:
            payload = json.load(fh)
    except (OSError, ValueError):
        return None
    if time.time() - payload.get("cached_at", 0) > ttl:
        return None
    return payload.get("body")


def cache_set(key: str, body) -> None:
    os.makedirs(CACHE_DIR, exist_ok=True)
    tmp = _cache_path(key) + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump({"cached_at": time.time(), "body": body}, fh)
    os.replace(tmp, _cache_path(key))


def http_get(url: str, params: dict | None = None, headers: dict | None = None,
             timeout: int = DEFAULT_TIMEOUT, retries: int = 3,
             backoff: float = 2.0, min_interval: float = 0.0,
             last_call: dict | None = None) -> tuple[int, str, dict]:
    """GET with retries/backoff/timeout. Returns (status, text, resp_headers).

    `last_call` is a mutable dict the caller can reuse across calls to enforce
    a minimum interval between requests (rate-limit respect): key "t".
    """
    if params:
        url = url + ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
    req_headers = {"User-Agent": f"EntityVerification/1.0 (+{AGENT_CONTACT})",
                   "Accept": "application/json, text/plain, */*"}
    if headers:
        req_headers.update(headers)
    last_status, last_exc = 0, None
    for attempt in range(retries + 1):
        if last_call is not None and min_interval > 0:
            gap = time.time() - last_call.get("t", 0)
            if gap < min_interval:
                time.sleep(min_interval - gap)
        req = urllib.request.Request(url, headers=req_headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                text = resp.read().decode("utf-8", errors="replace")
                if last_call is not None:
                    last_call["t"] = time.time()
                return resp.status, text, dict(resp.headers)
        except urllib.error.HTTPError as exc:  # noqa: F821
            last_status = exc.code
            try:
                exc.read()
            except Exception:
                pass
            if exc.code in (429, 503) or 500 <= exc.code < 600:
                wait = backoff * (2 ** attempt) + random.uniform(0, 0.5)
                retry_after = exc.headers.get("Retry-After") if exc.headers else None
                if retry_after:
                    try:
                        wait = max(wait, float(retry_after))
                    except ValueError:
                        pass
                time.sleep(wait)
                continue
            return exc.code, "", dict(exc.headers or {})
        except Exception as exc:  # network/timeout: retry
            last_exc = exc
            last_status = 0
            time.sleep(backoff * (2 ** attempt) + random.uniform(0, 0.5))
    raise RuntimeError(f"http_get failed after {retries + 1} attempts: {url} "
                       f"(last_status={last_status}, last_exc={last_exc})")


def lane_record(lane: str, source: str, status: str, facts: dict,
                sources: list | None = None, notes: list | None = None) -> dict:
    """Standard per-lane output record. status: ok | no_record | parked | error."""
    return {
        "lane": lane,
        "source": source,
        "retrieved_at": now_iso(),
        "status": status,
        "facts": facts,
        "sources": sources or [source],
        "notes": notes or [],
    }
