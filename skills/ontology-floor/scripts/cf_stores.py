#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Write layer for the Ontology Floor — persists a verified Grounding Record to
three owned Cloudflare stores:
  R2 (ontology-floor): the full record JSON + proof pointer
  D1 (ontology):    the index row resolve() reads
  Vectorize (ontology-floor-canon): the term/definition embedding (BGE, 768-d)

All provisioning is idempotent (safe to call every run). Uses the Cloudflare
(Global) skill env: CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID,
R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY.

`python3 cf_stores.py --writetest` provisions + writes ONE record + reads it back.
"""
import os, json, hmac, hashlib, datetime, urllib.request, urllib.parse

ACCT = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "fd98d813898e36431c9d6af3b0beeb20")
TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")
AKID = os.environ.get("R2_ACCESS_KEY_ID", "")
SECRET = os.environ.get("R2_SECRET_ACCESS_KEY", "")
API = "https://api.cloudflare.com/client/v4"
R2_BUCKET = "ontology-floor"
D1_NAME = "ontology"
VEC_INDEX = "ontology-floor-canon"
VEC_DIMS = 768

# ---------------- Cloudflare REST (Bearer) ----------------
def _api(method, path, body=None, ndjson=False):
    data = None
    headers = {"Authorization": "Bearer " + TOKEN, "User-Agent": "ontology-stores/1.0"}
    if body is not None:
        if ndjson:
            data = body.encode(); headers["Content-Type"] = "application/x-ndjson"
        else:
            data = json.dumps(body).encode(); headers["Content-Type"] = "application/json"
    req = urllib.request.Request(API + path, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode())
        except Exception:
            return e.code, {"success": False}

# ---------------- R2 (SigV4) ----------------
def _sign(key, msg): return hmac.new(key, msg.encode(), hashlib.sha256).digest()

def _r2(method, key, data=b""):
    host = "%s.r2.cloudflarestorage.com" % ACCT
    now = datetime.datetime.utcnow()
    amz = now.strftime("%Y%m%dT%H%M%SZ"); ds = now.strftime("%Y%m%d")
    region, service = "auto", "s3"
    ph = hashlib.sha256(data).hexdigest()
    uri = "/%s/%s" % (R2_BUCKET, urllib.parse.quote(key))
    ch = "host:%s\nx-amz-content-sha256:%s\nx-amz-date:%s\n" % (host, ph, amz)
    sh = "host;x-amz-content-sha256;x-amz-date"
    creq = "%s\n%s\n\n%s\n%s\n%s" % (method, uri, ch, sh, ph)
    scope = "%s/%s/%s/aws4_request" % (ds, region, service)
    sts = "AWS4-HMAC-SHA256\n%s\n%s\n%s" % (amz, scope, hashlib.sha256(creq.encode()).hexdigest())
    k = _sign(_sign(_sign(_sign(("AWS4"+SECRET).encode(), ds), region), service), "aws4_request")
    sig = hmac.new(k, sts.encode(), hashlib.sha256).hexdigest()
    auth = "AWS4-HMAC-SHA256 Credential=%s/%s, SignedHeaders=%s, Signature=%s" % (AKID, scope, sh, sig)
    h = {"Authorization": auth, "x-amz-content-sha256": ph, "x-amz-date": amz}
    req = urllib.request.Request("https://%s%s" % (host, uri), data=(data if method in ("PUT","POST") else None),
                                 method=method, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()

# ---------------- provisioning (idempotent) ----------------
def ensure_r2():
    s, j = _api("POST", "/accounts/%s/r2/buckets" % ACCT, {"name": R2_BUCKET})
    return "ok" if (j.get("success") or s == 409 or "already" in json.dumps(j).lower()) else j

def ensure_d1():
    s, j = _api("GET", "/accounts/%s/d1/database?name=%s" % (ACCT, D1_NAME))
    for db in (j.get("result") or []):
        if db.get("name") == D1_NAME:
            return db["uuid"]
    s, j = _api("POST", "/accounts/%s/d1/database" % ACCT, {"name": D1_NAME})
    return (j.get("result") or {}).get("uuid")

def d1_query(db, sql, params=None):
    return _api("POST", "/accounts/%s/d1/database/%s/query" % (ACCT, db),
                {"sql": sql, "params": params or []})

def ensure_d1_table(db):
    return d1_query(db, ("CREATE TABLE IF NOT EXISTS records ("
                         "canonical_id TEXT PRIMARY KEY, term TEXT, tier INTEGER, domain TEXT, "
                         "math TEXT, sha256 TEXT, status TEXT, provenance TEXT, root_path TEXT, updated_at TEXT)"))

def ensure_vectorize():
    s, j = _api("GET", "/accounts/%s/vectorize/v2/indexes/%s" % (ACCT, VEC_INDEX))
    if j.get("success"):
        return "ok"
    s, j = _api("POST", "/accounts/%s/vectorize/v2/indexes" % ACCT,
                {"name": VEC_INDEX, "config": {"dimensions": VEC_DIMS, "metric": "cosine"}})
    return "ok" if (j.get("success") or "already" in json.dumps(j).lower()) else j

def vec_upsert(cid, values, meta):
    line = json.dumps({"id": cid, "values": values, "metadata": meta})
    return _api("POST", "/accounts/%s/vectorize/v2/indexes/%s/upsert" % (ACCT, VEC_INDEX), line, ndjson=True)

# ---------------- watermark (dedup state) in R2 ----------------
WM_KEY = "state/watermark.json"

def load_watermark():
    s, body = _r2("GET", WM_KEY)
    if s == 200:
        try:
            return json.loads(body)
        except Exception:
            pass
    return {"seen": []}

def save_watermark(wm):
    s, _ = _r2("PUT", WM_KEY, json.dumps(wm).encode())
    return s

# ---------------- the write ----------------
def write_record(rec):
    """Persist one verified Grounding Record to R2 + D1 + Vectorize."""
    cid = rec["canonical_id"]
    # R2: full record
    r2s, _ = _r2("PUT", "records/%s.json" % cid, json.dumps(rec, indent=2).encode())
    # D1: index row
    d1s, _ = d1_query(ensure_d1_cache(), (
        "INSERT INTO records (canonical_id,term,tier,domain,math,sha256,status,provenance,root_path,updated_at) "
        "VALUES (?,?,?,?,?,?,?,?,?,?) ON CONFLICT(canonical_id) DO UPDATE SET "
        "term=excluded.term,math=excluded.math,status=excluded.status,updated_at=excluded.updated_at"),
        [cid, rec["term"], rec.get("tier"), rec.get("domain"), rec.get("math",""), rec.get("sha256",""),
         rec.get("status","verified"), rec.get("provenance",""), json.dumps(rec.get("root_path",[])),
         datetime.datetime.utcnow().isoformat()])
    # Vectorize: embedding of term + math
    import ingest_gate as ig
    vec = ig._embed([rec["term"].replace("_"," ") + " : " + rec.get("math","")])[0]
    vecs, _ = vec_upsert(cid, vec, {"term": rec["term"], "domain": rec.get("domain","")})
    return {"r2": r2s, "d1": d1s, "vectorize": vecs}

_D1_ID = None
def ensure_d1_cache():
    global _D1_ID
    if _D1_ID is None:
        _D1_ID = ensure_d1()
    return _D1_ID

def provision():
    return {"r2": ensure_r2(), "d1": ensure_d1_cache(), "d1_table": ensure_d1_table(ensure_d1_cache())[0], "vectorize": ensure_vectorize()}


def _writetest():
    print("provisioning owned stores…")
    p = provision(); print(" ", json.dumps({k: (v if not isinstance(v, tuple) else v[0]) for k, v in p.items()})[:200])
    rec = {"canonical_id": "GR-writetest-ke", "term": "kinetic_energy", "tier": 2,
           "root_path": ["E", "matter"], "domain": "physical", "math": "KE = 1/2 m v^2",
           "proof_kind": "definition", "provenance": "writetest", "sha256": "wt"*32, "status": "verified", "verifiable": True}
    print("writing record %s …" % rec["canonical_id"])
    res = write_record(rec); print("  write status:", res)
    # readback
    r2s, body = _r2("GET", "records/%s.json" % rec["canonical_id"])
    print("  R2 readback: HTTP %s, term=%s" % (r2s, (json.loads(body).get("term") if r2s == 200 else "-")))
    s, j = d1_query(ensure_d1_cache(), "SELECT canonical_id,term,status FROM records WHERE canonical_id=?", [rec["canonical_id"]])
    rows = (((j.get("result") or [{}])[0]).get("results")) if j.get("success") else None
    print("  D1 readback:", rows)
    print("DONE" if r2s == 200 and rows else "INCOMPLETE — check statuses above")


if __name__ == "__main__":
    import sys
    if "--writetest" in sys.argv:
        _writetest()
