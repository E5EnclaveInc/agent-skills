#!/usr/bin/env python3
"""Download an R2 object using the CLOUDFLARE_API_TOKEN environment
variable (scoped Bearer token; the token needs R2 read permission).
Usage: r2get.py <account_id> <bucket> <key> <out_path>
Streams the body to out_path. Prints sha256 of the downloaded bytes."""
import hashlib
import os
import sys
import urllib.request


def main() -> int:
    acct, bucket, key, out = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    token = os.environ.get("CLOUDFLARE_API_TOKEN")
    if not token:
        print("credential error: set the CLOUDFLARE_API_TOKEN environment "
              "variable", file=sys.stderr)
        return 2
    url = "https://api.cloudflare.com/client/v4/accounts/%s/r2/buckets/%s/objects/%s" % (acct, bucket, key)
    req = urllib.request.Request(url, method="GET")
    req.add_header("Authorization", f"Bearer {token}")
    h = hashlib.sha256()
    with urllib.request.urlopen(req, timeout=120) as r, open(out, "wb") as f:
        while True:
            chunk = r.read(65536)
            if not chunk:
                break
            h.update(chunk)
            f.write(chunk)
    print(h.hexdigest())
    return 0


if __name__ == "__main__":
    sys.exit(main())
