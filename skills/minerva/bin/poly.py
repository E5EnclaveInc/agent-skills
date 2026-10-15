#!/usr/bin/env python3
"""Polymarket API — public Gamma/CLOB data keyless; authenticated trading via CLOB credentials.
PAPER DOCTRINE: live orders are RED-gated — the order path refuses without BOTH --arm and
POLY_ARMED=ARM (per-session arming ceremony). Reads never need arming.
US-status note: keep your own compliance memo with your trading records; the operator
holds the accounts and the decision. This tool enforces the arm gate regardless.
Usage:
  poly.py crypto [--limit N]          # public: active crypto-tag markets w/ prices
  poly.py market <condition_id>       # public: market detail via gamma
  poly.py book <token_id>             # public: CLOB order book
  poly.py balance                     # authed: requires py-clob-client (pip) + credentials
  poly.py order <token_id> <buy|sell> <price> <size> [--arm]   # authed + ARMED only
"""
import json, os, sys, urllib.request

GAMMA = "https://gamma-api.polymarket.com"
CLOB = "https://clob.polymarket.com"

def get(url):
    r = urllib.request.Request(url, headers={"User-Agent": "minerva-poly/0.1"})
    with urllib.request.urlopen(r, timeout=30) as x: return json.loads(x.read())

def need_creds():
    pk = os.environ.get("POLY_KEY_TEXT", "") or os.environ.get("POLY_PRIVATE_KEY", "")
    if not pk:
        sys.exit("credentials not configured — paste the wallet key into the skill vault first")
    return pk

def funder_address():
    """Derived from the private key — never asked for separately."""
    from eth_account import Account
    pk = need_creds()
    return Account.from_key(pk if pk.startswith("0x") else "0x" + pk).address

def place_order_idempotent(order_args, clob_client):
    """Fire-and-read order contract for the arming ceremony (Base44 A1).

    When py-clob-client is wired, the ceremony calls this (not a raw POST):
    mint client id -> lookup by client id -> POST once -> on ambiguous
    error, lookup again BEFORE any resend. Never blind-resend.
    clob_client: an authenticated py-clob-client ClobClient.
    order_args: dict with token_id, side ("BUY"/"SELL"), price, size.
    """
    import sys as _sys, os as _os
    _here = _os.path.dirname(_os.path.abspath(__file__))
    _sys.path.insert(0, _os.path.join(_here, "..", "..", "..", "trading"))
    try:
        import order_idempotency as _idem
    except ImportError:
        _sys.exit("REFUSED: order_idempotency module unavailable — will not place orders without the fire-and-read guard.")
    coid = _idem.new_client_order_id("e5")
    def _lookup():
        # CLOB: fetch open orders and match our client id (field name
        # verified against the live client at the arming ceremony).
        try:
            orders = clob_client.get_orders() or []
        except Exception:
            return None
        for o in orders:
            oid = o.get("client_order_id", o.get("id")) if isinstance(o, dict) else None
            if oid == coid:
                return o
        return None
    def _send():
        from py_clob_client.clob_types import OrderArgs, OrderType
        return clob_client.create_and_post_order(OrderArgs(
            token_id=order_args["token_id"],
            side=order_args["side"], price=order_args["price"],
            size=order_args["size"], type=OrderType.GTC,
        ), client_order_id=coid)
    return _idem.fire_and_read(coid, _send, _lookup)

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "crypto":
        lim = sys.argv[sys.argv.index("--limit")+1] if "--limit" in sys.argv else "20"
        ms = get(f"{GAMMA}/markets?limit={lim}&active=true&closed=false&tag_id=21")
        for m in (ms if isinstance(ms, list) else []):
            print(json.dumps({"q": m.get("question"), "prices": m.get("outcomePrices"),
                              "end": m.get("endDate"), "condition_id": m.get("conditionId")}))
    elif cmd == "market":
        print(json.dumps(get(f"{GAMMA}/markets?condition_ids={sys.argv[2]}"), indent=1)[:3000])
    elif cmd == "book":
        print(json.dumps(get(f"{CLOB}/book?token_id={sys.argv[2]}"), indent=1)[:3000])
    elif cmd == "address":
        print(funder_address())
    elif cmd in ("balance", "order"):
        need_creds()
        if cmd == "order" and ("--arm" not in sys.argv or os.environ.get("POLY_ARMED") != "ARM"):
            sys.exit("REFUSED: live orders are RED-gated. Requires --arm AND POLY_ARMED=ARM. Paper doctrine stands until then.")
        sys.exit("authed path requires py-clob-client — installed and wired at the arming ceremony, not before (deliberate: no order code runs until the operator arms)")
    else:
        print(__doc__)
