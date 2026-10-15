#!/usr/bin/env python3
"""Upload a file to R2 using the CLOUDFLARE_API_TOKEN environment
variable (scoped Bearer token; the token needs R2 write permission).
Usage: r2put.py <account_id> <bucket> <key> <local_path> [content_type]
PUTs the file bytes to the R2 object key. Prints sha256 of the uploaded bytes."""
import hashlib
import mimetypes
import os
import sys
import urllib.request


def main() -> int:
    acct, bucket, key, path = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    ctype = sys.argv[5] if len(sys.argv) > 5 else (mimetypes.guess_type(path)[0] or "application/octet-stream")
    token = os.environ.get("CLOUDFLARE_API_TOKEN")
    if not token:
        print("credential error: set the CLOUDFLARE_API_TOKEN environment "
              "variable", file=sys.stderr)
        return 2
    with open(path, "rb") as f:
        data = f.read()
    print("sha256:", hashlib.sha256(data).hexdigest(), "bytes:", len(data), file=sys.stderr)
    url = "https://api.cloudflare.com/client/v4/accounts/%s/r2/buckets/%s/objects/%s" % (acct, bucket, key)
    req = urllib.request.Request(url, data=data, method="PUT")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", ctype)
    with urllib.request.urlopen(req, timeout=180) as r:
        print(r.status, r.read(200).decode("utf-8", "replace")[:200])
    return 0


if __name__ == "__main__":
    sys.exit(main())
