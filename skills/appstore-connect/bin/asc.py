#!/usr/bin/env python3
"""
App Store Connect — ES256 JWT REST client.

Drives App Store Connect entirely by API: builds, export compliance,
TestFlight internal/external beta groups, testers, test information, and
external Beta App Review submission.

Credentials (env vars):
  APP_STORE_CONNECT_ISSUER_ID        - the Issuer ID (UUID) from ASC > Integrations
  APP_STORE_CONNECT_KEY_IDENTIFIER   - the Key ID (10 chars) of the API key
  APP_STORE_CONNECT_PRIVATE_KEY      - the .p8 private key contents (PEM; single-line OK)

Python 3.9 compatible. Depends on `cryptography` (stdlib otherwise).

Usage:
  python3 asc.py whoami
  python3 asc.py apps [--bundle com.example.app]
  python3 asc.py builds --app <APP_ID> [--limit 10]
  python3 asc.py build-get --build <BUILD_ID>
  python3 asc.py set-compliance --build <BUILD_ID> [--exempt false]
  python3 asc.py groups --app <APP_ID>
  python3 asc.py group-create --app <APP_ID> --name "Internal" --internal
  python3 asc.py group-add-build --group <GROUP_ID> --build <BUILD_ID>
  python3 asc.py tester-add --group <GROUP_ID> --email a@b.com --first First --last Last
  python3 asc.py set-feedback-email --app <APP_ID> --email a@b.com [--locale en-US]
  python3 asc.py set-review-detail --app <APP_ID> --first First --last Last --phone "+1..." --email a@b.com
  python3 asc.py submit-external --build <BUILD_ID> --group <GROUP_ID>
  python3 asc.py raw --method GET --path "/v1/apps/<APP_ID>/builds?limit=5"
"""
import os, sys, json, time, base64, argparse, urllib.request, urllib.error

API = "https://api.appstoreconnect.apple.com"

def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")

def normalize_pem(raw: str) -> str:
    """Reconstruct a canonical wrapped PEM from a possibly single-line .p8."""
    raw = raw.strip().replace("\\n", "\n")
    if "BEGIN" in raw and "\n" in raw and "-----\n" in raw:
        return raw
    # collapse to the base64 body, then rewrap 64-char lines
    body = raw
    for marker in ("-----BEGIN PRIVATE KEY-----", "-----END PRIVATE KEY-----",
                   "-----BEGIN EC PRIVATE KEY-----", "-----END EC PRIVATE KEY-----"):
        body = body.replace(marker, "")
    body = "".join(body.split())
    lines = [body[i:i+64] for i in range(0, len(body), 64)]
    return "-----BEGIN PRIVATE KEY-----\n" + "\n".join(lines) + "\n-----END PRIVATE KEY-----\n"

def _load_local_config():
    # Optional local config: .asc_config sits next to this script (see .asc_config.example).
    # Values here are defaults; real environment variables still win.
    cfg = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".asc_config")
    cfg = os.path.normpath(cfg)
    if os.path.exists(cfg):
        for line in open(cfg).read().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

_load_local_config()

def _env(*names):
    for n in names:
        v = os.environ.get(n)
        if v:
            return v
    raise KeyError("none of env vars set: " + ", ".join(names))

def make_jwt() -> str:
    issuer = _env("ASC_ISSUER_ID", "APP_STORE_CONNECT_ISSUER_ID").strip()
    kid = _env("ASC_KEY_ID", "APP_STORE_CONNECT_KEY_IDENTIFIER").strip()
    # Convenience: read the .p8 from disk if a path is given,
    # whether ASC_PRIVATE_KEY is unset or empty.
    p8path = os.environ.get("ASC_P8_PATH", "").strip()
    pem_raw = os.environ.get("ASC_PRIVATE_KEY", os.environ.get("APP_STORE_CONNECT_PRIVATE_KEY", ""))
    if pem_raw.strip():
        pem = normalize_pem(pem_raw)
    elif p8path and os.path.exists(p8path):
        pem = normalize_pem(open(p8path).read())
    else:
        raise KeyError("no ASC private key: set ASC_PRIVATE_KEY or ASC_P8_PATH")
    header = {"alg": "ES256", "kid": kid, "typ": "JWT"}
    now = int(time.time())
    payload = {"iss": issuer, "iat": now, "exp": now + 1080, "aud": "appstoreconnect-v1"}
    signing_input = (b64url(json.dumps(header, separators=(",", ":")).encode()) + "." +
                     b64url(json.dumps(payload, separators=(",", ":")).encode()))
    try:
        from cryptography.hazmat.primitives.serialization import load_pem_private_key
        from cryptography.hazmat.primitives.asymmetric import ec
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
        key = load_pem_private_key(pem.encode("utf-8"), password=None)
        der = key.sign(signing_input.encode("ascii"), ec.ECDSA(hashes.SHA256()))
        r, s = decode_dss_signature(der)
        sig = r.to_bytes(32, "big") + s.to_bytes(32, "big")
    except ModuleNotFoundError:
        # Sandbox fallback: pycryptodome (Crypto) is available where `cryptography` is not.
        # DSS 'fips-186-3' outputs the raw r||s concatenation (64 bytes) = exactly JWT ES256.
        from Crypto.PublicKey import ECC
        from Crypto.Signature import DSS
        from Crypto.Hash import SHA256
        key = ECC.import_key(pem)
        h = SHA256.new(signing_input.encode("ascii"))
        sig = DSS.new(key, "fips-186-3").sign(h)
    return signing_input + "." + b64url(sig)

def call(method: str, path: str, body=None):
    url = path if path.startswith("http") else API + path
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + make_jwt())
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            raw = r.read().decode("utf-8")
            return r.status, (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8")
        try:
            return e.code, json.loads(raw)
        except Exception:
            return e.code, {"raw": raw}

def out(status, payload):
    print(json.dumps({"status": status, "body": payload}, indent=2))
    return 0 if 200 <= status < 300 else 1

# ---- commands ----
def c_whoami(a):
    st, b = call("GET", "/v1/apps?limit=1")
    return out(st, b)

def c_apps(a):
    path = "/v1/apps?limit=200"
    if a.bundle:
        path += "&filter[bundleId]=" + a.bundle
    st, b = call("GET", path)
    if 200 <= st < 300:
        apps = [{"id": x["id"], "bundleId": x["attributes"].get("bundleId"),
                 "name": x["attributes"].get("name"),
                 "sku": x["attributes"].get("sku")} for x in b.get("data", [])]
        return out(st, apps)
    return out(st, b)

def c_builds(a):
    path = ("/v1/builds?filter[app]=%s&limit=%d&sort=-uploadedDate"
            "&include=preReleaseVersion" % (a.app, a.limit))
    st, b = call("GET", path)
    if 200 <= st < 300:
        rows = []
        for x in b.get("data", []):
            at = x["attributes"]
            rows.append({"id": x["id"], "version": at.get("version"),
                         "processingState": at.get("processingState"),
                         "uploadedDate": at.get("uploadedDate"),
                         "expired": at.get("expired"),
                         "usesNonExemptEncryption": at.get("usesNonExemptEncryption")})
        return out(st, rows)
    return out(st, b)

def c_build_get(a):
    st, b = call("GET", "/v1/builds/%s" % a.build)
    return out(st, b)

def c_set_compliance(a):
    exempt = (a.exempt.lower() == "true")
    body = {"data": {"type": "builds", "id": a.build,
                     "attributes": {"usesNonExemptEncryption": exempt}}}
    st, b = call("PATCH", "/v1/builds/%s" % a.build, body)
    return out(st, b)

def c_groups(a):
    st, b = call("GET", "/v1/betaGroups?filter[app]=%s&limit=200" % a.app)
    if 200 <= st < 300:
        rows = [{"id": x["id"], "name": x["attributes"].get("name"),
                 "isInternalGroup": x["attributes"].get("isInternalGroup"),
                 "hasAccessToAllBuilds": x["attributes"].get("hasAccessToAllBuilds"),
                 "publicLinkEnabled": x["attributes"].get("publicLinkEnabled"),
                 "publicLink": x["attributes"].get("publicLink")} for x in b.get("data", [])]
        return out(st, rows)
    return out(st, b)

def c_group_create(a):
    attrs = {"name": a.name}
    if a.internal:
        # internal groups: up to 100 testers who are ASC users, no review needed
        attrs["isInternalGroup"] = True
    body = {"data": {"type": "betaGroups", "attributes": attrs,
                     "relationships": {"app": {"data": {"type": "apps", "id": a.app}}}}}
    st, b = call("POST", "/v1/betaGroups", body)
    return out(st, b)

def c_group_add_build(a):
    body = {"data": [{"type": "builds", "id": a.build}]}
    st, b = call("POST", "/v1/betaGroups/%s/relationships/builds" % a.group, body)
    return out(st, b if b else {"ok": True})

def c_tester_add(a):
    body = {"data": {"type": "betaTesters",
                     "attributes": {"email": a.email, "firstName": a.first, "lastName": a.last},
                     "relationships": {"betaGroups": {"data": [{"type": "betaGroups", "id": a.group}]}}}}
    st, b = call("POST", "/v1/betaTesters", body)
    return out(st, b)

def c_set_feedback_email(a):
    # find existing betaAppLocalization for the locale
    st, b = call("GET", "/v1/apps/%s/betaAppLocalizations" % a.app)
    loc_id = None
    for x in b.get("data", []):
        if x["attributes"].get("locale") == a.locale:
            loc_id = x["id"]; break
    if loc_id:
        body = {"data": {"type": "betaAppLocalizations", "id": loc_id,
                         "attributes": {"feedbackEmail": a.email}}}
        st2, b2 = call("PATCH", "/v1/betaAppLocalizations/%s" % loc_id, body)
        return out(st2, b2)
    body = {"data": {"type": "betaAppLocalizations",
                     "attributes": {"locale": a.locale, "feedbackEmail": a.email},
                     "relationships": {"app": {"data": {"type": "apps", "id": a.app}}}}}
    st2, b2 = call("POST", "/v1/betaAppLocalizations", body)
    return out(st2, b2)

def c_set_review_detail(a):
    attrs = {"contactFirstName": a.first, "contactLastName": a.last,
             "contactPhone": a.phone, "contactEmail": a.email,
             "demoAccountRequired": False}
    # betaAppReviewDetails id == app id
    body = {"data": {"type": "betaAppReviewDetails", "id": a.app, "attributes": attrs}}
    st, b = call("PATCH", "/v1/betaAppReviewDetails/%s" % a.app, body)
    if st == 404:
        body = {"data": {"type": "betaAppReviewDetails", "attributes": attrs,
                         "relationships": {"app": {"data": {"type": "apps", "id": a.app}}}}}
        st, b = call("POST", "/v1/betaAppReviewDetails", body)
    return out(st, b)

def c_submit_external(a):
    body = {"data": {"type": "betaAppReviewSubmissions",
                     "relationships": {"build": {"data": {"type": "builds", "id": a.build}}}}}
    st, b = call("POST", "/v1/betaAppReviewSubmissions", body)
    return out(st, b)

def c_raw(a):
    body = json.loads(a.body) if a.body else None
    st, b = call(a.method, a.path, body)
    return out(st, b)

def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("whoami")
    s = sub.add_parser("apps"); s.add_argument("--bundle")
    s = sub.add_parser("builds"); s.add_argument("--app", required=True); s.add_argument("--limit", type=int, default=10)
    s = sub.add_parser("build-get"); s.add_argument("--build", required=True)
    s = sub.add_parser("set-compliance"); s.add_argument("--build", required=True); s.add_argument("--exempt", default="false")
    s = sub.add_parser("groups"); s.add_argument("--app", required=True)
    s = sub.add_parser("group-create"); s.add_argument("--app", required=True); s.add_argument("--name", required=True); s.add_argument("--internal", action="store_true")
    s = sub.add_parser("group-add-build"); s.add_argument("--group", required=True); s.add_argument("--build", required=True)
    s = sub.add_parser("tester-add"); s.add_argument("--group", required=True); s.add_argument("--email", required=True); s.add_argument("--first", default="Test"); s.add_argument("--last", default="Tester")
    s = sub.add_parser("set-feedback-email"); s.add_argument("--app", required=True); s.add_argument("--email", required=True); s.add_argument("--locale", default="en-US")
    s = sub.add_parser("set-review-detail"); s.add_argument("--app", required=True); s.add_argument("--first", required=True); s.add_argument("--last", required=True); s.add_argument("--phone", required=True); s.add_argument("--email", required=True)
    s = sub.add_parser("submit-external"); s.add_argument("--build", required=True); s.add_argument("--group", required=True)
    s = sub.add_parser("raw"); s.add_argument("--method", required=True); s.add_argument("--path", required=True); s.add_argument("--body")
    a = p.parse_args()
    fn = globals()["c_" + a.cmd.replace("-", "_")]
    sys.exit(fn(a))

if __name__ == "__main__":
    main()
