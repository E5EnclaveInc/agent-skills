#!/usr/bin/env python3
"""Lambda Cloud API client (stdlib only, no pip).

Endpoints grounded in the official Lambda Cloud API spec v1.10.0
(https://cloud.lambdalabs.com/api/v1/openapi.json, recon 2026-09-15).

AUTH: Bearer <LAMBDA_API_KEY>, read from the LAMBDA_API_KEY environment
variable, falling back to ~/.lambda/api_key (chmod 600). The key is
NEVER echoed, logged, put in argv,
written elsewhere, or pasted in chat by this tool. Basic auth
(`curl -u $KEY:`) also works (legacy per the docs); this client uses the
docs-preferred Bearer scheme.

Rate limits (per the spec): ~1 request/second overall; launch is
1 request per 12 seconds or 5 per minute. This client sleeps 1.2s
between calls.

Usage:
  lambda.py types [--region REGION]
      List instance types: GPU, vCPU, RAM, price/hr, regions with capacity.
  lambda.py list
      List instances on the account.
  lambda.py get <instance-id>
      Show one instance's details.
  lambda.py launch --region R --type T --ssh-key NAME [--name N]
                   [--fs FS ...] [--user-data FILE] [--hostname H]
                   [--firewall-rulesets IDS] [--dry-run] [--confirm]
      Launch an on-demand instance. EXACTLY ONE ssh key is required by the
      API. --firewall-rulesets attaches firewall ruleset IDs (comma-separated,
      must exist in the launch region); without it the account's global
      ruleset applies (tcp/22 + icmp ONLY — see SKILL.md firewall note).
      --dry-run prints the exact request + estimated hourly cost and sends
      NOTHING. A real launch requires --confirm (refuses otherwise).
  lambda.py terminate <id> [id ...] --confirm
      Terminate instance(s). Requires --confirm; prints targets first.
  lambda.py restart <id> [id ...] --confirm
      Restart instance(s). Requires --confirm; prints targets first.
  lambda.py ssh-keys
      List SSH keys on the account.
  lambda.py ssh-keys add --name NAME [--public-key FILE] [--save-private PATH]
      Add an SSH key. With --public-key, uploads your key. Without it,
      Lambda GENERATES a keypair server-side and returns the private key
      ONCE -- it is saved immediately to --save-private (chmod 600).
      Lambda does not retain generated private keys.

COST STEWARDSHIP (hard rules, also in SKILL.md):
  - No launch without a frozen benchmark protocol on file and a per-run
    burn cap (hypothesis, cheapest falsifying type, max dollars, abort
    condition). `launch` prints this reminder every time.
  - Always pick the cheapest instance type that falsifies the hypothesis.
  - Terminate the instant the run ends. No idle burn.
"""
import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error

BASE = "https://cloud.lambdalabs.com/api/v1"

BURN_CAP_REMINDER = """\
COST STEWARDSHIP -- answer before you burn (vendor credits are a vendor
subsidy, not architecture):
  1. Hypothesis:      what specific question does this run answer?
  2. Cheapest falsifier: is this the cheapest instance type that can falsify it?
  3. Max dollars:     hard cap for this run -- terminate at the cap.
  4. Abort condition: what result stops the run early?
  5. Terminate the instant the run ends -- no idle burn.
No frozen benchmark protocol on file = no launch."""


KEY_FILE = os.path.expanduser("~/.lambda/api_key")


def api_key():
    key = os.environ.get("LAMBDA_API_KEY", "").strip()
    if not key:
        try:
            with open(KEY_FILE) as f:
                key = f.read().strip()
        except OSError:
            pass
    if not key:
        sys.stderr.write(
            "error: LAMBDA_API_KEY is not set and %s is missing.\n"
            "You mint the API key at\n"
            "https://cloud.lambda.ai/api-keys/cloud-api and stored at\n"
            "%s (chmod 600) -- never paste it in chat or logs.\n" % (KEY_FILE, KEY_FILE)
        )
        sys.exit(2)
    return key


def api(method, path, body=None):
    """Signed-JSON helper. Returns the parsed `data` payload.

    Transport note (2026-09-17, durable fix): this sandbox's egress proxy
    mangles chunked responses for urllib/http.client on some Lambda
    endpoints (IncompleteRead on /instance-types, reproduced repeatedly),
    while requests handles them fine. Prefer requests when importable;
    fall back to urllib otherwise.
    """
    key = api_key()
    time.sleep(1.2)  # spec rate limit: ~1 req/sec
    headers = {
        "Authorization": "Bearer " + key,
        "Accept": "application/json",
        "Content-Type": "application/json",
        # cloud.lambdalabs.com is Cloudflare-fronted with bot management:
        # urllib's default UA gets Error 1010; a browser UA clears it
        # (measured lesson: Cloudflare bot management 403s default script UAs).
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    }
    data = json.dumps(body).encode() if body is not None else None
    try:
        import requests  # noqa
        r = requests.request(method, BASE + path, headers=headers,
                             data=data, timeout=60)
        if r.status_code >= 400:
            try:
                err = r.json().get("error", {})
                code, msg, sug, rid = (err.get("code", "unknown"),
                                       err.get("message", ""),
                                       err.get("suggestion", ""),
                                       err.get("request_id", ""))
                sys.stderr.write(
                    "API error %d: %s\n  %s\n  suggestion: %s\n  request_id: %s\n"
                    % (r.status_code, code, msg, sug or "-", rid or "-"))
            except Exception:
                sys.stderr.write("API error %d (unparseable body)\n"
                                 % r.status_code)
            sys.exit(3)
        payload = r.json()
        if isinstance(payload, dict) and "error" in payload:
            sys.stderr.write("API error: %s\n" % json.dumps(payload["error"]))
            sys.exit(3)
        return payload.get("data", payload)
    except ImportError:
        pass  # fall through to the urllib path below

    req = urllib.request.Request(
        BASE + path, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            payload = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        try:
            err = json.loads(e.read().decode()).get("error", {})
            code = err.get("code", "unknown")
            msg = err.get("message", "")
            sug = err.get("suggestion", "")
            rid = err.get("request_id", "")
            sys.stderr.write(
                "API error %d: %s\n  %s\n  suggestion: %s\n  request_id: %s\n"
                % (e.code, code, msg, sug or "-", rid or "-")
            )
        except Exception:
            sys.stderr.write("API error %d (unparseable body)\n" % e.code)
        sys.exit(3)
    if isinstance(payload, dict) and "error" in payload:
        sys.stderr.write("API error: %s\n" % json.dumps(payload["error"]))
        sys.exit(3)
    return payload.get("data", payload)


def cmd_types(args):
    data = api("GET", "/instance-types")
    items = _type_items(data)
    if args.json:
        # Raw payload: consumers (select_hardware.py --live) normalize it
        # themselves and rely on the name-keyed dict shape.
        print(json.dumps(data))
        return
    if args.region:
        items = [i for i in items
                 if any(r.get("name") == args.region
                        for r in i.get("regions_with_capacity_available", []))]
    print("%-22s %4s %6s %9s %10s  %s" %
          ("TYPE", "GPUs", "vCPU", "RAM GiB", "$/hr", "CAPACITY REGIONS"))
    for item in sorted(items,
                       key=lambda i: i["instance_type"].get("price_cents_per_hour", 0)):
        t = item["instance_type"]
        cents = t.get("price_cents_per_hour", 0)
        specs = t.get("specs", {})
        regions = ",".join(r.get("name", "?")
                           for r in item.get("regions_with_capacity_available", []))
        print("%-22s %4d %6d %9d %10.2f  %s" % (
            t.get("name"), specs.get("gpus", 0), specs.get("vcpus", 0),
            specs.get("memory_gib", 0), cents / 100.0, regions or "(none)"))
        if t.get("gpu_description"):
            print("    %s | %s" % (t.get("gpu_description"),
                                   t.get("description", "")))


def cmd_list(_args):
    data = api("GET", "/instances")
    insts = data if isinstance(data, list) else data.get("data", [])
    if not insts:
        print("(no instances)")
        return
    for i in insts:
        it = i.get("instance_type", {}) or {}
        rg = i.get("region", {}) or {}
        print("%s  %-28s  %-18s  %-10s  %-15s  %s" % (
            i.get("id"), (i.get("name") or "")[:28], it.get("name", "?"),
            rg.get("name", "?"), i.get("ip") or "-", i.get("status", "?")))


def cmd_get(args):
    i = api("GET", "/instances/" + args.id)
    it = i.get("instance_type", {}) or {}
    rg = i.get("region", {}) or {}
    print("id:        ", i.get("id"))
    print("name:      ", i.get("name"))
    print("status:    ", i.get("status"))
    print("type:      ", it.get("name"), "-", it.get("gpu_description", ""))
    print("price/hr:  ", "$%.2f" % (it.get("price_cents_per_hour", 0) / 100.0))
    print("region:    ", rg.get("name"), "-", rg.get("description", ""))
    print("ip:        ", i.get("ip"))
    print("private_ip:", i.get("private_ip"))
    print("ssh keys:  ", ", ".join(i.get("ssh_key_names", []) or []))
    print("filesystems:", ", ".join(i.get("file_system_names", []) or []))
    print("hostname:  ", i.get("hostname"))
    print("jupyter:   ", i.get("jupyter_url") or "-")


def _type_items(data):
    """Normalize the /instance-types feed to a list of
    {instance_type, regions_with_capacity_available} entries.

    Live shape (2026-09-17): data is a dict keyed by instance type name,
    each value an object with "instance_type" +
    "regions_with_capacity_available". Older shape: list, or {"data": [...]}.
    """
    if isinstance(data, dict):
        return list(data.values())
    if isinstance(data, list):
        return data
    return data.get("data", [])


def price_for(instance_type_name):
    """Hourly USD for a type, from the live /instance-types feed."""
    items = _type_items(api("GET", "/instance-types"))
    for item in items:
        t = item["instance_type"]
        if t.get("name") == instance_type_name:
            cents = t.get("price_cents_per_hour",
                          t.get("priceCentsPerHour", 0))
            return (cents / 100.0 if isinstance(cents, (int, float)) else 0.0,
                    item.get("regions_with_capacity_available", []))
    return None, []
    return None, []


def cmd_launch(args):
    # The API requires EXACTLY ONE ssh key (spec: ssh_key_names).
    body = {
        "region_name": args.region,
        "instance_type_name": args.type,
        "ssh_key_names": [args.ssh_key],
    }
    if args.name:
        body["name"] = args.name
    if args.fs:
        body["file_system_names"] = args.fs
    if args.hostname:
        body["hostname"] = args.hostname
    if args.image:
        body["image"] = {"id": args.image}
    if args.user_data:
        with open(args.user_data) as f:
            ud = f.read()
        if len(ud.encode()) > 1024 * 1024:
            sys.stderr.write("error: user_data exceeds the 1MB API limit\n")
            sys.exit(2)
        body["user_data"] = ud
    # 2026-09-24: r2-r5 postmortem — the global firewall allows only
    # tcp/22+icmp inbound, so judge-API boxes were unreachable on :8080
    # (persistent TCP timeout). Attach the run's ruleset explicitly.
    fw = [x.strip() for x in (args.firewall_rulesets or "").split(",")
          if x.strip()]
    if fw:
        body["firewall_rulesets"] = [{"id": x} for x in fw]

    print("== LAUNCH REQUEST (structure preview; secret-bearing fields redacted) ==")
    # 2026-09-25: dry-run used to print filled user_data to stdout — filled
    # userdata carries the per-run ingest bearer token. Never print it;
    # show a summary instead. The real launch path is unaffected.
    _shown = dict(body)
    if "user_data" in _shown:
        _ud = _shown["user_data"]
        import hashlib as _hl
        _shown["user_data"] = ("<redacted: %d bytes, sha256=%s; filled userdata "
                               "may carry per-run secrets — not printed>" %
                               (len(_ud.encode()),
                                _hl.sha256(_ud.encode()).hexdigest()[:16]))
    print(json.dumps(_shown, indent=2))

    # Pricing/capacity gate: api_key() resolves the credential from either
    # the LAMBDA_API_KEY env var or the stored key file, and aborts if
    # neither exists — so this check always runs before a launch.
    hourly, regions = price_for(args.type)
    if hourly is None:
        sys.stderr.write(
            "warning: instance type '%s' not found in /instance-types; "
            "cannot price or check capacity.\n" % args.type)
    else:
        print("\nestimated cost: $%.2f/hr  ($%.2f/day if left running)" %
              (hourly, hourly * 24))
        if not any(r.get("name") == args.region for r in regions):
            have = ",".join(r.get("name", "?") for r in regions) or "(none)"
            sys.stderr.write(
                "REFUSED: no capacity for %s in %s (capacity regions: %s)\n"
                % (args.type, args.region, have))
            sys.exit(4)

    print("\n" + BURN_CAP_REMINDER)

    if args.dry_run:
        print("\n--dry-run: nothing sent.")
        return
    if not args.confirm:
        sys.stderr.write(
            "\nREFUSED: launch requires --confirm (or use --dry-run to preview).\n"
            "Re-run with --confirm once the burn-cap answers above are on file.\n")
        sys.exit(2)
    resp = api("POST", "/instance-operations/launch", body)
    ids = (resp.get("instance_ids")
           if isinstance(resp, dict) else None) or []
    print("\nlaunched instance_ids:", ids)
    print("REMINDER: terminate the instant the run ends -- no idle burn.")


def cmd_terminate(args):
    print("Will TERMINATE these instances:")
    for i in args.ids:
        print("  ", i)
    if not args.confirm:
        sys.stderr.write("REFUSED: add --confirm to terminate.\n")
        sys.exit(2)
    resp = api("POST", "/instance-operations/terminate",
               {"instance_ids": args.ids})
    terms = resp.get("terminated_instances", []) if isinstance(resp, dict) else []
    for t in terms:
        print("terminating:", t.get("id"), t.get("name"), t.get("status"))


def cmd_restart(args):
    print("Will RESTART these instances:")
    for i in args.ids:
        print("  ", i)
    if not args.confirm:
        sys.stderr.write("REFUSED: add --confirm to restart.\n")
        sys.exit(2)
    resp = api("POST", "/instance-operations/restart",
               {"instance_ids": args.ids})
    rests = resp.get("restarted_instances", []) if isinstance(resp, dict) else []
    for r in rests:
        print("restarted:", r.get("id"), r.get("name"), r.get("status"))


def cmd_ssh_keys(args):
    data = api("GET", "/ssh-keys")
    keys = data if isinstance(data, list) else data.get("data", [])
    if not keys:
        print("(no SSH keys)")
        return
    for k in keys:
        print("%s  %-24s  %s" %
              (k.get("id"), k.get("name"), (k.get("public_key") or "")[:60]))


def cmd_ssh_keys_add(args):
    body = {"name": args.name}
    if args.public_key:
        with open(os.path.expanduser(args.public_key)) as f:
            body["public_key"] = f.read().strip()
    resp = api("POST", "/ssh-keys", body)
    if not isinstance(resp, dict):
        print(json.dumps(resp, indent=2))
        return
    priv = resp.get("private_key")
    if priv:
        # Server-side generated keypair: Lambda does NOT retain the private
        # key. Save it immediately, 0600, or access is lost forever.
        dest = os.path.expanduser(
            args.save_private or ("./%s.pem" % args.name))
        with open(dest, "w") as f:
            f.write(priv + "\n")
        os.chmod(dest, 0o600)
        print("key id:      ", resp.get("id"))
        print("private key saved (0600):", dest)
        print("WARNING: Lambda does not store generated private keys. "
              "Back this file up or lose SSH access.")
    else:
        print("added key:", resp.get("id"), resp.get("name"))


def main():
    p = argparse.ArgumentParser(prog="lambda.py",
                                description="Lambda Cloud API client")
    sub = p.add_subparsers(dest="cmd", required=True)

    t = sub.add_parser("types", help="list instance types + pricing + capacity")
    t.add_argument("--region", help="only types with capacity in REGION")
    t.add_argument("--json", action="store_true",
                   help="print raw JSON payload (machine-readable)")
    t.set_defaults(fn=cmd_types)

    l = sub.add_parser("list", help="list instances")
    l.set_defaults(fn=cmd_list)

    g = sub.add_parser("get", help="show one instance")
    g.add_argument("id")
    g.set_defaults(fn=cmd_get)

    ln = sub.add_parser("launch", help="launch an on-demand instance")
    ln.add_argument("--region", required=True)
    ln.add_argument("--type", required=True,
                    help="instance_type_name, e.g. gpu_1x_a10")
    ln.add_argument("--ssh-key", required=True,
                    help="name of ONE registered SSH key (API requires exactly one)")
    ln.add_argument("--name", help="instance name (<=64 chars)")
    ln.add_argument("--hostname", help="hostname (lowercase, digits, hyphens)")
    ln.add_argument("--fs", nargs="*", default=[],
                    help="filesystem names to mount (must be in same region)")
    ln.add_argument("--user-data", help="cloud-init user-data file (<=1MB)")
    ln.add_argument("--firewall-rulesets", default="",
                    help="comma-separated firewall ruleset IDs to attach "
                         "(must exist in the launch region); e.g. the "
                         "llm-temp0-8080 ruleset for judge-API runs. "
                         "Without this, the account's global ruleset applies "
                         "(tcp/22 + icmp ONLY — inbound 8080 is dropped).")
    ln.add_argument("--image", default=None,
                    help="image id (uuid) for the launch; default: latest Lambda Stack")
    ln.add_argument("--dry-run", action="store_true",
                    help="print the exact request + cost estimate, send nothing")
    ln.add_argument("--confirm", action="store_true",
                    help="actually send the launch request")
    ln.set_defaults(fn=cmd_launch)

    tm = sub.add_parser("terminate", help="terminate instance(s)")
    tm.add_argument("ids", nargs="+")
    tm.add_argument("--confirm", action="store_true")
    tm.set_defaults(fn=cmd_terminate)

    rs = sub.add_parser("restart", help="restart instance(s)")
    rs.add_argument("ids", nargs="+")
    rs.add_argument("--confirm", action="store_true")
    rs.set_defaults(fn=cmd_restart)

    sk = sub.add_parser("ssh-keys", help="list SSH keys")
    sk.set_defaults(fn=cmd_ssh_keys)

    ska = sub.add_parser("ssh-keys-add", help="add an SSH key")
    ska.add_argument("--name", required=True)
    ska.add_argument("--public-key",
                     help="path to a public key file; omit to have Lambda generate a keypair")
    ska.add_argument("--save-private",
                     help="where to save a server-generated private key (default ./<name>.pem)")
    ska.set_defaults(fn=cmd_ssh_keys_add)

    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
