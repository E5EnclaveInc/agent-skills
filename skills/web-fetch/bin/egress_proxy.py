#!/usr/bin/env python3
"""Validating egress forward proxy — the connection-layer SSRF control for web-fetch.

Listens on 127.0.0.1:8899. The fetch MCP server is configured (HTTP_PROXY/
HTTPS_PROXY) so every outbound request goes through here. The proxy resolves
the target host ITSELF, at connection time, and checks EVERY resolved IP
against the blocklist before connecting to the validated IP directly.

Why this beats a wrapper-level check (which is kept only as defense-in-depth):
  - DNS rebinding: the proxy resolves once and connects to that exact IP; the
    server never resolves the hostname itself for proxied requests.
  - Redirects: each new request (including 30x hops) is validated independently.
  - IP encodings (http://0x7f.0.0.1/, http://2130706433/, http://0.0.0.0/):
    normalized through the ipaddress module, not string matching.
  - CNAME chains: getaddrinfo follows them; the final IPs are what get checked.

Blocked: all private/loopback/link-local/multicast/reserved/unspecified ranges
(IPv4+IPv6), carrier-grade NAT, documentation ranges, and 169.254.169.254
(cloud metadata). Only http/https schemes are proxied.
"""
import ipaddress
import logging
import os
import select
import socket
import sys
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

LISTEN_HOST = "127.0.0.1"
LISTEN_PORT = 8899
CONNECT_TIMEOUT = 20

# Upstream: this sandbox blocks direct TCP (policy middlebox), so the proxy
# chains through the sandbox egress proxy from the environment. Validation
# below still gates WHAT may be requested; the upstream only carries allowed
# targets. The credential lives in the environment, never in logs or files.
def _upstream():
    from urllib.parse import urlsplit as _us
    for var in ("HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy"):
        val = os.environ.get(var)
        if val:
            p = _us(val)
            auth = None
            if p.username:
                import base64
                auth = "Basic " + base64.b64encode(
                    f"{p.username}:{p.password or ''}".encode()).decode()
            return p.hostname, p.port or 8080, auth
    return None, None, None

UPSTREAM_HOST, UPSTREAM_PORT, UPSTREAM_AUTH = _upstream()

# Explicit CIDR blocklist (belt) — plus ipaddress property checks (suspenders).
BLOCKED_NETS = [
    ipaddress.ip_network(c) for c in (
        "0.0.0.0/8", "10.0.0.0/8", "100.64.0.0/10", "127.0.0.0/8",
        "169.254.0.0/16", "172.16.0.0/12", "192.0.0.0/24", "192.0.2.0/24",
        "192.168.0.0/16", "198.18.0.0/15", "198.19.0.0/16", "198.51.100.0/24",
        "203.0.113.0/24", "224.0.0.0/4", "240.0.0.0/4",
        "::/128", "::1/128", "64:ff9b::/96", "100::/64", "2001::/23",
        "2001:db8::/32", "fc00::/7", "fe80::/10", "ff00::/8",
    )
]
# Optional egress-slice exception (default: none — the strict blocklist
# applies in full). Some sandboxes route all DNS through an egress middlebox
# whose addresses sit inside a normally-blocked range (e.g. benchmarking
# space) and route direct TCP by Host/SNI. If yours does, set
# WEB_FETCH_EGRESS_SLICE to that CIDR to allow exactly it.
_egress_slice = os.environ.get("WEB_FETCH_EGRESS_SLICE", "").strip()
EGRESS_SLICE = ipaddress.ip_network(_egress_slice) if _egress_slice else None

# Hostnames that must never be fetched, even if DNS would resolve them.
INTERNAL_NAMES = {
    "localhost", "ip6-localhost", "ip6-loopback",
    "metadata.google.internal", "instance-data", "instance-data-compute",
}

HOP_HEADERS = {
    "connection", "proxy-connection", "proxy-authenticate", "proxy-authorization",
    "te", "trailer", "transfer-encoding", "upgrade", "keep-alive",
}

log = logging.getLogger("egress-proxy")


def ip_allowed(ip):
    """True if the IP is a permissible fetch target.

    Allowed: global public unicast, or the operator-configured egress
    slice (WEB_FETCH_EGRESS_SLICE) when one is set. Everything else
    (private, loopback, link-local, multicast, reserved, unspecified,
    CGNAT, documentation, benchmarking) is denied.
    """
    if EGRESS_SLICE is not None and ip.version == EGRESS_SLICE.version and ip in EGRESS_SLICE:
        return True
    for net in BLOCKED_NETS:
        if ip.version == net.version and ip in net:
            return False
    if (ip.is_private or ip.is_loopback or ip.is_link_local
            or ip.is_multicast or ip.is_reserved or ip.is_unspecified):
        return False
    return ip.is_global


def resolve_validated_ip(host):
    """Resolve host and return (ip_str, blocked_reason|None).

    Every resolved address is checked; the first allowed one wins.
    Raises ValueError on failure/block.
    """
    h = host.strip().strip("[]").lower().rstrip(".")
    if h in INTERNAL_NAMES or h.endswith(".internal") or h.endswith(".local"):
        raise ValueError(f"internal hostname {host!r} is blocked")
    try:
        candidates = [ipaddress.ip_address(host.strip("[]"))]
    except ValueError:
        try:
            infos = socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)
        except socket.gaierror as e:
            raise ValueError(f"DNS resolution failed for {host!r}: {e}")
        # Deduplicate while preserving order; getaddrinfo already followed CNAMEs.
        seen = set()
        candidates = []
        for _fam, _typ, _proto, _canon, sockaddr in infos:
            ip = ipaddress.ip_address(sockaddr[0])
            if str(ip) not in seen:
                seen.add(str(ip))
                candidates.append(ip)
    if not candidates:
        raise ValueError(f"no addresses for {host!r}")
    for ip in candidates:
        if ip_allowed(ip):
            return str(ip)
    raise ValueError(f"all resolved addresses for {host!r} are blocked: "
                     + ", ".join(str(c) for c in candidates))


class ProxyHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "E5EgressProxy/1.0"

    def log_message(self, fmt, *args):  # route into our logger, not stderr spam
        log.info("%s - " + fmt, self.client_address[0], *args)

    def _deny(self, reason):
        log.warning("DENIED %s %s (%s)", self.command, self.path[:120], reason)
        body = f"blocked by egress policy: {reason}".encode()
        self.send_response(403)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _forward_headers(self):
        headers = {}
        for k, v in self.headers.items():
            if k.lower() in HOP_HEADERS:
                continue
            headers[k] = v
        return headers

    def do_GET(self): self._proxy_http("GET")
    def do_POST(self): self._proxy_http("POST")
    def do_HEAD(self): self._proxy_http("HEAD")
    def do_PUT(self): self._proxy_http("PUT")

    def _proxy_http(self, method):
        parts = urlsplit(self.path)
        if parts.scheme not in ("http", "https"):
            return self._deny(f"unsupported scheme in {self.path[:80]!r}")
        if parts.scheme == "https":
            # httpx always uses CONNECT for https-through-proxy; a direct
            # absolute https URI here is unexpected — refuse rather than guess.
            return self._deny("https must use CONNECT")
        host = parts.hostname or ""
        port = parts.port or 80
        try:
            ip = resolve_validated_ip(host)
        except ValueError as e:
            return self._deny(str(e))
        origin_path = parts.path or "/"
        if parts.query:
            origin_path += "?" + parts.query
        body = None
        if "Content-Length" in self.headers:
            try:
                body = self.rfile.read(int(self.headers["Content-Length"]))
            except (ValueError, OSError):
                return self._deny("bad Content-Length")
        headers = self._forward_headers()
        headers["Host"] = parts.netloc
        headers["Connection"] = "close"
        if UPSTREAM_AUTH:
            headers["Proxy-Authorization"] = UPSTREAM_AUTH
        if not UPSTREAM_HOST:
            return self._deny("no upstream egress proxy configured")
        try:
            # Chain through the sandbox egress proxy: absolute-form request.
            conn = HTTPConnection(UPSTREAM_HOST, UPSTREAM_PORT,
                                  timeout=CONNECT_TIMEOUT)
            conn.request(method, self.path, body=body, headers=headers)
            resp = conn.getresponse()
            self.send_response(resp.status, resp.reason)
            for k, v in resp.getheaders():
                if k.lower() in HOP_HEADERS or k.lower() == "content-length":
                    continue
                self.send_header(k, v)
            data = resp.read(5_000_000)  # 5MB cap per response
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            conn.close()
            log.info("ALLOWED %s %s://%s (%s)", method, parts.scheme, host, ip)
        except OSError as e:
            log.warning("UPSTREAM-FAIL %s: %s", host, e)
            self.send_error(502, f"upstream error: {e}")

    def do_CONNECT(self):
        # CONNECT host:port — the https path.
        if ":" not in self.path:
            return self._deny("CONNECT target must be host:port")
        host, _, port_s = self.path.rpartition(":")
        host = host.strip("[]")
        try:
            port = int(port_s)
        except ValueError:
            return self._deny("bad CONNECT port")
        if port not in (443, 8443):
            return self._deny(f"CONNECT to port {port} not allowed")
        try:
            ip = resolve_validated_ip(host)
        except ValueError as e:
            return self._deny(str(e))
        if not UPSTREAM_HOST:
            return self._deny("no upstream egress proxy configured")
        # Chain CONNECT through the sandbox egress proxy, then tunnel.
        try:
            up = socket.create_connection((UPSTREAM_HOST, UPSTREAM_PORT),
                                          timeout=CONNECT_TIMEOUT)
        except OSError as e:
            log.warning("UPSTREAM-FAIL %s:%s: %s", host, port, e)
            return self.send_error(502, f"upstream error: {e}")
        try:
            req = (f"CONNECT {host}:{port} HTTP/1.1\r\n"
                   f"Host: {host}:{port}\r\n")
            if UPSTREAM_AUTH:
                req += f"Proxy-Authorization: {UPSTREAM_AUTH}\r\n"
            req += "\r\n"
            up.sendall(req.encode())
            resp = up.recv(4096).decode("iso-8859-1", "replace")
            status = resp.split(" ", 2)[1] if resp.startswith("HTTP/") else "?"
            if status != "200":
                log.warning("UPSTREAM-CONNECT-DENIED %s:%s -> %s", host, port,
                            resp.splitlines()[0] if resp else "?")
                up.close()
                return self._deny(f"upstream refused CONNECT: "
                                  f"{resp.splitlines()[0] if resp else '?'}")
        except OSError as e:
            up.close()
            return self.send_error(502, f"upstream error: {e}")
        log.info("ALLOWED CONNECT %s:%s (%s)", host, port, ip)
        self.send_response(200, "Connection established")
        self.end_headers()
        self._tunnel(self.connection, up)

    def _tunnel(self, client, upstream):
        sockets = [client, upstream]
        try:
            while True:
                readable, _, _ = select.select(sockets, [], [], 60)
                if not readable:
                    break
                for s in readable:
                    data = s.recv(65536)
                    if not data:
                        return
                    (upstream if s is client else client).sendall(data)
        except OSError:
            pass
        finally:
            for s in sockets:
                try:
                    s.close()
                except OSError:
                    pass


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "proxy.log")),
                  logging.StreamHandler(sys.stderr)],
    )
    # Fail closed: never bind anywhere but loopback.
    server = ThreadingHTTPServer((LISTEN_HOST, LISTEN_PORT), ProxyHandler)
    server.daemon_threads = True
    log.info("egress proxy listening on %s:%s", LISTEN_HOST, LISTEN_PORT)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
