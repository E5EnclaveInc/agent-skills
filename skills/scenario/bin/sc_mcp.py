"""Scenario MCP client: OAuth (DCR + device flow) + Streamable HTTP calls."""
import os, sys, json, time, secrets, hashlib, base64
import httpx

PROXY = os.environ.get("https_proxy") or os.environ.get("HTTPS_PROXY")
BASE = "https://mcp.scenario.com"
MCP_URL = BASE + "/mcp"
STATE = os.path.expanduser("~/.config/scenario-mcp.json")

def client():
    return httpx.Client(proxy=PROXY, trust_env=False, timeout=60)

def load():
    try: return json.load(open(STATE))
    except Exception: return {}

def save(s):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    json.dump(s, open(STATE, "w"))
    os.chmod(STATE, 0o600)

def register():
    c = client()
    r = c.post(BASE + "/oauth/register", json={
        "client_name": "Scenario MCP",
        "redirect_uris": ["http://127.0.0.1:9/callback"],
        "grant_types": ["authorization_code", "refresh_token",
                        "urn:ietf:params:oauth:grant-type:device_code"],
        "response_types": ["code"],
        "token_endpoint_auth_method": "none",
        "scope": "openid profile email",
    })
    r.raise_for_status()
    d = r.json()
    s = load(); s["client_id"] = d["client_id"]; save(s)
    return d["client_id"]

def device_start(client_id):
    c = client()
    r = c.post("https://clerk.scenario.com/oauth/device_authorization",
               data={"client_id": client_id, "scope": "openid profile email"})
    r.raise_for_status()
    return r.json()

def device_poll(client_id, device_code, interval):
    c = client()
    while True:
        time.sleep(interval)
        r = c.post(BASE + "/oauth/token", data={
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            "device_code": device_code, "client_id": client_id})
        d = r.json()
        if "access_token" in d:
            s = load(); s["tokens"] = d; save(s); return d
        if d.get("error") not in ("authorization_pending", "slow_down"):
            return d

def refresh():
    s = load(); t = s.get("tokens", {})
    c = client()
    r = c.post(BASE + "/oauth/token", data={
        "grant_type": "refresh_token", "refresh_token": t.get("refresh_token"),
        "client_id": s.get("client_id")})
    if r.status_code == 200:
        d = r.json(); t.update(d); s["tokens"] = t; save(s); return t["access_token"]
    return None

def token():
    s = load(); t = s.get("tokens")
    if not t: return None
    return t.get("access_token")

def call(method, params=None):
    """One MCP JSON-RPC call over Streamable HTTP."""
    tok = token()
    if not tok:
        # try refresh once
        tok = refresh()
    c = client()
    headers = {"Content-Type": "application/json",
               "Accept": "application/json, text/event-stream"}
    if tok: headers["Authorization"] = f"Bearer {tok}"
    body = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params or {}}
    # initialize handshake first (stateless attempt)
    r = c.post(MCP_URL, json={"jsonrpc":"2.0","id":0,"method":"initialize",
        "params":{"protocolVersion":"2025-03-26","capabilities":{},
                  "clientInfo":{"name":"scenario-skill","version":"0.1"}}},
        headers=headers)
    sess = r.headers.get("mcp-session-id")
    if sess: headers["Mcp-Session-Id"] = sess
    r = c.post(MCP_URL, json=body, headers=headers)
    if r.status_code == 401 and refresh():
        return call(method, params)
    r.raise_for_status()
    # parse SSE or JSON
    txt = r.text
    if txt.startswith("event:"):
        # take last data: block
        datas = [l[5:].strip() for l in txt.splitlines() if l.startswith("data:")]
        return json.loads(datas[-1]) if datas else {"raw": txt[:500]}
    return r.json()

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "register":
        print("client_id:", register())
    elif cmd == "device":
        s = load()
        cid = s.get("client_id") or register()
        d = device_start(cid)
        print(json.dumps(d, indent=2))
    elif cmd == "poll":
        s = load(); cid = s["client_id"]
        d = json.load(open(sys.argv[2]))
        print(json.dumps(device_poll(cid, d["device_code"], d.get("interval", 5)), indent=2)[:300])
    elif cmd == "call":
        print(json.dumps(call(sys.argv[2], json.loads(sys.argv[3]) if len(sys.argv) > 3 else None), indent=2)[:4000])
