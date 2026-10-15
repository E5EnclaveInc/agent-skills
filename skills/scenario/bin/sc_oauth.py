"""Authorization-code + PKCE via loopback listener. Prints the authorize URL,
waits for the callback, exchanges the code, saves tokens."""
import os, json, secrets, hashlib, base64, threading, time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, urlencode
import httpx

PROXY = os.environ.get("https_proxy") or os.environ.get("HTTPS_PROXY")
BASE = "https://mcp.scenario.com"
STATE = os.path.expanduser("~/.config/scenario-mcp.json")
s = json.load(open(STATE)); CID = s["client_id"]

verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=").decode()
challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
state = secrets.token_urlsafe(16)
code_holder = {}

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        q = parse_qs(urlparse(self.path).query)
        code_holder.update(q)
        self.send_response(200); self.send_header("Content-Type","text/html"); self.end_headers()
        self.wfile.write(b"<h1>Signed in. You can close this tab and return to your agent.</h1>")
    def log_message(self, *a): pass

srv = HTTPServer(("127.0.0.1", 0), H)
port = srv.server_address[1]
redir = f"http://127.0.0.1:{port}/callback"
params = {"client_id": CID, "redirect_uri": redir, "response_type": "code",
          "scope": "openid profile email offline_access",
          "code_challenge": challenge, "code_challenge_method": "S256",
          "state": state, "resource": BASE + "/mcp"}
url = BASE + "/oauth/authorize?" + urlencode(params)
print("AUTHORIZE_URL=" + url)
t = threading.Thread(target=srv.handle_request, daemon=True); t.start()
deadline = time.time() + 600
while time.time() < deadline and "code" not in code_holder:
    time.sleep(1)
srv.server_close()
if "code" not in code_holder:
    print("TIMEOUT waiting for callback"); raise SystemExit(1)
c = httpx.Client(proxy=PROXY, trust_env=False, timeout=60)
r = c.post(BASE + "/oauth/token", data={
    "grant_type": "authorization_code", "code": code_holder["code"][0],
    "redirect_uri": redir, "client_id": CID, "code_verifier": verifier,
    "resource": BASE + "/mcp"})
r.raise_for_status()
toks = r.json(); s["tokens"] = toks; s["redirect_uri"] = redir
json.dump(s, open(STATE, "w")); os.chmod(STATE, 0o600)
print("TOKEN_OK scopes=", toks.get("scope"))
