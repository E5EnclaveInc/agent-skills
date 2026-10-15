#!/usr/bin/env python3
"""Kalshi API — public market data keyless; authenticated account/trading via RSA-signed requests.
PAPER DOCTRINE: live orders are RED-gated — the place-order path refuses without BOTH --arm and
the operator's per-session arming (env KALSHI_ARMED=ARM). Reads never need arming.
Usage:
  kalshi.py markets <series> [--limit N]     # public: e.g. KXBTCD, KXETHD
  kalshi.py market <ticker>                  # public: single market detail
  kalshi.py balance                          # authed: account balance
  kalshi.py positions                        # authed: open positions
  kalshi.py order <ticker> <yes|no> <count> <price_cents> [--arm]   # authed + ARMED only
"""
import base64, datetime, json, os, sys, urllib.request

BASE = "https://api.elections.kalshi.com"

def pub(path):
    r = urllib.request.Request(BASE + path, headers={"User-Agent": "minerva-kalshi/0.1"})
    with urllib.request.urlopen(r, timeout=30) as x: return json.loads(x.read())

def _load_pem():
    # BRIDGE mode first: PEM staged from treasurebox (kalshi/private-key.pem) — survives vault delivery quirks
    bridge = os.environ.get("BRIDGE_DIR", "/tmp/.augbridge")
    bp = os.path.join(bridge, "kalshi-private-key.pem")
    if os.path.exists(bp):
        return open(bp, "rb").read()
    return _load_pem_env()

def _load_pem_env():
    """Accept the private key as raw multi-line PEM OR single-line base64 of the PEM
    (password fields fight multi-line pastes — base64 the whole file and paste one line)."""
    raw = (os.environ.get("KALSHI_PRIVATE_KEY_B64", "") or os.environ.get("KALSHI_PRIVATE_KEY_PEM", "")).strip()
    if not raw: return None
    if "BEGIN" in raw:
        # tolerate flattened PEM (newlines lost in paste): rebuild line structure
        if "\n" not in raw:
            import re
            m = re.match(r"(-----BEGIN [A-Z ]+-----)(.*)(-----END [A-Z ]+-----)$", raw)
            if m:
                head, body, tail = m.groups()
                body = body.replace(" ", "")
                raw = head + "\n" + "\n".join(body[i:i+64] for i in range(0, len(body), 64)) + "\n" + tail + "\n"
        return raw.encode()
    try:
        return base64.b64decode(raw)   # single-line base64 of the whole PEM file
    except Exception:
        return None

def _sign(method, path):
    key_id = os.environ.get("KALSHI_KEY_ID", "")
    pem = _load_pem()
    if not key_id or not pem: sys.exit("credentials not configured — need KALSHI_KEY_ID and KALSHI_PRIVATE_KEY_B64 (single-line base64 of the PEM file; raw PEM also accepted)")
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding
    ts = str(int(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1000))
    msg = (ts + method + path.split("?")[0]).encode()
    key = serialization.load_pem_private_key(pem, password=None)
    sig = key.sign(msg, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.DIGEST_LENGTH), hashes.SHA256())
    return {"KALSHI-ACCESS-KEY": key_id, "KALSHI-ACCESS-SIGNATURE": base64.b64encode(sig).decode(),
            "KALSHI-ACCESS-TIMESTAMP": ts, "Content-Type": "application/json", "User-Agent": "minerva-kalshi/0.1"}

def authed(method, path, body=None):
    req = urllib.request.Request(BASE + path, method=method, headers=_sign(method, path),
                                 data=json.dumps(body).encode() if body else None)
    with urllib.request.urlopen(req, timeout=30) as x: return json.loads(x.read())

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "markets":
        lim = sys.argv[sys.argv.index("--limit")+1] if "--limit" in sys.argv else "20"
        print(json.dumps(pub(f"/trade-api/v2/markets?series_ticker={sys.argv[2]}&status=open&limit={lim}"), indent=1)[:4000])
    elif cmd == "market":
        print(json.dumps(pub(f"/trade-api/v2/markets/{sys.argv[2]}"), indent=1))
    elif cmd == "balance":
        print(json.dumps(authed("GET", "/trade-api/v2/portfolio/balance"), indent=1))
    elif cmd == "positions":
        print(json.dumps(authed("GET", "/trade-api/v2/portfolio/positions"), indent=1))
    elif cmd == "order":
        if "--arm" not in sys.argv or os.environ.get("KALSHI_ARMED") != "ARM":
            sys.exit("REFUSED: live orders are RED-gated. Requires --arm AND KALSHI_ARMED=ARM (the operator's per-session arming ceremony). Paper doctrine stands until then.")
        # Fire-and-read idempotency (Base44 A1): import the shared guard;
        # fail CLOSED if it is unavailable — never place orders unguarded.
        _here = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, os.path.join(_here, "..", "..", "..", "trading"))
        try:
            import order_idempotency as _idem
        except ImportError:
            sys.exit("REFUSED: order_idempotency module unavailable — will not place orders without the fire-and-read guard.")
        t, side, count, px = sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
        coid = _idem.new_client_order_id("e5")
        body = {"ticker": t, "action": "buy", "side": side, "count": count, "type": "limit",
                ("yes_price" if side == "yes" else "no_price"): px,
                "client_order_id": coid}
        def _lookup():
            data = authed("GET", f"/trade-api/v2/portfolio/orders?ticker={t}&limit=100")
            for o in (data.get("orders", []) if isinstance(data, dict) else []):
                if isinstance(o, dict) and o.get("client_order_id") == coid:
                    return o
            return None
        def _send():
            return authed("POST", "/trade-api/v2/portfolio/orders", body)
        res = _idem.fire_and_read(coid, _send, _lookup)
        print(json.dumps(res, indent=1, default=str))
        if res["status"] == "ambiguous":
            sys.exit("AMBIGUOUS: POST outcome unknown and order not found on re-read. NO auto-resend — verify manually before any retry.")
    else:
        print(__doc__)
